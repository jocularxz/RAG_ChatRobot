import json
import os
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.runnables.history import RunnableWithMessageHistory

def get_history(session_id):
    return FileChatMessageHistory(
        session_id=session_id,
        storage_path="D:/大模型微调/learningagent/P4_RAG项目案例/chat_histories/"  #存储文件夹路径
    )


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id        #会话id
        self.storage_path = storage_path    #不同会话id的存储文件，所在的文件夹路径
        #完整的文件路径
        self.file_path = os.path.join(storage_path, self.session_id)
        #确保存储文件夹存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequence序列 类似list、tuple
        all_messages = list(self.messages)  #默认定义的获取消息的属性，已有消息列表
        all_messages.extend(messages)      #新旧消息融合成一个list

        #将数据同步写入本地文件中
        #类对象写入文件—>一堆二进制
        #为了方便，可以将BaseMessage消息转为字典（借助json模块以json字符串写入文件）
        #官方message_to_dict函数：单个消息对象（BaseMessage类实例）->字典
        # new_messages = []
        # for message in all_messages:
        #     new_messages.append(message_to_dict(message))
        new_messages = [message_to_dict(message) for message in all_messages]
        #将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)
    @property #@property装饰器，将方法变为属性调用
    def messages(self) -> list[BaseMessage]:
        """获取消息列表属性"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)  #从文件中读取json字符串，并转为python数据结构
            #官方messages_from_dict函数:[字典,字典,...]->[消息,消息,消息...]
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []
        
    def clear(self) -> None:
        """清空消息记录"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)