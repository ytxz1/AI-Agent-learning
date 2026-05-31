"""
Day 13 - 练习 5（综合）：扩展应用功能

任务：给主程序添加更多功能模式（翻译助手、代码助手）。

新增内容（标注 [新增]）：
  1. [新增] translate_mode - 翻译模式
  2. [新增] code_mode - 代码助手模式
  3. [新增] 模式扩展的完整流程
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 13 - 练习 5：扩展应用功能", style="bold blue")
console.print("=" * 60, style="bold blue")

llm = ChatOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, model=MODEL_NAME, temperature=0.7)

# [新增] 翻译模式
def translate_mode(text: str, target_lang: str = "中文") -> str:
    """翻译文本到目标语言"""
    prompt = f"请将以下文本翻译成{target_lang}，只返回翻译结果：\n{text}"
    return llm.invoke([HumanMessage(content=prompt)]).content

# [新增] 代码助手模式
def code_mode(request: str) -> str:
    """根据需求生成代码"""
    prompt = SystemMessage(content="你是一个 Python 代码助手。请根据用户需求生成代码，包含注释。")
    return llm.invoke([prompt, HumanMessage(content=request)]).content

# [新增] 总结模式
def summarize_mode(text: str) -> str:
    """总结文本"""
    prompt = f"请用简洁的语言总结以下内容：\n{text}"
    return llm.invoke([HumanMessage(content=prompt)]).content

# [新增] 测试所有模式
console.print("[bold cyan][新增] 测试新模式[/bold cyan]")

table = Table(title="新模式测试", show_header=True)
table.add_column("模式", style="cyan", width=14)
table.add_column("输入", style="yellow", width=25)
table.add_column("输出预览", style="green", width=45)

# 翻译测试
trans_result = translate_mode("Hello, welcome to the world of AI!", "中文")
table.add_row("翻译", "Hello, welcome...", trans_result[:45] + "...")

# 代码测试
code_result = code_mode("写一个计算斐波那契数列的 Python 函数")
table.add_row("代码", "斐波那契数列", code_result[:45] + "...")

# 总结测试
summary_result = summarize_mode("人工智能是计算机科学的一个分支。它致力于创建能够模拟人类智能的系统。AI 的发展经历了符号主义、连接主义和深度学习三个阶段。")
table.add_row("总结", "人工智能是...", summary_result[:45] + "...")

console.print(table)

console.print(Panel(
    "[bold]模式扩展方式：[/bold]\n"
    "  1. 编写功能函数\n"
    "  2. 在界面层添加命令和菜单项\n"
    "  3. 在 Agent 中注册新功能\n"
    "  4. 测试和优化\n\n"
    "[bold]可以扩展更多模式：[/bold]\n"
    "  - 图片生成模式\n"
    "  - 数据分析模式\n"
    "  - 邮件撰写模式\n"
    "  - 英语学习模式",
    title="扩展方式总结",
    style="green"
))

console.print("\n练习 5 完成！", style="bold green")
