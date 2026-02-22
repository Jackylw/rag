# Chroma数据库配置
from langchain_community.embeddings import DashScopeEmbeddings

collection_name = "knowledge_rag"
embedding_function = DashScopeEmbeddings(
    model="text-embedding-v4"
)
chat_model = "qwen3-max-preview"
persist_directory = "./data/chroma_db"

# RecursiveCharacterTextSplitter配置
chunk_size = 1000  # 每个文档分块的最大字符数
chunk_overlap = 100  # 分块之间的重叠字符数
separators = ["\n\n", "\n", ".", "！", "？", "!", "?", "。"," ",""]  # 用于分割文本的分隔符列表
split_char_len = 1000  # 超过这个长度的文本会被递归分割

# 知识库检索器配置
retriever_k = 2  # 每次检索返回的文档数量



# md5记录文件路径，用于记录已上传文档的md5值，避免重复上传
md5_path = "./data/md5_records.txt"

session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }