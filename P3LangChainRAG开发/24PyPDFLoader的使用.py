from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path="D:/A New Axis of Sparsity for Large Language Models.pdf",
    mode = "page", #默认是page模式，每个页面形成一个Document文档对象，
                   #single模式是将整个PDF内容形成一个Document文档对象
)

i = 0
for doc in loader.lazy_load():
    i += 1
    print("="*20)
    print(type(doc), doc)  # 打印每个文档的内容