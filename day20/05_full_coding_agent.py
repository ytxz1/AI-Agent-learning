"""Day 20 - 完整演示：Coding Agent。"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from config import DEFAULT_TOP_N, MAX_FILE_PREVIEW_CHARS, MAX_FILES_PREVIEW, WORKSPACE_DIR
from modules.coding_agent import CodingAgent

console = Console()


class CodingAgentApp:
    """命令行版 Coding Agent 应用。"""

    def __init__(self):
        self.agent = CodingAgent(WORKSPACE_DIR)
        self.running = True
        self.last_plan = None
        self.last_change_set = None

    def show_welcome(self):
        console.print(
            Panel.fit(
                "[bold]Day 20 - Coding Agent[/bold]\n"
                "本日重点：理解代码、生成计划、生成草案、做验证建议。\n"
                f"工作区：{self.agent.workspace.root}",
                style="bold green",
            )
        )

    def show_menu(self):
        table = Table(title="功能菜单", show_header=True, header_style="bold magenta")
        table.add_column("命令", width=14)
        table.add_column("说明", width=60)
        table.add_row("scan", "扫描工作区并查看摘要")
        table.add_row("files", "查看常见文件预览")
        table.add_row("inspect", "查看指定文件内容")
        table.add_row("plan", "生成修改计划")
        table.add_row("draft", "生成代码草案")
        table.add_row("demo", "运行示例请求")
        table.add_row("save", "把最近一次计划/草案保存到 output/")
        table.add_row("q", "退出程序")
        console.print(table)

    def show_scan(self):
        summary = self.agent.workspace_summary()
        console.print("\n[bold cyan]工作区摘要[/bold cyan]")
        console.print(self.agent.pretty_json(summary), style="green")
        console.print("\n[bold cyan]目录树[/bold cyan]")
        for line in self.agent.scan_tree():
            console.print(line, style="yellow")

    def show_files(self):
        files = self.agent.workspace.summarize_files(max_files=MAX_FILES_PREVIEW, max_chars=MAX_FILE_PREVIEW_CHARS)
        console.print("\n[bold cyan]文件预览[/bold cyan]")
        for item in files:
            console.print(f"\n[bold]路径：{item.path}[/bold]")
            console.print(f"大小：{item.size}")
            console.print(item.preview, style="yellow")

    def inspect_file(self):
        relative_path = Prompt.ask("请输入要查看的文件路径", default="main.py")
        try:
            preview = self.agent.inspect(relative_path, max_chars=MAX_FILE_PREVIEW_CHARS)
            console.print(self.agent.pretty_json(preview), style="green")
        except Exception as exc:
            console.print(f"查看失败：{exc}", style="red")

    def build_plan(self):
        request = Prompt.ask("请输入 Coding 需求", default="给这个项目增加一个 help 命令，并保留现有菜单结构")
        files_input = Prompt.ask("请输入重点文件（逗号分隔）", default="main.py")
        focus_files = [item.strip() for item in files_input.split(",") if item.strip()]
        plan = self.agent.generate_plan(request, focus_files=focus_files)
        self.last_plan = plan
        console.print("\n[bold cyan]修改计划[/bold cyan]")
        console.print(self.agent.pretty_json(plan), style="green")

    def build_change_set(self):
        request = Prompt.ask("请输入 Coding 需求", default="给这个项目增加一个 help 命令，并保留现有菜单结构")
        files_input = Prompt.ask("请输入重点文件（逗号分隔）", default="main.py")
        focus_files = [item.strip() for item in files_input.split(",") if item.strip()]
        if self.last_plan is None:
            self.last_plan = self.agent.generate_plan(request, focus_files=focus_files)
        change_set = self.agent.generate_change_set(request, focus_files=focus_files)
        self.last_change_set = change_set
        console.print("\n[bold cyan]代码草案[/bold cyan]")
        console.print(self.agent.pretty_json(change_set), style="green")

    def run_demo(self):
        examples = [
            "给这个项目增加一个 help 命令，并保留现有菜单结构",
            "帮我修复一个文件读取路径错误的问题",
            "请给这个项目补充一个单元测试建议",
        ]
        for request in examples:
            console.print(f"\n[bold cyan]请求：{request}[/bold cyan]")
            plan = self.agent.generate_plan(request, focus_files=["main.py"])
            change_set = self.agent.generate_change_set(request, focus_files=["main.py"])
            console.print("[bold yellow]计划：[/bold yellow]")
            console.print(self.agent.pretty_json(plan), style="yellow")
            console.print("[bold green]草案：[/bold green]")
            console.print(self.agent.pretty_json(change_set), style="green")

    def save_outputs(self):
        output_dir = self.agent.workspace.root / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        if self.last_plan is not None:
            (output_dir / "last_plan.json").write_text(
                self.agent.pretty_json(self.last_plan),
                encoding="utf-8",
            )
        if self.last_change_set is not None:
            (output_dir / "last_change_set.json").write_text(
                self.agent.pretty_json(self.last_change_set),
                encoding="utf-8",
            )
        console.print(f"已保存到：{output_dir}", style="green")

    def run(self):
        self.show_welcome()
        self.show_menu()
        console.print(f"\n[dim]当前默认展示数量：{DEFAULT_TOP_N}[/dim]")

        while self.running:
            try:
                cmd = Prompt.ask("\n请输入命令").strip().lower()
            except (EOFError, KeyboardInterrupt):
                console.print("\n再见！", style="bold red")
                break

            if cmd == "q":
                console.print("再见！", style="bold red")
                break
            if cmd == "scan":
                self.show_scan()
            elif cmd == "files":
                self.show_files()
            elif cmd == "inspect":
                self.inspect_file()
            elif cmd == "plan":
                self.build_plan()
            elif cmd == "draft":
                self.build_change_set()
            elif cmd == "demo":
                self.run_demo()
            elif cmd == "save":
                self.save_outputs()
            else:
                console.print("未知命令，请重新输入。", style="yellow")


if __name__ == "__main__":
    CodingAgentApp().run()

