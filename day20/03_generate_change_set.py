"""Day 20 - 练习 3：生成代码草案。

练习目标：
理解“计划”和“代码草案”的区别。

参考答案：
调用 generate_change_set()，让 Agent 基于需求和工作区上下文生成可审阅的 change set。
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
console.print("Day 20 - 练习 3：生成代码草案", style="bold blue")
console.print("=" * 60, style="bold blue")

# 创建 Agent，然后生成代码草案。
agent = CodingAgent(WORKSPACE_DIR)

# 注意：这里不会直接修改真实文件，只会输出结构化草案。
change_set = agent.generate_change_set("给这个项目增加一个 help 命令，并保留现有菜单结构", focus_files=["main.py"])
console.print(agent.pretty_json(change_set), style="green")
