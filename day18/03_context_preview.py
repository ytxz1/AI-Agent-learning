"""Day 18 - 练习 3：上下文预览。"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR, TOP_K
from modules.pipeline import RAGPipeline

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 18 - 练习 3：上下文预览", style="bold blue")
console.print("=" * 60, style="bold blue")

pipeline = RAGPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, top_k=TOP_K)
result = pipeline.ask("请解释上下文拼接的作用")

console.print("\n[bold cyan]检索摘要：[/bold cyan]")
console.print(result["retrieval_summary"], style="yellow")
console.print("\n[bold cyan]上下文内容：[/bold cyan]")
console.print(result["context"], style="green")

