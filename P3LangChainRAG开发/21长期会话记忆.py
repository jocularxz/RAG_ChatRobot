import os,json
from typing import Sequence
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_models import ChatTongyi  # 导入ChatTongyi模型
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 导入ChatPromptTemplate和MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser  # 导入StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory  # 导入RunnableWithMessageHistory
#message_to_dict:单个消息对象（BaseMessage类实例）->字典
#messages_from_dict:[字典,字典,...]->[消息,消息,消息...]
#AIMessage,HumanMessage,SystemMessage等类都是BaseMessage的子类

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id        #会话id
        self.storage_path = storage_path    #不同会话id的存储文件，所在的文件夹路径
        #完整的文件路径
        self.file_path = os.path.join(storage_path, self.session_id)
        #确保存储文件夹存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequence序列 类似list、tuple
        all_messages = list(self.messages)  #默认定义的获取消息的属性，已有消息列表
        all_messages.extend(messages)      #新旧消息融合成一个list

        #将数据同步写入本地文件中
        #类对象写入文件—>一堆二进制
        #为了方便，可以将BaseMessage消息转为字典（借助json模块以json字符串写入文件）
        #官方message_to_dict函数：单个消息对象（BaseMessage类实例）->字典
        # new_messages = []
        # for message in all_messages:
        #     new_messages.append(message_to_dict(message))
        new_messages = [message_to_dict(message) for message in all_messages]
        #将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)
    @property #@property装饰器，将方法变为属性调用
    def messages(self) -> list[BaseMessage]:
        """获取消息列表属性"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)  #从文件中读取json字符串，并转为python数据结构
            #官方messages_from_dict函数:[字典,字典,...]->[消息,消息,消息...]
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []
        
    def clear(self) -> None:
        """清空消息记录"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


model = ChatTongyi(model_name="qwen3-max")  # 初始化通义千问聊天模型
# prompt = PromptTemplate.from_template(
#     "你需要根据会话历史回应用户问题。对话历史：{chat_history}\n用户问题：{input}\n请给出简洁的回答。"
# )

prompt = ChatPromptTemplate.from_messages( 
    [
        ("system", "你需要根据会话历史回应用户问题。对话历史，"),  # 系统消息
        MessagesPlaceholder(variable_name="chat_history"),  # 占位符，表示历史消息,
        ("human", "回答如下问题，{input}"),  # 用户消息   
    ]
) # 创建一个聊天提示词模板

str_parser = StrOutputParser()  # 初始化字符串输出解析器

def print_prompt(full_prompt):
    """打印完整的提示词内容"""
    print("="*20 ,full_prompt.to_string(),"="*20)
    return full_prompt

base_chain = prompt | print_prompt | model | str_parser  # 组成基础链

def get_history(session_id):
    return FileChatMessageHistory(
        session_id=session_id,
        storage_path="./chat_histories/"  #存储文件夹路径
    )


# 创建一个新的链，对原有链增强功能：自动附加历史消息
conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,                #通过会话id获取FileChatMessageHistory类对象
    input_messages_key="input",                      #基础链中表示用户输入的key
    history_messages_key="chat_history",           #表示用户输入在模型中的占位符 
)

if __name__ == "__main__":
    #固定格式，添加LangChain的配置，为当前程序配置所属的session id
    session_config = {
        "configurable": {
            "session_id": "user_002"
        }
    }

    # res = conversation_chain.invoke(
    #     {"input":"小明有2只猫"}, session_config
    # )
    # print("第1次执行：", res)
    # res = conversation_chain.invoke(
    #     {"input":"小刚有1只狗"}, session_config
    # )
    # print("第2次执行：", res)
    res = conversation_chain.invoke(
        {"input":"一共有多少只宠物？"}, session_config
    )
    print("第3次执行：", res)

    """在原脚本中，RunnableWithMessageHistory 自动完成了 “取出”。你可能注意到，原脚本中没有显式写 history_obj.messages，
    但历史记录依然被用上了 —— 这是因为 RunnableWithMessageHistory（LangChain 用于管理会话历史的组件）帮我们自动做了 “调用 
    messages 属性” 这一步：当你调用 conversation_chain.invoke(...) 时，RunnableWithMessageHistory 会先调用 
    get_history(session_id)，拿到该用户的 FileChatMessageHistory 实例；它会自动访问这个实例的 messages 属性，取出历史记录；
    把取出的历史记录填充到 prompt 中的 MessagesPlaceholder(variable_name="chat_history") 位置，再传给模型。"""