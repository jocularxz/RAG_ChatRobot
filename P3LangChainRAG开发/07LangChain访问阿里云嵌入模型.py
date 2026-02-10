from langchain_community.embeddings import DashScopeEmbeddings

# 创建模型对象，不传model默认用的是text-embedding-v1
model = DashScopeEmbeddings()

# 不用invoke stream
# embed_query、embed_documents方法直接传入文本即可
print(model.embed_query("你好"))
print(model.embed_documents(["你好", "今天天气真好啊！"]))