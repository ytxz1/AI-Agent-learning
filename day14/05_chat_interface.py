"""Day 14 - 05 交互式命令行界面

运行：
    python main.py
或者：
    python 05_chat_interface.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from modules.agent import ToolAgent


console = Console()


class ChatInterface:
    MODE_NAMES = {
        "chat": "普通聊天",
        "tool": "工具调用",
        "auto": "自动判断",
    }

    def __init__(self):
        self.agent = ToolAgent()
        self.running = True

    def show_welcome(self):
        console.print(
            Panel.fit(
                "[bold]Day 14 - 工具调用 Agent[/bold]\n"
                "支持：聊天 / 计算 / 天气 / 翻译 / 时间 / 单位换算\n"
                "命令：chat, tool, auto, tools, history, clear, status, q",
                style="bold blue",
            )
        )

    def show_menu(self):
        table = Table(title="命令菜单", show_header=True, header_style="bold magenta")
        table.add_column("命令", style="green", width=12)
        table.add_column("说明", style="white", width=50)
        table.add_row("chat", "切换到普通聊天模式")
        table.add_row("tool", "切换到工具调用模式")
        table.add_row("auto", "自动判断是否需要工具")
        table.add_row("tools", "查看所有可用工具")
        table.add_row("history", "查看对话历史")
        table.add_row("clear", "清空对话历史")
        table.add_row("status", "查看系统状态")
        table.add_row("q", "退出程序")
        console.print(table)

    def show_tools(self):
        console.print("\n[bold cyan]可用工具[/bold cyan]")
        for item in self.agent.tools:
            console.print(f"- {item.name}: {item.description.splitlines()[0]}")

    def show_examples(self):
        examples = [
            "帮我算一下 2 + 3 * 4",
            "北京今天天气怎么样？",
            "把“你好”翻译成英文",
            "现在几点了？",
            "把 25 摄氏度换成华氏度",
        ]
        console.print("\n[bold cyan]示例问题[/bold cyan]")
        for idx, item in enumerate(examples, 1):
            console.print(f"{idx}. {item}")

    def show_status(self):
        status = self.agent.get_status()
        console.print("\n[bold cyan]系统状态[/bold cyan]")
        console.print(f"当前模式：{self.MODE_NAMES.get(status.mode, status.mode)}")
        console.print(f"API 可用：{'是' if status.api_available else '否'}")
        console.print(f"工具数量：{status.tool_count}")
        console.print(f"历史消息：{status.history_count}")

    def run(self):
        self.show_welcome()
        self.show_menu()
        self.show_examples()
        console.print(f"\n[dim]当前模式：{self.MODE_NAMES[self.agent.current_mode]}[/dim]")

        while self.running:
            try:
                user_input = Prompt.ask("\n你")
            except (EOFError, KeyboardInterrupt):
                console.print("\n再见！", style="bold red")
                break

            if not user_input:
                continue

            cmd = user_input.strip().lower()

            if cmd == "q":
                console.print("再见！", style="bold red")
                break
            if cmd in {"chat", "tool", "auto"}:
                result = self.agent.switch_mode(cmd)
                console.print(result, style="dim green")
                continue
            if cmd == "tools":
                self.show_tools()
                continue
            if cmd == "history":
                console.print(self.agent.get_history())
                continue
            if cmd == "clear":
                console.print(self.agent.clear_history(), style="dim yellow")
                continue
            if cmd == "status":
                self.show_status()
                continue
            if cmd == "help":
                self.show_menu()
                continue

            with console.status("[bold green]处理中..."):
                if self.agent.current_mode == self.agent.MODE_CHAT:
                    response = self.agent.chat_mode(user_input)
                elif self.agent.current_mode == self.agent.MODE_TOOL:
                    response = self.agent.tool_mode(user_input)
                else:
                    response = self.agent.auto_mode(user_input)

            console.print(f"[bold green]助手：{response}[/bold green]")


if __name__ == "__main__":
    ChatInterface().run()

