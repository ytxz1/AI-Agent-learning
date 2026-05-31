"""
Day 13 - 界面层：交互式命令行界面

整合所有模块，提供用户交互界面。
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.agent import SmartAgent
from modules.tools import all_tools
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()


class ChatInterface:
    """交互式命令行界面"""

    MODE_NAMES = {"chat": "普通对话", "tool": "工具增强", "rag": "文档问答"}

    def __init__(self):
        self.agent = SmartAgent()
        self.running = True

    def show_welcome(self):
        """显示欢迎界面"""
        console.print(Panel.fit(
            "[bold]Day 13 - 综合 AI 助手[/bold]\n"
            "整合 LLM + Tools + Memory + RAG + Agent\n"
            "支持：对话聊天、工具调用、文档问答",
            style="bold green"
        ))

    def show_menu(self):
        """显示功能菜单"""
        table = Table(title="功能菜单", show_header=True, header_style="bold magenta")
        table.add_column("命令", style="green", width=12)
        table.add_column("说明", style="white", width=30)
        table.add_row("chat", "切换到普通对话模式（默认）")
        table.add_row("tool", "切换到工具增强模式")
        table.add_row("rag", "切换到文档问答模式")
        table.add_row("mode", "查看当前模式")
        table.add_row("history", "查看对话历史")
        table.add_row("tools", "查看所有可用工具")
        table.add_row("clear", "清空对话历史")
        table.add_row("example", "查看示例问题")
        table.add_row("status", "查看系统状态")
        table.add_row("q", "退出程序")
        console.print(table)

    def show_tools(self):
        """显示工具列表"""
        console.print("\n[bold cyan]可用工具：[/bold cyan]")
        for t in all_tools:
            desc = t.description.split("。")[0]
            console.print(f"  - {t.name}: {desc}", style="green")

    def show_examples(self):
        """显示示例问题"""
        examples = [
            "chat 模式：你好！/ 今天心情怎么样？",
            "tool 模式：帮我算一下 2 的 20 次方",
            "tool 模式：北京天气怎么样？",
            "tool 模式：现在几点了？",
            "tool 模式：把 25 摄氏度转换成华氏度",
            "tool 模式：什么是机器学习？",
            "rag 模式：Python 有什么特点？",
            "rag 模式：AI 的核心技术有哪些？",
        ]
        console.print("\n[bold cyan]示例问题：[/bold cyan]")
        for i, ex in enumerate(examples, 1):
            console.print(f"  {i}. {ex}", style="yellow")

    def show_status(self):
        """显示系统状态"""
        stats = self.agent.memory.get_stats()
        console.print("\n[bold cyan]系统状态：[/bold cyan]")
        console.print(f"  当前模式：{self.MODE_NAMES.get(self.agent.current_mode, '未知')}", style="green")
        console.print(f"  历史消息：{stats['total_messages']} 条", style="green")
        console.print(f"  工具数量：{len(all_tools)} 个", style="green")
        console.print(f"  RAG 状态：{'可用' if self.agent.rag_available else '不可用'}", style="green")

    def run(self):
        """运行主循环"""
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

            # 命令处理
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
            elif cmd == "rag":
                self.agent.switch_mode("rag")
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

            # 处理用户输入
            with console.status(f"[bold green]{self.MODE_NAMES[self.agent.current_mode]}模式处理中..."):
                if self.agent.current_mode == self.agent.MODE_TOOL:
                    response = self.agent.tool_mode(user_input)
                elif self.agent.current_mode == self.agent.MODE_RAG:
                    response = self.agent.rag_mode(user_input)
                else:
                    response = self.agent.chat_mode(user_input)

            console.print(f"[bold green]助手：{response}[/bold green]")


if __name__ == "__main__":
    interface = ChatInterface()
    interface.run()
