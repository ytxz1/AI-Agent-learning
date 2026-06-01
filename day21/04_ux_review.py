"""Day 21 - 练习 4：用户体验评审。

练习目标：
检查项目命令行体验是否足够清楚、是否有菜单、示例和结果保存能力。

参考答案：
使用 UXReviewer 对目标项目生成 positives 和 suggestions。
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
console.print("Day 21 - 练习 4：用户体验评审", style="bold blue")
console.print("=" * 60, style="bold blue")

app = OptimizationApp(CURRENT_DIR, TARGET_PROJECTS, "output")
reviews = app.ux_review(max_preview_chars=MAX_PREVIEW_CHARS)

for review in reviews:
    console.print(f"\n[bold cyan]项目：{review['project']}[/bold cyan]")
    console.print("做得好的地方：", review["positives"], style="green")
    console.print("可以优化的地方：", review["suggestions"], style="yellow")
