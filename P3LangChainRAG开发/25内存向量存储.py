from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma

# vector_store = InMemoryVectorStore(
#     embedding=DashScopeEmbeddings()
# )

vector_store = Chroma(
    collection_name="test",
    embedding_function=DashScopeEmbeddings(),
    persist_directory="./chroma"
)

loader = CSVLoader(
    file_path='P3LangChainRAG开发/data/info.csv',
    encoding='utf-8',
    source_column='source'#指定名为 "source" 的列作为“来源”字段
)

documents = loader.load()
# print(documents,type(documents))

#id1 id2 id3 id4
#向量存储 新增、删除、检索
vector_store.add_documents(
    documents=documents,
    ids=["id"+str(i) for i in range(1,len(documents)+1)]
)

#删除 传入[id,id...]
vector_store.delete(
    ids=["id1","id2"]
)

#检索 返回类型list[Document]
result = vector_store.similarity_search(
    query="python能月薪过万吗",
    k=2,
    filter={"source":"黑马程序员"} #根据source字段进行过滤
)
print(result)