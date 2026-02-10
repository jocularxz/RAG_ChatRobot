from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

prompt_template = PromptTemplate.from_template( 
    "我的邻居姓{lastname}，刚生了{gender}，请帮我起个名字，简单回答。"
)

# 调用.format()方法注入信息即可
# prompt_text = prompt_template.format(lastname="王", gender="男孩")

# model = Tongyi(model_name="qwen-max")
# res = model.invoke(input=prompt_text)
# print(res)

#写chain
model = Tongyi(model_name="qwen-max")
chain = prompt_template | model
res = chain.invoke(input={"lastname": "李", "gender": "女孩"})
print(res)