from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda


#模型创建
model = ChatTongyi(model_name="qwen3-max")  # 初始化通义千问聊天模型

str_parser = StrOutputParser()  # 初始化字符串输出解析器
#第一个提示词模板
first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，请帮我起个名字，仅回复我名字，无需额外内容。" 
)

#第二个提示词模板
second_prompt = PromptTemplate.from_template(
    "姓名:{name}，请帮我解析含义。"
)

# 将普通函数 / 匿名函数（lambda）封装为可执行的 Runnable 组件 的工具
my_func = RunnableLambda(lambda ai_msg:{"name": ai_msg.content})  # 定义一个RunnableLambda用于提取名字

# chain = first_prompt | model | my_func | second_prompt | model | str_parser
chain = first_prompt | model | (lambda ai_msg:{"name": ai_msg.content}) | second_prompt | model | str_parser #用普通函数时，会自动转换为RunnableLambda
for chunk in chain.stream(input={"lastname":"赵","gender":"女孩"}):  # 流式调用链
    print(chunk, end="", flush=True)