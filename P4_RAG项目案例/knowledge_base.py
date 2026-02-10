"""
知识库
"""
import os
import config_data as config
import hashlib
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
def check_md5(md5_str):
    """检查传入的md5字符串是否已经被处理过了
       return False(md5未处理过) True(md5已处理过,已有记录)
    """
    if not os.path.exists(config.md5_path,):
        #if进入表示文件不存在，那肯定没有处理过这个md5了
        open(config.md5_path,"w",encoding="utf-8").close() #创建一个空文件
        return False
    else:
        for line in open(config.md5_path,"r",encoding="utf-8").readlines(): #遍历文件中的每一行
            line = line.strip() #处理字符串前后的空格和回车
            if line == md5_str:
                return True
        return False
    

def save_md5(md5_str):
    """将传入的md5字符串保存到知识库中"""
    with open(config.md5_path,"a",encoding="utf-8") as f:
        f.write(md5_str+"\n") #将md5字符串写入文件中，每个字符串占一行

def get_string_md5(input_str,encoding="utf-8"):
    """将传入的字符串转换为md5字符串"""
    
    #将字符串转换为bytes字节数组
    input_str = input_str.encode(encoding)
    
    #创建md5对象
    md5_obj = hashlib.md5() #创建一个md5对象，创建一个加密器，把任意文字转成32b的md5字符串
    md5_obj.update(input_str) #将字节数组更新到md5对象中
    md5_hex = md5_obj.hexdigest() #将md5对象转换为16进制字符串  
    return md5_hex  

class KnowledgeBaseService(object):
    def __init__(self):
        self.chroma = Chroma(
            collection_name=config.collection_name, #数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory, #数据库本地存储文件夹
        ) #向量存储的实例Chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, #分割后的文本段最大长度
            chunk_overlap=config.chunk_overlap, #连续文本段之间的字符重叠数量
            separators=config.separtors, #自然段落划分的符号
            length_function=len, #使用python自带的len函数做长度统计的依据
        ) #文本分割器对象

    def upload_by_str(self, data, filename):
        """将传入的字符串数据，进行向量化，存入向量数据库中"""
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已经存在在知识库中"
        
        if len(data) > config.max_split_char_number: #如果文本长度超过了最大分割字符数
            knowledge_chunks = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = { 
            "source":filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"诙谐",
        }

        self.chroma.add_texts(
            texts=knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],#为每个文本段添加元数据，（元数据就是给内容贴的标签，告诉你这内容是谁、什么时候、从哪来的。）
        ) #将文本段和元数据添加到向量数据库中

        save_md5(md5_hex)#将存入过的md5字符串保存到知识库中
        return "[成功]内容已存入知识库"
if __name__ == "__main__":
    service = KnowledgeBaseService()
    res = service.upload_by_str("你好","test.txt")
    print(res)