"""Day 21 - 练习 3：增加功能清单。

练习目标：
给 Day 19 和 Day 20 生成后续可以增加的功能 backlog。

参考答案：
使用 FeaturePlanner 根据项目类型输出功能建议和优先级。
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.table import Table

from config import CURRENT_DIR, TARGET_PROJECTS
from modules.optimization_app import OptimizationApp


console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 21 - 练习 3：增加功能清单", style="bold blue")
console.print("=" * 60, style="bold blue")

app = OptimizationApp(CURRENT_DIR, TARGET_PROJECTS, "output")
plans = app.feature_plan()

for plan in plans:
    table = Table(title=f"{plan['project']} 功能优化清单", show_header=True)
    table.add_column("ID", style="cyan", width=6)
    table.add_column("优先级", style="yellow", width=10)
    table.add_column("功能", style="green")
    for item in plan["features"]:
        table.add_row(str(item["id"]), item["priority"], item["title"])
    console.print(table)
