"""Day 12 - 结构化输出演示程序。

这个入口文件负责：
1. 启动命令行界面
2. 接收用户输入
3. 调用结构化输出工作流
4. 把结果更清晰地打印出来
"""

import os
import sys

# 允许直接运行这个文件时，仍然能导入同目录下的 modules、schemas 等包。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from modules.demo_workflow import StructuredOutputWorkflow


console = Console()


class OutputParseApp:
    """Day 12 的命令行演示应用。"""

    def __init__(self):
        # 这里初始化工作流对象，后面所有命令都会调用它。
        self.workflow = StructuredOutputWorkflow()
        self.running = True

    def show_banner(self):
        """显示欢迎横幅。"""
        console.print(
            Panel.fit(
                "[bold]Day 12 - 输出解析[/bold]\n"
                "命令：intent / extract / resume / demo / q\n"
                "示例：\n"
                "  intent 帮我查一下北京天气\n"
                "  extract 这段文本请提取摘要和关键词\n"
                "  resume 我叫张三，本科毕业，擅长 Python 和 AI 开发",
                style="bold blue",
            )
        )

    def show_menu(self):
        """把可用命令整理成表格，方便查看。"""
        table = Table(title="命令菜单", show_header=True, header_style="bold magenta")
        table.add_column("命令", width=12)
        table.add_column("说明", width=50)
        table.add_row("intent", "进行意图分类输出")
        table.add_row("extract", "进行结构化信息抽取")
        table.add_row("resume", "进行简历信息抽取")
        table.add_row("demo", "运行内置演示样例")
        table.add_row("q", "退出程序")
        console.print(table)

    def _render_result(self, result: dict):
        """把工作流返回的字典格式结果，转成更好读的中文输出。"""
        if result["ok"]:
            console.print("[bold green]解析成功[/bold green]")
            console.print(f"模式：{result['schema']}")
            console.print(f"尝试次数：{result['attempts']}")
            console.print(f"模型原始输出：{result['raw_output']}")
            console.print(f"解析后的数据：{result['parsed']}")
        else:
            console.print("[bold red]解析失败[/bold red]")
            console.print(f"模式：{result['schema']}")
            console.print(f"尝试次数：{result['attempts']}")
            console.print(f"模型原始输出：{result['raw_output']}")
            console.print(f"错误信息：{result['validation_errors']}")

    def run_demo(self):
        """运行几组预设示例，方便一次性观察完整流程。"""
        examples = [
            ("intent", "帮我查一下北京天气"),
            ("extract", "这段文本请提取摘要和关键词，内容是 Python 是一门非常适合 AI 开发的语言。"),
            ("resume", "我叫张三，本科毕业于某大学，擅长 Python 和 AI 开发。"),
        ]

        for task, text in examples:
            console.print(f"\n[bold cyan]{task}[/bold cyan] -> {text}")
            result = self.workflow.run(task, text)
            self._render_result(result)

    def run(self):
        """主循环：持续接收用户输入，直到用户退出。"""
        self.show_banner()
        self.show_menu()

        while self.running:
            try:
                user_input = Prompt.ask("\n请输入命令和文本")
            except (EOFError, KeyboardInterrupt):
                console.print("\n再见！", style="bold red")
                break

            if not user_input:
                continue

            command = user_input.strip().lower()
            if command == "q":
                console.print("再见！", style="bold red")
                break
            if command == "demo":
                self.run_demo()
                continue

            # 用户输入格式：命令 + 空格 + 文本
            parts = user_input.split(" ", 1)
            if len(parts) == 1:
                console.print("请输入命令加文本，例如：intent 帮我查一下北京天气", style="yellow")
                continue

            task, text = parts[0], parts[1]
            result = self.workflow.run(task, text)
            self._render_result(result)


if __name__ == "__main__":
    OutputParseApp().run()
