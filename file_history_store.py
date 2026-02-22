import json
import os
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict


def get_history(session_id: str):
    """获取会话历史记录"""
    return FileChatMessageHistory(session_id, store_path="./chat_history")


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, store_path: str = "./chat_history"):
        self.session_id = session_id  # 会话id
        self.store_path = store_path  # 不同会话id的消息存储路径
        # 完整的文件存储路径
        self.file_path = os.path.join(self.store_path, self.session_id)
        os.makedirs(self.store_path, exist_ok=True)

    def add_message(self, message: BaseMessage) -> None:
        self.add_messages([message])

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)  # 先将当前消息转换为列表
        all_messages.extend(messages)  # 新的消息添加到列表中
        new_messages = [message_to_dict(msg) for msg in all_messages]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)

    # 获取会话历史记录
    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages = json.load(f)
                return messages_from_dict(messages)
        except FileNotFoundError:
            return []

    # 清空会话历史记录
    def clear(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)


