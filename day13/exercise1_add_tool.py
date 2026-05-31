"""
Day 13 - 练习 1（基础）：添加新工具

任务：给 Agent 添加一个新工具（获取随机数），并验证是否可用。

新增内容（标注 [新增]）：
  1. [新增] random_number 工具定义
  2. [新增] 在 Agent 中注册并使用
"""

import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_core.tools import tool
from rich.console import Console

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 13 - 练习 1：添加新工具", style="bold blue")
console.print("=" * 60, style="bold blue")

# [新增] 随机数工具
@tool
def random_number(min_value: int = 1, max_value: int = 100) -> str:
    """生成一个随机整数。当用户需要随机数时使用此工具。
    参数: min_value - 最小值（默认1）, max_value - 最大值（默认100）"""
    result = random.randint(min_value, max_value)
    return f"随机数：{result}（范围 {min_value}-{max_value}）"

# [新增] 注册到工具列表
from modules.tools import all_tools, tool_map
all_tools.append(random_number)
tool_map[random_number.name] = random_number

console.print(f"[新增] 已添加工具：{random_number.name}", style="green")
console.print(f"  描述：{random_number.description.split('。')[0]}", style="white")

# [新增] 测试
console.print("\n[bold cyan]测试新工具：[/bold cyan]")

# 直接调用测试
result = random_number.invoke({"min_value": 1, "max_value": 100})
console.print(f"  random_number(1, 100) = {result}", style="green")

result = random_number.invoke({"min_value": 10, "max_value": 20})
console.print(f"  random_number(10, 20) = {result}", style="green")

# Agent 调用测试
console.print("\n[bold cyan]通过 Agent 调用测试：[/bold cyan]")
from modules.agent import SmartAgent
agent = SmartAgent()
result = agent.tool_mode("帮我生成一个 1 到 50 之间的随机数")
console.print(f"  Agent：{result}", style="bold green")

console.print("\n练习 1 完成！", style="bold green")
