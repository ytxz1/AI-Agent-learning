"""Day 20 - 练习 4：查看文件。"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import MAX_FILE_PREVIEW_CHARS, WORKSPACE_DIR
from modules.coding_agent import CodingAgent

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 20 - 练习 4：查看文件", style="bold blue")
console.print("=" * 60, style="bold blue")

agent = CodingAgent(WORKSPACE_DIR)
preview = agent.inspect("main.py", max_chars=MAX_FILE_PREVIEW_CHARS)
console.print(agent.pretty_json(preview), style="green")

