from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    file_path='P3LangChainRAG开发/data/python基础使用语法.txt',
    encoding='utf-8'
)
docs = loader.load()
# print(docs, len(docs))  #打印文档的内容

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,  #每个小块的最大字符数
    chunk_overlap=20,  #重叠字符数
    separators=["\n\n", "\n", "。", "，", "、", "；", "："],  #文本自然段落分隔的依据符号
    length_function=len  #计算文本长度的函数
)

split_docs = splitter.split_documents(docs)
print(len(split_docs))
for i, doc in enumerate(split_docs):
    print("="*20)
    print(doc.page_content)