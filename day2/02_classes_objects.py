"""Day 2 - 练习 2：类和对象。"""

from __future__ import annotations

from rich.console import Console

from modules.student import Student


console = Console()

student = Student(
    id=100,
    name="测试学生",
    age=18,
    scores={"python": 96, "math": 88, "english": 91},
    tags=["python", "class", "object"],
)

console.print("=" * 60, style="bold blue")
console.print("类和对象演示", style="bold blue")
console.print("=" * 60, style="bold blue")
console.print(f"对象：{student}", style="green")
console.print(f"平均分：{student.average_score()}", style="yellow")
console.print(f"等级：{student.level()}", style="yellow")
console.print(f"是否有 python 标签：{student.has_tag('python')}", style="cyan")
console.print("\n[bold cyan]转换成字典：[/bold cyan]")
console.print(student.to_dict(), style="green")

