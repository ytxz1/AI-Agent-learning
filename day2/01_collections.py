"""Day 2 - 练习 1：列表、字典、集合。"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from config import STUDENTS_JSON
from modules.collections_tools import collect_all_tags, group_students_by_level, sort_students_by_average
from modules.json_tools import load_json
from modules.student import Student


console = Console()

raw_students = load_json(STUDENTS_JSON)
students = [Student.from_dict(item) for item in raw_students]

table = Table(title="按平均分排序", show_header=True)
table.add_column("姓名", style="cyan")
table.add_column("平均分", style="green")
table.add_column("等级", style="yellow")
table.add_column("标签", style="white")

for student in sort_students_by_average(students):
    table.add_row(student.name, str(student.average_score()), student.level(), ", ".join(student.tags))

console.print(table)
console.print("\n[bold cyan]按等级分组：[/bold cyan]")
console.print(group_students_by_level(students), style="green")
console.print("\n[bold cyan]所有标签（set 去重）：[/bold cyan]")
console.print(sorted(collect_all_tags(students)), style="yellow")

