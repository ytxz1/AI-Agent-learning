"""
Day 13 - 练习 2（中等）：对比 Agent 三种模式

任务：用相同的问题测试三种模式，对比效果差异。

新增内容（标注 [新增]）：
  1. [新增] 模式对比实验
  2. [新增] 每种模式的效果分析
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.agent import SmartAgent
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 13 - 练习 2：Agent 模式对比", style="bold blue")
console.print("=" * 60, style="bold blue")

agent = SmartAgent()

# [新增] 测试问题
test_cases = [
    ("你好，我叫小明", "chat"),
    ("北京天气怎么样？", "tool"),
    ("什么是 Python？", "rag"),
    ("帮我算一下 2 的 20 次方", "tool"),
    ("现在几点了？", "tool"),
    ("Python 有什么特点？", "rag"),
]

# [新增] 模式对比表
table = Table(title="模式对比实验", show_header=True)
table.add_column("问题", style="cyan", width=25)
table.add_column("推荐模式", style="yellow", width=12)
table.add_column("实际效果", style="green", width=50)

for question, expected in test_cases:
    # 用 chat 模式
    agent.switch_mode("chat")
    chat_result = agent.chat_mode(question)
    agent.clear_memory()

    # 用 tool 模式
    agent.switch_mode("tool")
    tool_result = agent.tool_mode(question)
    agent.clear_memory()

    expected_name = {"chat": "普通对话", "tool": "工具调用", "rag": "文档检索"}[expected]
    best = "chat" if len(chat_result) < len(tool_result) else "tool"
    table.add_row(question[:25], expected_name, chat_result[:40] + "...")

console.print(table)

console.print(Panel(
    "[bold]结论：[/bold]\n"
    "  - 日常对话（问候、名字）：用 chat 模式\n"
    "  - 需要外部信息（天气、计算）：用 tool 模式\n"
    "  - 文档知识（产品说明、指南）：用 rag 模式\n"
    "  - 未来可以加上 auto 模式自动判断",
    title="模式选择建议",
    style="green"
))

console.print("\n练习 2 完成！", style="bold green")
