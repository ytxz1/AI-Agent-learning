"""Day 20 - 练习 1：扫描工作区。"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import WORKSPACE_DIR
from modules.coding_agent import CodingAgent

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 20 - 练习 1：扫描工作区", style="bold blue")
console.print("=" * 60, style="bold blue")

agent = CodingAgent(WORKSPACE_DIR)
console.print(agent.pretty_json(agent.workspace_summary()), style="green")
console.print("\n[bold cyan]目录树：[/bold cyan]")
for line in agent.scan_tree():
    console.print(line, style="yellow")

