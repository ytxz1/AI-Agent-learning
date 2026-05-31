"""Day 18 - 练习 4：Top-K 对比。"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.table import Table

from config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR
from modules.pipeline import RAGPipeline

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 18 - 练习 4：Top-K 对比", style="bold blue")
console.print("=" * 60, style="bold blue")

table = Table(title="Top-K 对比", show_header=True)
table.add_column("top_k", style="cyan", width=8)
table.add_column("结果数量", style="yellow", width=12)
table.add_column("前两条摘要", style="green", width=60)

for top_k in [1, 2, 3, 4]:
    pipeline = RAGPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, top_k=top_k)
    result = pipeline.ask("RAG 的核心流程是什么")
    summary_lines = result["retrieval_summary"].splitlines()
    preview = " | ".join(summary_lines[:2])[:60]
    table.add_row(str(top_k), str(len(summary_lines)), preview)

console.print(table)

