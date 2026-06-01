"""Day 18 - 练习 4：Top-K 对比。

练习目标：
理解 top_k 控制“检索返回多少条相关 chunk”，并观察它对上下文数量的影响。

参考答案：
分别用 top_k=1、2、3、4 创建 RAGPipeline，再对同一个问题提问。
"""

from __future__ import annotations

import os
import sys

# 让脚本可以直接导入 day18 内部模块。
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

# 用同一个问题测试不同 top_k，这样对比才公平。
for top_k in [1, 2, 3, 4]:
    pipeline = RAGPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, top_k=top_k)
    result = pipeline.ask("RAG 的核心流程是什么")

    # retrieval_summary 按行展示每条检索结果。
    summary_lines = result["retrieval_summary"].splitlines()
    preview = " | ".join(summary_lines[:2])[:60]
    table.add_row(str(top_k), str(len(summary_lines)), preview)

console.print(table)
