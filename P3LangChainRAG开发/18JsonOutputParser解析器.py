from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

#创建所需的解析器
str_parser = StrOutputParser()  # 初始化字符串输出解析器
json_parser = JsonOutputParser()  # 初始化JSON输出解析器

#模型创建
model = ChatTongyi(model_name="qwen3-max")  # 初始化通义千问聊天模型

#第一个提示词模板
first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，请帮我起个名字，仅回复我名字，无需额外内容。" \
    "并封装为JSON格式返回给我。要求key是name，value是名字，请严格遵守格式要求。"
)

#第二个提示词模板
second_prompt = PromptTemplate.from_template(
    "姓名:{name}，请帮我解析含义。"
)

chain = first_prompt | model | json_parser | second_prompt | model 
res = chain.invoke(input={"lastname":"李","gender":"男孩"})
print(res.content)  
print(type(res))