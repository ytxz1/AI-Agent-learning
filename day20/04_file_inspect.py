"""Day 20 - 练习 4：查看文件。

练习目标：
理解 Coding Agent 如何安全读取工作区内的指定文件。

参考答案：
调用 inspect("main.py") 获取文件路径、大小和内容预览。
"""

from __future__ import annotations

import os
import sys

# 支持直接运行当前文件。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import MAX_FILE_PREVIEW_CHARS, WORKSPACE_DIR
from modules.coding_agent import CodingAgent

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 20 - 练习 4：查看文件", style="bold blue")
console.print("=" * 60, style="bold blue")

# 创建 Agent 并查看 main.py。
agent = CodingAgent(WORKSPACE_DIR)
preview = agent.inspect("main.py", max_chars=MAX_FILE_PREVIEW_CHARS)
console.print(agent.pretty_json(preview), style="green")
