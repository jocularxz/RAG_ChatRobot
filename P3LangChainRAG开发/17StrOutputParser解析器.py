from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

parser = StrOutputParser()  # 初始化字符串输出解析器,可以将AImessage转换为字符串
model = ChatTongyi(model_name="qwen3-max")  # 初始化通义千问聊天模型
prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，请帮我起个名字，简单回答。"
)

chain = prompt | model | parser  | model| parser  # 组成链，包含提示词模板、模型和输出解析器
res = chain.invoke(input={"lastname":"王","gender":"女孩"})
print(res)  # 输出最终结果
print(type(res))  # 输出结果类型