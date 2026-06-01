"""Day 21 - 完整演示：项目优化与调试应用。

这个文件把扫描、评分、提示词优化、功能规划、UX 评审和报告保存串成完整流程。
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from config import CURRENT_DIR, MAX_PREVIEW_CHARS, REPORT_DIR, TARGET_PROJECTS
from modules.optimization_app import OptimizationApp


console = Console()


class Day21App:
    """Day 21 命令行应用。"""

    def __init__(self):
        self.app = OptimizationApp(CURRENT_DIR, TARGET_PROJECTS, REPORT_DIR)
        self.last_report: dict | None = None

    def show_welcome(self):
        """显示欢迎信息。"""
        console.print(
            Panel.fit(
                "[bold]Day 21 - 项目优化与调试[/bold]\n"
                "本日重点：优化提示词、提升准确率、增加功能、优化用户体验。",
                style="bold green",
            )
        )

    def show_menu(self):
        """显示菜单。"""
        table = Table(title="功能菜单", show_header=True, header_style="bold magenta")
        table.add_column("命令", width=12)
        table.add_column("说明", width=60)
        table.add_row("scan", "扫描 Day 19 / Day 20 项目")
        table.add_row("quality", "项目质量评分")
        table.add_row("prompt", "优化一个提示词")
        table.add_row("features", "生成后续功能清单")
        table.add_row("ux", "生成用户体验评审")
        table.add_row("report", "生成完整优化报告")
        table.add_row("save", "保存最近一次完整报告到 output/")
        table.add_row("q", "退出")
        console.print(table)

    def run(self):
        """运行主循环。"""
        self.show_welcome()
        self.show_menu()

        while True:
            try:
                command = Prompt.ask("\n请输入命令").strip().lower()
            except (EOFError, KeyboardInterrupt):
                console.print("\n再见！", style="bold red")
                break

            if command == "q":
                console.print("再见！", style="bold red")
                break
            if command == "scan":
                console.print(self.app.scan(MAX_PREVIEW_CHARS), style="green")
            elif command == "quality":
                console.print(self.app.evaluate(MAX_PREVIEW_CHARS), style="green")
            elif command == "prompt":
                prompt = Prompt.ask("请输入要评估的提示词", default="帮我优化项目，输出建议")
                console.print(self.app.prompt_review(prompt, task_name="项目优化"), style="green")
            elif command == "features":
                console.print(self.app.feature_plan(), style="green")
            elif command == "ux":
                console.print(self.app.ux_review(MAX_PREVIEW_CHARS), style="green")
            elif command == "report":
                self.last_report = self.app.full_report(MAX_PREVIEW_CHARS)
                console.print(self.last_report, style="green")
            elif command == "save":
                if self.last_report is None:
                    self.last_report = self.app.full_report(MAX_PREVIEW_CHARS)
                path = self.app.save_report(self.last_report)
                console.print(f"已保存：{path}", style="green")
            else:
                console.print("未知命令，请输入 scan / quality / prompt / features / ux / report / save / q", style="yellow")


if __name__ == "__main__":
    Day21App().run()
