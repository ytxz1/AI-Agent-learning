"""Day 21 - 练习 1：优化提示词。

练习目标：
学会检查一个提示词是否包含角色、上下文、任务、约束和输出格式。

参考答案：
使用 PromptOptimizer.review() 对示例提示词评分，并生成更稳的优化模板。
"""

from __future__ import annotations

import os
import sys

# 支持直接运行当前文件。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from modules.prompt_optimizer import PromptOptimizer


console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 21 - 练习 1：优化提示词", style="bold blue")
console.print("=" * 60, style="bold blue")

# 这个提示词故意写得比较粗糙，方便观察优化器如何发现问题。
bad_prompt = "帮我优化项目，输出建议。"

optimizer = PromptOptimizer()
review = optimizer.review(bad_prompt, task_name="优化 RAG 问答系统")

console.print("\n[bold cyan]原始提示词：[/bold cyan]")
console.print(bad_prompt, style="yellow")
console.print("\n[bold cyan]评估结果：[/bold cyan]")
console.print(review, style="green")
console.print("\n[bold cyan]优化后的提示词模板：[/bold cyan]")
console.print(review.improved_prompt, style="magenta")
