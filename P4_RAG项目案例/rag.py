import config_data as config
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder
from file_history_store import get_history
from langchain_core.runnables.history import RunnableWithMessageHistory
def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)

    return prompt

class RagService(object):

    def __init__(self):
        self.vector_service = VectorStoreService(
            DashScopeEmbeddings(model=config.embedding_model_name)
            )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主，"
                 "简洁和专业的回答用户问题。参考资料:{context}。"),
                ("system","并且我提供用户的对话历史记录，如下："),
                MessagesPlaceholder(variable_name="history"),
                ("user","请回答用户问题：{input}")
            ]
        )

        self.chat_model = ChatTongyi(model=config.chat_model_name)

        self.chain = self.__get_chain()
    
    def __get_chain(self):
        """获得最终的执行链"""
        retriever = self.vector_service.get_retriever()    #获取向量检索

        def format_document(docs):
            if not docs:
                return "无相关参考资料"
            
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"

            return formatted_str
        
        def format_for_retriever(value):
            # print("--------------------",value)
            return value["input"]
        
        def format_for_prompt_template(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            # print("--------------------",value)
            return new_value

        chain = (
            {"input":RunnablePassthrough(),
             "context": RunnableLambda(format_for_retriever) | retriever | format_document
            } | RunnableLambda(format_for_prompt_template) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        conversion_chain = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=get_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        return conversion_chain

if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id":"user_001",
        }
        }
    res = RagService().chain.invoke({"input":"挂载的数据文档是谁创建的"}, config=session_config)
    print(res)

