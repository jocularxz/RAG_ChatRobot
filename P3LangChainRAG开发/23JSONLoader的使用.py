from langchain_community.document_loaders.json_loader import JSONLoader

loader = JSONLoader(
    file_path="P3LangChainRAG开发/data/stu_json_lines.json", #必填
    jq_schema=".name",  #必填，jq表达式，提取每个学生的姓名
    text_content=False,
    json_lines=True,
)

document = loader.load()
print(type(document), document)  #打印文档的内容