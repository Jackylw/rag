from langchain_community.chat_models import ChatTongyi
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from typing import List
import config_data
from vector_stores import VectorStoreService

def print_prompt(prompt):
    print("="*50)
    print(prompt)
    print("="*50)
    return prompt

class RagService:
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding_function=config_data.embedding_function
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供已知的参考资料为主，简洁的回答用户问题，参考资料:{context}"),
                ("user", "{question}"),
            ]
        )
        self.chat_model = ChatTongyi(
            model=config_data.chat_model
        )
        self.chain = self.__get_chain()

    def __get_chain(self):
        """获取RAG链"""
        retriever = self.vector_service.get_retriever()

        def format_docs(docs: List[Document]):
            """格式化文档，将文档内容合并为一个字符串"""
            if not docs:
                return "没有相关文档"
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            return formatted_str

        chain = (
                {
                    "context": retriever | format_docs,
                    "question": RunnablePassthrough(),
                } | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        return chain


if __name__ == "__main__":
    rag_service = RagService()
    res = rag_service.chain.invoke("我的身高是180cm，体重是85kg，应该选什么尺码")
    print(res)
