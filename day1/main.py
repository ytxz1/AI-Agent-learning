"""Day 1 主入口：Python 基础交互练习。"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from modules.basics import build_profile, calculate_grade, filter_even_numbers, format_profile
from modules.file_tools import read_text_file, summarize_text_file
from config import SAMPLE_NOTES_FILE


console = Console()


def show_menu() -> None:
    """显示菜单。"""
    table = Table(title="Day 1 功能菜单", show_header=True, header_style="bold magenta")
    table.add_column("命令", style="cyan", width=14)
    table.add_column("说明", style="white", width=44)
    table.add_row("profile", "演示变量、列表和字典")
    table.add_row("grade", "输入分数并判断等级")
    table.add_row("even", "筛选 1 到 30 的偶数")
    table.add_row("file", "读取并统计 sample_notes.txt")
    table.add_row("q", "退出")
    console.print(table)


def run_profile_demo() -> None:
    """变量和数据结构演示。"""
    profile = build_profile("学习者", 18, ["Python", "API", "Agent"])
    console.print(format_profile(profile), style="green")


def run_grade_demo() -> None:
    """成绩判断演示。"""
    raw = Prompt.ask("请输入一个 0-100 的分数", default="85")
    try:
        score = float(raw)
    except ValueError:
        console.print("输入不是数字。", style="red")
        return
    console.print(f"等级：{calculate_grade(score)}", style="green")


def run_even_demo() -> None:
    """循环和列表推导式演示。"""
    console.print(filter_even_numbers(range(1, 31)), style="yellow")


def run_file_demo() -> None:
    """文件读取和统计演示。"""
    text = read_text_file(SAMPLE_NOTES_FILE)
    summary = summarize_text_file(SAMPLE_NOTES_FILE)
    console.print(text, style="green")
    console.print(summary, style="yellow")


def main() -> None:
    console.print(
        Panel.fit(
            "[bold]Day 1 - Python 基础[/bold]\n变量、数据类型、条件、循环、函数、模块、文件操作",
            style="bold green",
        )
    )
    show_menu()

    while True:
        try:
            command = Prompt.ask("\n请输入命令").strip().lower()
        except (EOFError, KeyboardInterrupt):
            console.print("\n再见！", style="bold red")
            break

        if command == "q":
            console.print("再见！", style="bold red")
            break
        if command == "profile":
            run_profile_demo()
        elif command == "grade":
            run_grade_demo()
        elif command == "even":
            run_even_demo()
        elif command == "file":
            run_file_demo()
        else:
            console.print("未知命令，请输入 profile / grade / even / file / q", style="yellow")


if __name__ == "__main__":
    main()

