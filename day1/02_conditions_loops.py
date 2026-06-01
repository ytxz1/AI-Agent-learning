"""Day 1 - 练习 2：条件判断和循环。"""

from __future__ import annotations

from rich.console import Console

from modules.basics import calculate_grade, filter_even_numbers, multiplication_table


console = Console()

scores = [95, 82, 76, 61, 48, 101]
console.print("=" * 60, style="bold blue")
console.print("成绩等级判断", style="bold blue")
console.print("=" * 60, style="bold blue")

for score in scores:
    console.print(f"分数：{score} -> 等级：{calculate_grade(score)}", style="green")

numbers = list(range(1, 21))
console.print("\n[bold cyan]1 到 20 之间的偶数：[/bold cyan]")
console.print(filter_even_numbers(numbers), style="yellow")

console.print("\n[bold cyan]九九乘法表：[/bold cyan]")
for row in multiplication_table():
    console.print(row, style="green")

