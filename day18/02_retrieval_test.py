"""Day 18 - 练习 2：检索测试。

练习目标：
用多个问题测试 Retriever 是否能找到相关 chunk。

参考答案：
调用 pipeline.ask(question)，从返回结果里查看 retrieval_summary。
"""

from __future__ import annotations

import os
import sys

# 让脚本可以直接导入 day18 内部模块。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.table import Table

from config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR, TOP_K
from modules.pipeline import RAGPipeline

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 18 - 练习 2：检索测试", style="bold blue")
console.print("=" * 60, style="bold blue")

# 创建完整检索管线。
# pipeline.ask() 会自动确保文档加载、切分和 RAGChain 初始化完成。
pipeline = RAGPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, top_k=TOP_K)

# 准备三个不同问题，观察分别命中哪些 chunk。
questions = [
    "什么是 RAG？",
    "Retriever 的作用是什么？",
    "上下文拼接为什么重要？",
]

table = Table(title="检索结果对比", show_header=True)
table.add_column("问题", style="cyan", width=24)
table.add_column("结果摘要", style="green", width=60)

for question in questions:
    # ask() 返回一个 dict，里面包含检索摘要、上下文、最终回答等信息。
    result = pipeline.ask(question)
    table.add_row(question, result["retrieval_summary"][:60] + "...")

console.print(table)
