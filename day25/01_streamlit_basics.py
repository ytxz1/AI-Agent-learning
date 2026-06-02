"""练习 01：Streamlit 基础。

这个脚本说明一个 Streamlit 页面通常由哪些部分组成。
注意：真正打开网页要运行 streamlit run app.py。
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table


console = Console()


def main() -> None:
    """打印 Streamlit 基础组件说明。"""

    console.rule("[bold green]练习 01：Streamlit 基础")
    table = Table(title="常用 Streamlit 组件")
    table.add_column("组件")
    table.add_column("作用")
    table.add_column("Day25 用法")
    table.add_row("st.title", "显示标题", "页面标题可以用它，也可以用自定义 HTML")
    table.add_row("st.sidebar", "侧边栏", "放运行模式、API 地址、清空按钮")
    table.add_row("st.chat_input", "聊天输入框", "用户输入问题")
    table.add_row("st.chat_message", "聊天气泡", "展示 user 和 assistant 消息")
    table.add_row("st.session_state", "页面状态", "保存聊天记录")
    console.print(table)

    # 练习题答案：
    # 题目：Streamlit 页面为什么需要 st.session_state？
    # 如何添加：
    # 因为 Streamlit 每次交互都会重新运行脚本；
    # 普通变量会丢失，session_state 可以保存聊天记录和页面状态。


if __name__ == "__main__":
    main()
