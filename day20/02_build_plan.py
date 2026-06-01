"""Day 20 - 练习 2：生成修改计划。

练习目标：
理解 Coding Agent 如何把自然语言需求拆解成结构化计划。

参考答案：
调用 generate_plan()，传入用户需求和重点文件，输出 JSON 计划。
"""

from __future__ import annotations

import os
import sys

# 支持直接运行当前文件。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import WORKSPACE_DIR
from modules.coding_agent import CodingAgent

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 20 - 练习 2：生成修改计划", style="bold blue")
console.print("=" * 60, style="bold blue")

# 创建 Agent 后，请求它生成计划。
agent = CodingAgent(WORKSPACE_DIR)

# focus_files 告诉 Agent 优先关注哪些文件。
plan = agent.generate_plan("给这个项目增加一个 help 命令，并保留现有菜单结构", focus_files=["main.py", "05_full_coding_agent.py"])
console.print(agent.pretty_json(plan), style="green")
