"""练习 04：页面状态和聊天记录。

Streamlit 的一个重要概念是：页面交互会导致脚本重新运行。
所以聊天记录必须保存起来。

Day25 使用 ChatStore 管理聊天记录，在 app.py 中放入 st.session_state。
"""

from __future__ import annotations

from rich.console import Console

from modules.chat_store import ChatStore


console = Console()


def main() -> None:
    """演示 ChatStore 的用法。"""

    console.rule("[bold green]练习 04：页面状态")
    store = ChatStore()
    store.add_user_message("你好，Day25")
    store.add_assistant_message("你好，这是一个 Streamlit 前端页面示例。")

    console.print("消息数量：", store.count())
    for message in store.messages:
        console.print(message.model_dump())

    store.clear()
    console.print("清空后消息数量：", store.count())

    # 练习题答案：
    # 题目：为什么不直接用普通 list 保存聊天记录？
    # 如何添加：
    # 普通 list 在 Streamlit 重新运行脚本时会重置；
    # 应该把 ChatStore 放到 st.session_state 里。


if __name__ == "__main__":
    main()
