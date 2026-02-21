# RAG 项目文档

## 项目简介

本次项目以"某东商品衣服"为例，以衣服属性构建本地知识。使用者可以自由更新本地知识，用户问题的答案也是基于本地知识生成的。

## 项目架构

### 离线流程
1. **本地知识文件加载和读取**
2. **文本切分**
3. **向量化数据库构建**

### 在线流程
1. **Query向量化**
2. **向量匹配**
3. **Prompt工程**
4. **提交LLM生成答案**

## 项目文件结构

```
rag/
├── app_file_upload.py       # 知识库更新主程序 (streamlit)
├── app_qa.py                # 项目主程序 (streamlit)，启动对话WEB页面
├── config_data.py           # 配置文件
├── file_history_store.py    # 长期会话记忆存储服务
├── knowledge_base.py        # 知识库更新服务
├── rag.py                   # rag核心服务
├── vector_stores.py         # 向量存储服务
├── data/
│   ├── 尺码推荐.txt
│   ├── 洗涤养护.txt
│   └── 颜色选择.txt
├── chat_history/
└── chroma_db/
```

## 使用说明

pip install streamlit