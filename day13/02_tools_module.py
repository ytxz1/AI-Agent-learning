"""Day 13 - 练习 2：工具模块讲解。

这个文件帮助你理解：
- 什么是工具
- 工具为什么要单独放在一个模块里
- 工具如何被 Agent 调用
- 如何把“输出解析”相关知识放进知识库里
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 13 - 工具模块讲解", style="bold blue")
console.print("=" * 60, style="bold blue")

console.print(
    Panel(
        "工具（Tool）就是 Agent 可以直接调用的外部函数。\n"
        "当模型发现自己需要计算、查询、换算或检索信息时，就可以把任务交给工具去做。",
        title="什么是工具",
        style="green",
    )
)

table = Table(title="内置工具", show_header=True)
table.add_column("工具名", style="cyan", width=18)
table.add_column("作用", style="white", width=38)
table.add_column("常见输入", style="yellow", width=22)
table.add_row("calculator", "执行数学计算", "expression")
table.add_row("get_weather", "查询天气", "city")
table.add_row("search_knowledge", "从简易知识库检索信息", "query")
table.add_row("get_current_time", "返回当前时间", "无参数")
table.add_row("unit_convert", "进行单位换算", "value/from_unit/to_unit")
console.print(table)

console.print("\n[bold cyan]知识库示例[/bold cyan]")
console.print(
    Panel(
        "search_knowledge 工具里保存的是一些常见概念说明。\n"
        "这一版不再放旧的文档问答说明，而是放了输出解析、结构化输出、JSON 等概念，\n"
        "这样更符合 Day 13 当前的学习主题。",
        style="yellow",
    )
)

console.print(
    Panel(
        "你可以把工具理解成：\n"
        "1. 模型负责思考\n"
        "2. 工具负责执行\n"
        "3. Agent 负责决定什么时候调用工具",
        title="工具的意义",
        style="blue",
    )
)

console.print("\n练习 2 讲解完成。", style="bold green")
