from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi


chat_prompt_template = ChatPromptTemplate.from_messages(  # 创建一个聊天提示词模板
    [
        ("system", "你是一个婉约派诗人，可以作诗。"),  # 系统消息
        MessagesPlaceholder(variable_name="history"),  # 占位符，表示历史消息,
        ("human", "请再来一首"),  # 用户消息
    ]
)

history_data = [    # 历史消息列表
    ("human", "请帮我写一首关于春天的诗"),
    ("ai", "春风拂面柳丝长，花开满园蝶儿忙。碧水青山映日丽，心随燕舞乐无疆。"),
    ("human", "请帮我写一首关于夏天的诗"),
    ("ai", "烈日炎炎照大地，荷花池畔蛙声齐。绿树成荫清风起，消暑良方莫过溪。"),
]
model = ChatTongyi(model_name="qwen3-max")  # 初始化通义千问聊天模型

#组成链，要求每一个组件都是Runnable接口的子类
chain = chat_prompt_template | model

#通过链去调用invoke或stream
# res = chain.invoke({"history": history_data})  # 调用链进行对话
# print(res.content, type(res))  # 输出模型的回复

#通过stream流式输出
for chunk in chain.stream({"history": history_data}):
    print(chunk.content, end="", flush=True)