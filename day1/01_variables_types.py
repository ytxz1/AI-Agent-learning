"""Day 1 - 练习 1：变量和数据类型。"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from modules.basics import build_profile, format_profile


console = Console()

name = "小明"
age = 20
height = 1.75
is_student = True
skills = ["Python", "AI", "写作"]
profile = build_profile(name, age, skills)

table = Table(title="变量和数据类型", show_header=True)
table.add_column("变量名", style="cyan")
table.add_column("值", style="green")
table.add_column("类型", style="yellow")

for variable_name, value in [
    ("name", name),
    ("age", age),
    ("height", height),
    ("is_student", is_student),
    ("skills", skills),
    ("profile", profile),
]:
    table.add_row(variable_name, str(value), type(value).__name__)

console.print(table)
console.print("\n[bold cyan]格式化后的个人信息：[/bold cyan]")
console.print(format_profile(profile), style="green")

