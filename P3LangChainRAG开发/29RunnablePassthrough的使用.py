"""
提示词：用户的提问 + 向量库中检索到的参考资料
"""
from langchain_community.chat_models import ChatTongyi
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
        ("human","用户提问：{question}"),
    ]
)

def print_prompt(prompt):
    print(prompt.to_string())
    print("="*20)
    return prompt

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(model="text-embedding-v4"),
)

#准备一下资料（向量库的数据）
#add_texts 传入一个 list[str]
vector_store.add_texts(["减肥就是要少吃多练","在减脂期问吃东西很重要，清淡少油控制卡路里摄入并运动起来","跑步是很好的运动哦"])

input_text = "怎么减肥？"


#langchain中向量存储对象，有一个方法：as_retriever，可以返回一个Runnable接口的子类实例对象
retriever = vector_store.as_retriever(search_kwargs={"k":2})

def format_func(docs):
    if not docs:
        return "没有相关资料"
    reference_text = "["
    for doc in docs:
        reference_text += doc.page_content
    reference_text+= "]" #把从向量库搜到的文档内容拼成一个字符串，前后加上[]形成引用资料。
    return reference_text



chain = (
    {"context":retriever | format_func,"question":RunnablePassthrough()} | prompt | print_prompt | model | StrOutputParser()
)

res = chain.invoke(input_text)
print(res)