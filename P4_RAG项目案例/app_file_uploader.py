"""
基于Streamlit完成WEB网页上传服务
streamlit存在组件改变脚本就重新执行一遍的问题
"""
import streamlit as st
from knowledge_base import KnowledgeBaseService
from langchain_community.embeddings import DashScopeEmbeddings
# 添加网页标题
st.title("知识库更新服务")

#file_uploader组件
uploaded_file = st.file_uploader(
    "请上传知识库文件", 
    type=['pdf', 'docx', 'txt'],
     accept_multiple_files=False,
    )
if "service" not in st.session_state: #如果session_state中没有service对象
    st.session_state["service"] = KnowledgeBaseService() #创建一个KnowledgeBaseService对象，并将其存储到session_state中

if uploaded_file is not None:
    #获取文件的信息
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size/1024 #单位：KB

    st.subheader(f"文件名: {file_name}")
    st.write(f"格式: {file_type} | 大小: {file_size:.2f} KB")

    
    text = uploaded_file.getvalue().decode('utf-8') #将文件内容转换为utf-8编码的字节序列
    st.write(text[:100]) #显示文件内容的前100个字符
    with st.spinner("载入知识库中。。。"):
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)