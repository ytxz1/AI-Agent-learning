"""Day 18 - 练习 2：检索测试。"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.table import Table

from config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR, TOP_K
from modules.pipeline import RAGPipeline

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 18 - 练习 2：检索测试", style="bold blue")
console.print("=" * 60, style="bold blue")

pipeline = RAGPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, top_k=TOP_K)

questions = [
    "什么是 RAG？",
    "Retriever 的作用是什么？",
    "上下文拼接为什么重要？",
]

table = Table(title="检索结果对比", show_header=True)
table.add_column("问题", style="cyan", width=24)
table.add_column("结果摘要", style="green", width=60)

for question in questions:
    result = pipeline.ask(question)
    table.add_row(question, result["retrieval_summary"][:60] + "...")

console.print(table)

