from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

#得到模型对象，qwen3-max是聊天模型
model = ChatTongyi(model_name="qwen3-max")

#构造对话消息
messages = [
    SystemMessage(content="你是一个田园诗人"),
    HumanMessage(content="请你写一首关于春天的诗歌"),
    AIMessage(content="春天来了，花儿开了，鸟儿唱了，万物复苏，生机勃勃。"),
    HumanMessage(content="按照你上一个回复的格式，再写一首关于冬天的诗。")
]

#调用tream流式接口
response = model.stream(input = messages)

#for循环迭代打印输出，通过.content来获取到内容
for chunk in response:
    print(chunk.content, end="", flush=True)