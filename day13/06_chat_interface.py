"""Day 13 - 界面层：交互式命令行界面。

这个文件只负责和用户交互：
- 展示欢迎信息
- 展示命令菜单
- 接收输入
- 调用 SmartAgent
- 显示结果
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from modules.agent import SmartAgent
from modules.tools import all_tools

console = Console()


class ChatInterface:
    """交互式命令行界面。"""

    MODE_NAMES = {
        "chat": "普通对话",
        "tool": "工具增强",
        "parse": "输出解析",
    }

    def __init__(self):
        self.agent = SmartAgent()
        self.running = True

    def show_welcome(self):
        """显示欢迎信息。"""
        console.print(
            Panel.fit(
                "[bold]Day 13 - 综合 AI 助手[/bold]\n"
                "整合 LLM + Tools + Memory + 输出解析 + Agent\n"
                "支持：对话聊天、工具调用、结构化输出",
                style="bold green",
            )
        )

    def show_menu(self):
        """显示功能菜单。"""
        table = Table(title="功能菜单", show_header=True, header_style="bold magenta")
        table.add_column("命令", style="green", width=12)
        table.add_column("说明", style="white", width=30)
        table.add_row("chat", "切换到普通对话模式（默认）")
        table.add_row("tool", "切换到工具增强模式")
        table.add_row("parse", "切换到输出解析模式")
        table.add_row("mode", "查看当前模式")
        table.add_row("history", "查看对话历史")
        table.add_row("tools", "查看所有可用工具")
        table.add_row("clear", "清空对话历史")
        table.add_row("example", "查看示例问题")
        table.add_row("status", "查看系统状态")
        table.add_row("q", "退出程序")
        console.print(table)

    def show_tools(self):
        """显示工具列表。"""
        console.print("\n[bold cyan]可用工具：[/bold cyan]")
        for t in all_tools:
            desc = t.description.split("。")[0]
            console.print(f"  - {t.name}: {desc}", style="green")

    def show_examples(self):
        """显示示例问题。"""
        examples = [
            "chat 模式：你好，今天过得怎么样？",
            "tool 模式：帮我算一下 2 的 20 次方",
            "tool 模式：现在几点了？",
            "tool 模式：北京天气怎么样？",
            "parse 模式：请把这段需求整理成 JSON：我要做一个天气助手，需要支持北京、上海和深圳。",
            "parse 模式：把下面内容提炼成关键词和任务步骤：先收集数据，再清洗，再导出。",
        ]
        console.print("\n[bold cyan]示例问题：[/bold cyan]")
        for i, ex in enumerate(examples, 1):
            console.print(f"  {i}. {ex}", style="yellow")

    def show_status(self):
        """显示系统状态。"""
        stats = self.agent.memory.get_stats()
        console.print("\n[bold cyan]系统状态：[/bold cyan]")
        console.print(f"  当前模式：{self.MODE_NAMES.get(self.agent.current_mode, '未知')}", style="green")
        console.print(f"  历史消息：{stats['total_messages']} 条", style="green")
        console.print(f"  工具数量：{len(all_tools)} 个", style="green")
        console.print(
            f"  输出解析模块状态：{'可用' if self.agent.output_parser_available else '不可用'}",
            style="green",
        )

    def run(self):
        """运行主循环。"""
        self.show_welcome()
        self.show_menu()

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
            elif cmd == "chat":
                self.agent.switch_mode("chat")
                console.print(f"[dim]已切换到：{self.MODE_NAMES[self.agent.current_mode]}[/dim]")
                continue
            elif cmd == "tool":
                self.agent.switch_mode("tool")
                console.print(f"[dim]已切换到：{self.MODE_NAMES[self.agent.current_mode]}[/dim]")
                continue
            elif cmd == "parse":
                self.agent.switch_mode("parse")
                console.print(f"[dim]已切换到：{self.MODE_NAMES[self.agent.current_mode]}[/dim]")
                continue
            elif cmd == "mode":
                console.print(f"当前模式：[bold green]{self.MODE_NAMES[self.agent.current_mode]}[/bold green]")
                continue
            elif cmd == "tools":
                self.show_tools()
                continue
            elif cmd == "history":
                console.print(self.agent.get_history())
                continue
            elif cmd == "clear":
                self.agent.clear_memory()
                console.print("[dim]对话历史已清空[/dim]")
                continue
            elif cmd == "example":
                self.show_examples()
                continue
            elif cmd == "status":
                self.show_status()
                continue

            with console.status(f"[bold green]{self.MODE_NAMES[self.agent.current_mode]}模式处理中..."):
                if self.agent.current_mode == self.agent.MODE_TOOL:
                    response = self.agent.tool_mode(user_input)
                elif self.agent.current_mode == self.agent.MODE_PARSE:
                    response = self.agent.parse_mode(user_input)
                else:
                    response = self.agent.chat_mode(user_input)

            console.print(f"[bold green]助手：{response}[/bold green]")


if __name__ == "__main__":
    interface = ChatInterface()
    interface.run()
