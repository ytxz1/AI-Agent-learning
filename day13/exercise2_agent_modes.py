"""Day 13 - 练习 2：对比 Agent 的三种模式。

任务：
- 用同一组问题测试三种模式
- 理解 chat、tool、parse 的区别
- 看看不同问题应该交给哪种模式处理
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from modules.agent import SmartAgent

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 13 - 练习 2：Agent 模式对比", style="bold blue")
console.print("=" * 60, style="bold blue")

agent = SmartAgent()

test_cases = [
    ("你好，我叫小明", "chat"),
    ("北京天气怎么样？", "tool"),
    ("什么是 Python？", "parse"),
    ("帮我算一下 2 的 20 次方", "tool"),
    ("现在几点了？", "tool"),
    ("请把这段需求整理成 JSON：我要做一个天气助手，需要支持北京、上海和深圳。", "parse"),
]

table = Table(title="模式对比实验", show_header=True)
table.add_column("问题", style="cyan", width=28)
table.add_column("推荐模式", style="yellow", width=12)
table.add_column("演示结果", style="green", width=50)

for question, expected in test_cases:
    agent.switch_mode("chat")
    chat_result = agent.chat_mode(question)
    agent.clear_memory()

    agent.switch_mode("tool")
    tool_result = agent.tool_mode(question)
    agent.clear_memory()

    agent.switch_mode("parse")
    parse_result = agent.parse_mode(question)
    agent.clear_memory()

    expected_name = {"chat": "普通对话", "tool": "工具调用", "parse": "输出解析"}[expected]
    if expected == "chat":
        sample_result = chat_result
    elif expected == "tool":
        sample_result = tool_result
    else:
        sample_result = parse_result
    table.add_row(question[:28], expected_name, sample_result[:40] + "...")

console.print(table)

console.print(
    Panel(
        "[bold]结论：[/bold]\n"
        "  - 日常聊天：用 chat 模式\n"
        "  - 需要计算、天气、时间：用 tool 模式\n"
        "  - 需要整理、提取、结构化、JSON：用 parse 模式\n"
        "  - 后面可以再加 auto 模式自动判断",
        title="模式选择建议",
        style="green",
    )
)

console.print("\n练习 2 完成！", style="bold green")
