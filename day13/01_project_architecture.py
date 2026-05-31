"""Day 13 - 项目实战：综合 AI 助手架构说明。

这个文件用来帮助你理解整个 Day 13 项目是如何分层的：
1. 配置层
2. 工具层
3. 记忆层
4. 输出解析层
5. Agent 层
6. 界面层
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

console.print("=" * 70, style="bold blue")
console.print("Day 13 - 项目实战：综合 AI 助手", style="bold blue")
console.print("=" * 70, style="bold blue")

console.print("\n[bold cyan]1. 项目架构图[/bold cyan]")
console.print(
    Panel(
        "┌──────────────────────────────┐\n"
        "│         综合 AI 助手         │\n"
        "└──────────────┬───────────────┘\n"
        "               │\n"
        "   ┌───────────┼───────────┐\n"
        "   │           │           │\n"
        "LLM 层      配置层       模块层\n"
        "(ChatOpenAI) (config.py) (tools / memory / output parser)\n"
        "               │           │\n"
        "               └─────┬─────┘\n"
        "                     │\n"
        "                  Agent 层\n"
        "           (ReAct 推理 + 模式切换)\n"
        "                     │\n"
        "                  界面层\n"
        "          (交互式命令行菜单)",
        title="项目架构",
        style="green",
    )
)

console.print("\n[bold cyan]2. 各模块职责[/bold cyan]")
table = Table(title="模块清单", show_header=True)
table.add_column("模块", style="cyan", width=15)
table.add_column("文件", style="green", width=30)
table.add_column("职责", style="white", width=40)
table.add_row("配置层", "config.py", "加载 API Key、模型名和基础配置")
table.add_row("工具层", "modules/tools.py", "计算、天气、时间、知识检索、单位转换")
table.add_row("记忆层", "modules/memory.py", "保存对话历史和系统提示词")
table.add_row("输出解析层", "modules/output_parser.py", "把自然语言整理成 JSON 等结构化结果")
table.add_row("Agent", "05_agent_module.py", "整合模式切换、工具调用和推理逻辑")
table.add_row("界面层", "06_chat_interface.py", "提供命令行菜单与交互")
table.add_row("入口文件", "main.py", "启动整个项目")
console.print(table)

console.print("\n[bold cyan]3. Day 8-13 知识回顾[/bold cyan]")
map_table = Table(title="知识映射", show_header=True)
map_table.add_column("Day", style="cyan", width=8)
map_table.add_column("主题", style="yellow", width=20)
map_table.add_column("在本项目中的应用", style="white", width=40)
map_table.add_row("Day 8", "LLM + Chain", "使用 ChatOpenAI 作为核心模型")
map_table.add_row("Day 9", "Memory", "保存对话历史并参与上下文构建")
map_table.add_row("Day 10", "Tools", "定义并注册可调用工具")
map_table.add_row("Day 11", "Agents", "根据问题决定调用哪种能力")
map_table.add_row("Day 12", "输出解析", "把文本整理成结构化 JSON")
map_table.add_row("Day 13", "综合实战", "把聊天、工具、记忆和输出解析整合到一起")
console.print(map_table)

console.print("\n[bold cyan]4. 数据流向[/bold cyan]")
console.print(
    Panel(
        "用户输入 -> 主程序 -> 功能分发\n"
        "    |\n"
        "    +-> 普通对话 -> Memory + LLM -> 回复\n"
        "    +-> 工具调用 -> Agent(ReAct) -> Tools -> LLM -> 回复\n"
        "    +-> 输出解析 -> Output Parser -> JSON 结果\n"
        "    +-> 历史查看 -> Memory -> 历史表格",
        title="数据流向",
        style="cyan",
    )
)

console.print("\n[bold green]项目架构说明完成，继续学习：python 02_tools_module.py[/bold green]")
