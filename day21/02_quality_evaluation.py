"""Day 21 - 练习 2：项目质量评估。

练习目标：
学会用结构化指标检查 Day 19 和 Day 20 项目是否完整。

参考答案：
扫描目标项目后，使用 QualityEvaluator 评分并输出建议。
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import CURRENT_DIR, MAX_PREVIEW_CHARS, TARGET_PROJECTS
from modules.optimization_app import OptimizationApp


console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 21 - 练习 2：项目质量评估", style="bold blue")
console.print("=" * 60, style="bold blue")

app = OptimizationApp(CURRENT_DIR, TARGET_PROJECTS, "output")
results = app.evaluate(max_preview_chars=MAX_PREVIEW_CHARS)

for result in results:
    console.print(f"\n[bold cyan]项目：{result['project']}[/bold cyan]")
    console.print(f"评分：{result['score']}", style="green")
    console.print("优点：", result["findings"], style="yellow")
    console.print("建议：", result["suggestions"], style="magenta")
