# RAG 智能客服项目文档

## 1. 项目简介

本项目是一个基于 RAG (Retrieval-Augmented Generation, 检索增强生成) 技术的智能客服/知识库问答系统。项目利用 **LangChain** 框架构建，结合 **ChromaDB** 向量数据库、**DashScope** (通义千问) 的 Embedding 和 LLM 模型，实现了私有知识库的构建与基于知识库的智能问答。

核心功能包括：
- **知识库管理**：支持上传文本文件，自动进行文本切分、向量化并存入 ChromaDB。内置 MD5 校验机制，防止重复上传。
- **智能问答**：基于用户问题检索知识库相关内容，结合对话历史（Context-Aware），由大模型生成准确回答。
- **会话记忆**：支持基于文件的长时会话历史存储，能够进行多轮对话。
- **Web 交互界面**：提供两个 Streamlit 界面，分别用于“知识库管理”和“在线问答”。

## 2. 项目文件结构

```text
rag/
├── app_file_uploader.py   # [入口] 知识库管理 Web 界面 (Streamlit)
├── app_qa.py              # [入口] 智能客服问答 Web 界面 (Streamlit)
├── config_data.py         # [配置] 项目全局配置文件 (模型、路径、参数等)
├── file_history_store.py  # [工具] 基于文件的会话历史存储服务
├── knowledge_base.py      # [核心] 知识库服务 (文档处理、向量化入库)
├── rag.py                 # [核心] RAG 核心逻辑 (检索链构建、Prompt工程)
├── vector_stores.py       # [核心] 向量数据库服务 (ChromaDB 封装)
├── data/                  # [数据] 存放原始文本数据及 ChromaDB 数据库文件
│   ├── chroma_db/         # 向量数据库持久化目录
│   ├── md5_records.txt    # 已上传文件的 MD5 记录
│   └── *.txt              # 示例文本文件
└── chat_history/          # [数据] 存放用户的会话历史记录 (JSON格式)
```

## 3. 详细功能说明

### 3.1 核心模块
- **`config_data.py`**: 集中管理配置项，包括 ChromaDB 集合名称、Embedding 模型 (`text-embedding-v4`)、LLM 模型 (`qwen3-max-preview`)、文本切分参数 (`chunk_size=1000`) 等。
- **`vector_stores.py`**: 封装 Chroma 客户端，提供获取 Retriever (检索器) 的接口。
- **`knowledge_base.py`**: 负责将上传的文本数据清洗、切分（使用 `RecursiveCharacterTextSplitter`），并计算 MD5 值进行去重，最后向量化存入数据库。
- **`rag.py`**: 构建 LangChain 的 Runnable 链。整合了检索器、Prompt 模板、LLM 和历史记录功能 (`RunnableWithMessageHistory`)，实现了完整的 RAG 流程。
- **`file_history_store.py`**: 自定义实现了 `BaseChatMessageHistory`，将用户的对话记录以 JSON 格式存储在本地文件系统中，确保重启后历史记录不丢失。

### 3.2 应用入口
- **`app_file_uploader.py`**: 提供简洁的 UI，允许管理员上传 TXT 文件更新知识库。
- **`app_qa.py`**: 提供类似 ChatGPT 的聊天界面，用户输入问题后，系统流式输出回答。

## 4. 环境准备与运行

### 4.1 安装依赖
请确保安装了以下核心库：
```bash
pip install streamlit langchain langchain-community langchain-chroma langchain-core dashscope
```
*(注意：请确保已配置 DashScope API Key 环境变量，或在代码中显式指定)*

### 4.2 运行知识库管理界面
启动后可上传本地 TXT 文件到知识库：
```bash
streamlit run app_file_uploader.py
```

### 4.3 运行智能客服界面
启动后即可开始对话：
```bash
streamlit run app_qa.py
```

## 5. 项目流程图解

**离线构建流程 (Knowledge Base Construction):**
`上传 TXT` -> `MD5 校验` -> `文本切分 (Splitter)` -> `向量化 (Embedding)` -> `存入 ChromaDB`

**在线问答流程 (RAG Pipeline):**
`用户提问` -> `加载历史记录` -> `向量化检索 (Retriever)` -> `构建 Prompt (Query + Context + History)` -> `LLM 生成` -> `流式返回`
