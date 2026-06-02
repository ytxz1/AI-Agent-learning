"""聊天记录管理模块。

Streamlit 页面每次交互都会重新执行脚本。
所以聊天记录不能只放在普通变量里，需要借助 st.session_state。

为了让核心逻辑更容易理解，这里先写一个纯 Python 的 ChatStore。
app.py 会把它放进 session_state 中保存。
"""

from __future__ import annotations

import sys
from pathlib import Path


DAY25_DIR = Path(__file__).resolve().parents[1]
if str(DAY25_DIR) not in sys.path:
    sys.path.insert(0, str(DAY25_DIR))

try:
    from .schemas import ChatMessage
except ImportError:
    from schemas import ChatMessage


class ChatStore:
    """保存聊天记录的简单类。"""

    def __init__(self) -> None:
        self.messages: list[ChatMessage] = []

    def add_user_message(self, content: str) -> None:
        """添加用户消息。"""

        self.messages.append(ChatMessage(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        """添加助手消息。"""

        self.messages.append(ChatMessage(role="assistant", content=content))

    def clear(self) -> None:
        """清空聊天记录。"""

        self.messages.clear()

    def count(self) -> int:
        """返回消息数量。"""

        return len(self.messages)


if __name__ == "__main__":
    # 练习题答案 4：
    # 如何测试聊天记录管理？
    # 如何添加：创建 ChatStore，分别添加 user 和 assistant 消息。
    store = ChatStore()
    store.add_user_message("你好")
    store.add_assistant_message("你好，我是 Day25 前端助手。")
    print("练习题答案 4：当前聊天记录数量", store.count())
    for message in store.messages:
        print(message.model_dump())
