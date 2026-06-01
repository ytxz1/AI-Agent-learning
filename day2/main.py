"""Day 2 主入口：Python 进阶交互练习。"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from config import STUDENTS_JSON
from modules.api_tools import fetch_python_repo_info
from modules.collections_tools import collect_all_tags, group_students_by_level, sort_students_by_average
from modules.json_tools import load_json
from modules.student import Student


console = Console()


def load_students() -> list[Student]:
    """加载学生列表。"""
    return [Student.from_dict(item) for item in load_json(STUDENTS_JSON)]


def show_menu() -> None:
    """显示菜单。"""
    table = Table(title="Day 2 功能菜单", show_header=True, header_style="bold magenta")
    table.add_column("命令", style="cyan", width=14)
    table.add_column("说明", style="white", width=48)
    table.add_row("list", "查看学生平均分排行")
    table.add_row("group", "按等级给学生分组")
    table.add_row("tags", "查看所有标签（set 去重）")
    table.add_row("api", "演示 requests 在线优先、本地兜底")
    table.add_row("q", "退出")
    console.print(table)


def show_students(students: list[Student]) -> None:
    """展示学生排行。"""
    table = Table(title="学生平均分排行", show_header=True)
    table.add_column("姓名", style="cyan")
    table.add_column("平均分", style="green")
    table.add_column("等级", style="yellow")
    for student in sort_students_by_average(students):
        table.add_row(student.name, str(student.average_score()), student.level())
    console.print(table)


def main() -> None:
    console.print(
        Panel.fit(
            "[bold]Day 2 - Python 进阶[/bold]\n列表、字典、集合、类和对象、异常处理、常用库",
            style="bold green",
        )
    )
    students = load_students()
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
        if command == "list":
            show_students(students)
        elif command == "group":
            console.print(group_students_by_level(students), style="green")
        elif command == "tags":
            console.print(sorted(collect_all_tags(students)), style="yellow")
        elif command == "api":
            console.print(fetch_python_repo_info(), style="green")
        else:
            console.print("未知命令，请输入 list / group / tags / api / q", style="yellow")


if __name__ == "__main__":
    main()

