"""Day 1 - 练习 3：函数和模块。"""

from __future__ import annotations

from rich.console import Console

from modules.basics import build_profile, count_words, format_profile


console = Console()

profile = build_profile("小红", 22, ["Python", "LangChain", "FastAPI"])
console.print("[bold cyan]调用模块函数生成个人信息：[/bold cyan]")
console.print(format_profile(profile), style="green")

text = "python ai python agent tools python memory agent"
console.print("\n[bold cyan]单词频率统计：[/bold cyan]")
for word, count in count_words(text):
    console.print(f"{word}: {count}", style="yellow")

console.print("\n这个文件的重点是：把可复用逻辑放到 modules/ 里，再通过 import 调用。", style="green")

