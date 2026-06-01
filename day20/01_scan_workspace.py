"""Day 20 - 练习 1：扫描工作区。

练习目标：
理解 Coding Agent 的第一步不是写代码，而是先看清楚工作区结构。

参考答案：
创建 CodingAgent，调用 workspace_summary() 查看统计信息，再调用 scan_tree() 查看目录树。
"""

from __future__ import annotations

import os
import sys

# 把 day20 根目录加入模块搜索路径，保证直接运行脚本时导入稳定。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import WORKSPACE_DIR
from modules.coding_agent import CodingAgent

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 20 - 练习 1：扫描工作区", style="bold blue")
console.print("=" * 60, style="bold blue")

# 创建教学版 Coding Agent。
agent = CodingAgent(WORKSPACE_DIR)

# 输出工作区摘要，包括文件数量、总大小和部分文件预览。
console.print(agent.pretty_json(agent.workspace_summary()), style="green")
console.print("\n[bold cyan]目录树：[/bold cyan]")

# 输出简化目录树，帮助你快速理解项目结构。
for line in agent.scan_tree():
    console.print(line, style="yellow")
