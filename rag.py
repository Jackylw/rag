from langchain_community.chat_models import ChatTongyi
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnableLambda
from typing import List

import config_data
from file_history_store import get_history
from vector_stores import VectorStoreService


def print_prompt(prompt):
    print("=" * 50)
    print(prompt)
    print("=" * 50)
    return prompt


class RagService:
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding_function=config_data.embedding_function
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供已知的参考资料为主，简洁的回答用户问题，参考资料:{context}"),
                ("system", "根据我提供的对话历史记录，回答用户问题"),
                MessagesPlaceholder(variable_name="history"),
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
                print(">>> [参考资料] 没有检索到相关文档")
                return "没有相关文档"
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            print("=" * 50)
            print(">>> [参考资料]")
            print(formatted_str)
            print("=" * 50)
            return formatted_str

        def print_history(x):
            history = x.get("history", [])
            print("=" * 50)
            print(">>> [历史聊天记录]")
            if not history:
                print("（暂无历史记录）")
            else:
                for msg in history:
                    role = getattr(msg, "type", "unknown")
                    content = getattr(msg, "content", str(msg))
                    print(f"  [{role}]: {content}")
            print("=" * 50)
            return x

        chain = (
                RunnableLambda(print_history)
                | {
                    "context": (lambda x: x["question"]) | retriever | format_docs,
                    "question": lambda x: x["question"],
                    "history": lambda x: x.get("history", []),
                }
                | self.prompt_template
                | RunnableLambda(print_prompt)
                | self.chat_model
                | StrOutputParser()
        )

        # 包装RAG链，添加会话历史记录功能
        conversation_chain = RunnableWithMessageHistory(
            chain,  # RAG链
            get_history,  # 获取会话历史记录的函数
            input_messages_key="question",  # 输入消息的键名
            history_messages_key="history"  # 会话历史记录的键名
        )

        return conversation_chain


if __name__ == "__main__":
    rag_service = RagService()
    res = rag_service.chain.invoke(
        {
            "question": "你知道我的身高和体重吗？我应该选什么尺码的衣服？"
        },
        config=config_data.session_config
    )
    print(res)
