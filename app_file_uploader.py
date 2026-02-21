"""
知识库更新服务Web页面
run: streamlit run app_file_uploader.py


streamlit : 当web刷新时、页面元素发生变化，代码会重新执行一遍

"""
import streamlit as st
from time import sleep
from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")

# 文件上传组件
uploader_file = st.file_uploader(
    "上传文件 (TXT)",
    type=["txt"],
    accept_multiple_files=False,  # 是否允许上传多个文件

)

# 初始化计数器，记录上传文件的数量
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if uploader_file is not None:
    # 获取文件信息
    file_name = uploader_file.name
    file_size = uploader_file.size / 1024  # 转换为KB
    file_type = uploader_file.type
    st.subheader(f"文件名: {file_name}")
    st.write(f"文件类型: {file_type} | 文件大小: {file_size:.2f} KB")

    text = uploader_file.read().decode("utf-8")

    with st.spinner("正在上传..."):
        sleep(1)
        res = st.session_state["service"].upload_by_str(text, file_name)
        st.write(res)
