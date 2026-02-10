md5_path="D:/大模型微调/learningagent/P4_RAG项目案例/md5.text"

#Chroma向量数据库配置
collection_name="rag"
persist_directory="D:/大模型微调/learningagent/P4_RAG项目案例\chroma_db"

#spliter
chunk_size=1000
chunk_overlap=100
separtors = ["\n\n","\n","。","！","？","！？","？！"," "]
max_split_char_number = 1000 #文本分割阈值

#
similarity_threshold = 2 #相似度阈值,检索返回匹配的文档数量
embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3-max"

session_config = {
        "configurable":{
            "session_id":"user_001",
        }
}
