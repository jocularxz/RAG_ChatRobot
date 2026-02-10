from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(
    file_path='P3LangChainRAG开发/data/sample_data.csv', 
    csv_args={
        'delimiter': ',', #指定分隔符
        'quotechar': '"', #指定带有分隔符文本的引用字符是单引号还是双引号
        # 'fieldnames': ['title', 'content'] #指定列名，如果表格已有列名，可省略
    },
    encoding='utf-8'
    )

#批量加载 .load() ->[Document,Document,...]
documents = loader.load()

# for doc in documents:
#     print(type(doc),doc)  #打印每个文档的内容

#懒加载 .lazy_load() 迭代器[Document,Document,...]
for doc in loader.lazy_load():
    print(type(doc),doc)  #打印每个文档的内容

