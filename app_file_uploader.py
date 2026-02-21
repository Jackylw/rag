"""
知识库更新服务Web页面
"""
import streamlit as st

# 添加网页标题
st.title("知识库更新服务")

# 文件上传组件
uploader_file = st.file_uploader(
    "上传文件 (TXT)",
    type=["txt"],
    accept_multiple_files=False,  # 是否允许上传多个文件

)

if uploader_file is not None:
    # 获取文件信息
    file_name = uploader_file.name
    file_size = uploader_file.size / 1024  # 转换为KB
    file_type = uploader_file.type
    st.subheader(f"文件名: {file_name}")
    st.write(f"文件类型: {file_type} | 文件大小: {file_size:.2f} KB")

    # 读取文件内容
    file_content = uploader_file.read().decode("utf-8")
    st.write("文件内容预览:")
    st.text(file_content[:500])  # 预览前500个字符