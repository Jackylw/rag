# Chroma数据库配置
collection_name = "knowledge_rag"
embedding_function = DashScopeEmbeddings(
    model="text-embedding-v4"
)
persist_directory = "./data/chroma_db"

# RecursiveCharacterTextSplitter配置
chunk_size = 1000  # 每个文档分块的最大字符数
chunk_overlap = 100  # 分块之间的重叠字符数
separators = ["\n\n", "\n", " ", ""]  # 用于分割文本的分隔符列表



# md5记录文件路径，用于记录已上传文档的md5值，避免重复上传
md5_path = "./data/md5_records.txt"
