"""练习 05：完整前端逻辑演示。

这个脚本不打开浏览器，而是在命令行模拟一次完整流程：
1. 用户提问；
2. 保存用户消息；
3. 调用本地 Agent；
4. 保存助手回复；
5. 打印最终聊天记录。
"""

from __future__ import annotations

from rich.console import Console

from modules.chat_store import ChatStore
from modules.local_agent import LocalAgent


console = Console()


def main() -> None:
    """运行完整前端逻辑演示。"""

    console.rule("[bold green]练习 05：完整前端逻辑演示")
    store = ChatStore()
    agent = LocalAgent()

    question = "Day25 前端页面要学什么？"
    store.add_user_message(question)

    response = agent.answer(question)
    store.add_assistant_message(response.answer)

    console.print("Agent 回答来源：", response.source)
    console.print("使用工具：", response.used_tools)
    console.print("\n完整聊天记录：")
    for message in store.messages:
        console.print(f"[{message.role}] {message.content}")

    # 练习题答案：
    # 题目：如何把这个命令行流程搬到 Streamlit 页面？
    # 如何添加：
    # 1. 用 st.chat_input 接收 question；
    # 2. 用 store.add_user_message 保存用户问题；
    # 3. 调用 LocalAgent 或 AgentAPIClient；
    # 4. 用 store.add_assistant_message 保存回答；
    # 5. 用 st.chat_message 渲染消息。


if __name__ == "__main__":
    main()
