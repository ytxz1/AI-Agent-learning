"""练习 02：构建简单界面结构。

这个脚本用文字方式拆解 Day25 页面布局：
- 顶部 Hero 区；
- 侧边栏控制面板；
- 主区域聊天窗口；
- 底部输入框。
"""

from __future__ import annotations

from rich.console import Console


console = Console()


def main() -> None:
    """打印页面结构说明。"""

    console.rule("[bold green]练习 02：构建简单界面")
    console.print("Day25 页面结构：")
    console.print("1. 顶部 Hero：展示标题、主题和学习目标。")
    console.print("2. 侧边栏：选择 local/api 模式，填写 API 地址。")
    console.print("3. 主区域：展示聊天记录。")
    console.print("4. 输入框：通过 st.chat_input 接收用户问题。")
    console.print("5. 状态卡片：显示当前模式、API 地址、消息数量。")

    # 练习题答案：
    # 题目：如何在侧边栏添加一个“清空聊天记录”按钮？
    # 如何添加：
    # 在 with st.sidebar: 中写 if st.button('清空聊天记录'): store.clear(); st.rerun()


if __name__ == "__main__":
    main()
