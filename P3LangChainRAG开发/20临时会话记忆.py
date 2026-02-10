from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

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

store = {}  # 用于存储会话历史的简单字典
def get_history(session_id):
    """根据会话ID获取对应的InMemoryChatMessageHistory对象"""
    # 在实际应用中，这里可以连接数据库或其他存储系统
    # 这里为了演示，使用一个简单的字典来存储会话历史
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# 创建一个新的链，对原有链增强功能：自动附加历史消息
conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,                #通过会话id获取InMemoryChatMessageHistory类对象
    input_messages_key="input",                      #基础链中表示用户输入的key
    history_messages_key="chat_history",           #表示用户输入在模型中的占位符 
)

if __name__ == "__main__":
    #固定格式，添加LangChain的配置，为当前程序配置所属的session id
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }

    res = conversation_chain.invoke(
        {"input":"小明有2只猫"}, session_config
    )
    print("第1次执行：", res)
    res = conversation_chain.invoke(
        {"input":"小刚有1只狗"}, session_config
    )
    print("第2次执行：", res)
    res = conversation_chain.invoke(
        {"input":"一共有多少只宠物？"}, session_config
    )
    print("第3次执行：", res)