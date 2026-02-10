from langchain_chroma import Chroma
import config_data as config
from langchain_community.embeddings import DashScopeEmbeddings

class VectorStoreService(object):
    def __init__(self,embedding):
        """
        __init__ 的 Docstring
        
        :param self: 说明
        :param embedding: 嵌入模型的传入/
        """
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name, #向量数据库的名称
            embedding_function=self.embedding,
            persist_directory=config.persist_directory, #向量数据库的存储路径
        )

    def get_retriever(self):
        """获取向量数据库的检索器，方便加入chain"""
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})

if __name__ == "__main__":
    retriever = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v4")).get_retriever()
    res = retriever.invoke()
    print(res)
