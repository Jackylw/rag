"""
知识库服务类，用于管理知识库的上传和检索
只有满足md5检测的知识才会被存进知识库
"""
import os
from pathlib import Path

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config_data
import hashlib
import datetime


def _ensure_md5_dir():
    Path(config_data.md5_path).parent.mkdir(parents=True, exist_ok=True)


def check_md5(md5_str: str) -> bool:
    if not os.path.exists(config_data.md5_path):
        return False

    with open(config_data.md5_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() == md5_str:
                return True
    return False


def save_md5(md5_str: str) -> bool:
    if check_md5(md5_str):
        return False
    _ensure_md5_dir()
    with open(config_data.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')
    return True


def get_string_md5(input_str: str, encoding='utf-8') -> str:
    """
    将传入的字符串转为md5
    """
    str_bytes = input_str.encode(encoding)  # 将字符串转换为字节序列
    md5_hash = hashlib.md5()  # 创建md5哈希对象
    md5_hash.update(str_bytes)  # 更新哈希对象的状态，将字节序列加入计算
    return md5_hash.hexdigest()  # 返回md5哈希值的十六进制表示


class KnowledgeBaseService:
    """知识库服务类，用于管理知识库的上传"""

    def __init__(self) -> None:
        Path(config_data.persist_directory).mkdir(parents=True, exist_ok=True)  # 确保数据库文件存储路径存在
        self.chroma = Chroma(
            collection_name=config_data.collection_name,  # 数据库表名
            embedding_function=config_data.embedding_function,  # 嵌入模型
            persist_directory=config_data.persist_directory,  # 数据库文件存储路径
        )  # 向量存储的实例
        self.splitter = RecursiveCharacterTextSplitter(  # 文本分割器对象
            chunk_size=config_data.chunk_size,  # 每个文档分块的最大字符数
            chunk_overlap=config_data.chunk_overlap,  # 分块之间的重叠字符数
            separators=config_data.separators,  # 用于分割文本的分隔符列表
            length_function=len  # 计算文本长度的函数，这里使用内置的len函数
        )

    def upload_by_str(self, data: str, filename: str) -> str:
        """
        上传字符串到知识库

        :param data: 要上传的文本数据
        :param filename: 文件名
        """
        if not data or not data.strip():
            return "[失败]上传内容为空，无法入库"
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已经存在在知识库中"
        # 对文本进行分块
        if len(data) > config_data.split_char_len:
            knowledge_chunks = self.splitter.split_text(data)
        else:
            knowledge_chunks = [data]
        # 元数据
        metadata = {
            "source": filename,
            # 20xx-xx-xx xx:xx:xx
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "admin",
        }
        self.chroma.add_texts(
            texts=knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )
        save_md5(md5_hex)
        return "[成功]知识库上传成功"


if __name__ == "__main__":
    service = KnowledgeBaseService()
    r = service.upload_by_str("这是一个测试文本", "test2.txt")
    print(r)
