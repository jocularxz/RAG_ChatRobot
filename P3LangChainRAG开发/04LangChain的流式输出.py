from langchain_community.llms.tongyi import Tongyi

model = Tongyi(model="qwen-max")

#通过stream方法获得流式输出
res = model.stream(input="请介绍一下杭州的历史文化")

for chunk in res:
    print(chunk, end="", flush=True)