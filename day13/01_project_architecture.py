"""
Day 13 - 项目实战：综合 AI 助手架构

本文件展示项目的整体架构设计：
1. 项目目标：构建一个综合 AI 助手
2. 架构设计：模块化分层
3. 各模块职责和关系
4. 数据流向

Day 8-12 知识回顾：
  Day 8: 使用 LangChain 调用 LLM
  Day 9: Memory 管理对话历史
  Day 10: Tools 扩展 AI 能力
  Day 11: Agents 自主决策
  Day 12: RAG 基于文档问答
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

console.print("=" * 70, style="bold blue")
console.print("Day 13 - 项目实战：综合 AI 助手", style="bold blue")
console.print("=" * 70, style="bold blue")

# ============================================================
# 1. 项目架构
# ============================================================
console.print("\n[bold cyan]1. 项目架构图[/bold cyan]")
console.print(Panel(
    "┌──────────────────────────────────────┐\n"
    "│         综合 AI 助手                   │\n"
    "│                                      │\n"
    "│  ┌──────────┐  ┌──────────┐        │\n"
    "│  │  LLM 层   │  │  配置层   │        │\n"
    "│  │ (ChatOpenAI)│  │ (config.py)│      │\n"
    "│  └────┬─────┘  └──────────┘        │\n"
    "│       │                             │\n"
    "│  ┌────┴─────────────────────┐     │\n"
    "│  │       模块层               │     │\n"
    "│  │  ┌─────┐ ┌──────┐ ┌───┐ │     │\n"
    "│  │  │Tools│ │Memory│ │RAG│ │     │\n"
    "│  │  │工具  │ │记忆  │ │检索│ │     │\n"
    "│  │  └─────┘ └──────┘ └───┘ │     │\n"
    "│  └──────────┬──────────────┘     │\n"
    "│             │                    │\n"
    "│  ┌──────────┴──────────────┐     │\n"
    "│  │      Agent 层            │     │\n"
    "│  │  ReAct 推理 + 工具选择   │     │\n"
    "│  └─────────────────────────┘     │\n"
    "│             │                    │\n"
    "│  ┌──────────┴──────────────┐     │\n"
    "│  │      界面层 (main.py)    │     │\n"
    "│  │  交互式命令行 + 功能菜单  │     │\n"
    "│  └─────────────────────────┘     │\n"
    "└──────────────────────────────────────┘",
    title="项目架构",
    style="green"
))

# ============================================================
# 2. 各模块职责
# ============================================================
console.print("\n[bold cyan]2. 各模块职责[/bold cyan]")

table = Table(title="模块清单", show_header=True)
table.add_column("模块", style="cyan", width=15)
table.add_column("文件", style="green", width=25)
table.add_column("职责", style="white", width=40)
table.add_row("配置层", "config.py", "加载 API 密钥、基础配置")
table.add_row("LLM 层", "各模块文件", "调用 DeepSeek/ChatOpenAI")
table.add_row("Tools", "02_tools_module.py", "定义计算、天气、搜索等工具")
table.add_row("Memory", "03_memory_module.py", "对话历史管理和裁剪")
table.add_row("RAG", "04_rag_module.py", "文档加载、分割、检索")
table.add_row("Agent", "05_agent_module.py", "ReAct 推理、工具选择")
table.add_row("界面", "06_chat_interface.py", "交互式命令行菜单")
table.add_row("入口", "main.py", "启动程序")
console.print(table)

# ============================================================
# 3. 知识回顾
# ============================================================
console.print("\n[bold cyan]3. 知识点映射[/bold cyan]")

map_table = Table(title="Day 8-12 知识回顾", show_header=True)
map_table.add_column("Day", style="cyan", width=8)
map_table.add_column("主题", style="yellow", width=20)
map_table.add_column("在本项目中的应用", style="white", width=40)
map_table.add_row("Day 8", "LLM + Chain", "使用 ChatOpenAI 调用大模型")
map_table.add_row("Day 9", "Memory", "管理对话历史、裁剪 Token")
map_table.add_row("Day 10", "Tools", "定义和注册自定义工具")
map_table.add_row("Day 11", "Agents", "ReAct 推理、工具选择")
map_table.add_row("Day 12", "RAG", "文档加载、向量检索、增强生成")
console.print(map_table)

# ============================================================
# 4. 数据流向
# ============================================================
console.print("\n[bold cyan]4. 数据流向[/bold cyan]")
console.print(Panel(
    "用户输入 -> 主程序 -> 功能分发\n"
    "    |\n"
    "    +-> 普通对话 -> Memory + LLM -> 回答\n"
    "    +-> 工具调用 -> Agent(ReAct) -> Tools -> LLM -> 回答\n"
    "    +-> 文档问答 -> RAG(检索) -> LLM -> 回答\n"
    "    +-> 代码助手 -> Agent -> 执行/分析 -> 回答",
    title="数据流向",
    style="cyan"
))

console.print("\n[bold green]项目架构展示完成！[/bold green]")
console.print("继续学习：python 02_tools_module.py")
