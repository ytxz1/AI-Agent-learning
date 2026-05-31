"""Day 20 - 练习 2：生成修改计划。"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import WORKSPACE_DIR
from modules.coding_agent import CodingAgent

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 20 - 练习 2：生成修改计划", style="bold blue")
console.print("=" * 60, style="bold blue")

agent = CodingAgent(WORKSPACE_DIR)
plan = agent.generate_plan("给这个项目增加一个 help 命令，并保留现有菜单结构", focus_files=["main.py", "05_full_coding_agent.py"])
console.print(agent.pretty_json(plan), style="green")

