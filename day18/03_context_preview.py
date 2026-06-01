"""Day 18 - 练习 3：上下文预览。

练习目标：
理解检索结果是如何被拼接成 context，再交给模型生成回答的。

参考答案：
调用 pipeline.ask() 后，分别打印 retrieval_summary 和 context。
"""

from __future__ import annotations

import os
import sys

# 添加 day18 根目录到模块搜索路径。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR, TOP_K
from modules.pipeline import RAGPipeline

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 18 - 练习 3：上下文预览", style="bold blue")
console.print("=" * 60, style="bold blue")

# 创建管线并提问。
pipeline = RAGPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, top_k=TOP_K)
result = pipeline.ask("请解释上下文拼接的作用")

# retrieval_summary 是给人看的检索摘要。
console.print("\n[bold cyan]检索摘要：[/bold cyan]")
console.print(result["retrieval_summary"], style="yellow")

# context 是真正准备交给模型的上下文内容。
console.print("\n[bold cyan]上下文内容：[/bold cyan]")
console.print(result["context"], style="green")
