from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate

template = PromptTemplate.from_template("我的邻居{name}，喜欢{hobby}")

res = template.format(name="小明", hobby="打篮球")
print(res,type(res))

res2 = template.invoke(input={"name":"小红","hobby":"画画"})
print(res2,type(res2))