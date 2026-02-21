from langchain_chroma import Chroma

import config_data


class VectorStoreService:
    """向量存储服务类，用于根据知识库提问"""

    def __init__(self, embedding_function=config_data.embedding_function):
        self.vector_store = Chroma(
            collection_name=config_data.collection_name,
            embedding_function=embedding_function,
            persist_directory=config_data.persist_directory,
        )

    def get_retriever(self):
        """获取向量存储的检索器"""
        return self.vector_store.as_retriever(
            search_kwargs={"k": config_data.retriever_k},  # 每次检索返回的文档数量
        )


if __name__ == "__main__":
    vector_store_service = VectorStoreService()
    retriever = vector_store_service.get_retriever()
    res = retriever.invoke("我的身高是180cm，体重是85kg，应该选什么尺码")
    for i, doc in enumerate(res):
        print(f"Document {i + 1}:")
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}")
        print("-" * 20)
