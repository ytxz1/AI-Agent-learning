"""Day 18 - 练习 1：构建检索器。"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR, TOP_K
from modules.pipeline import RAGPipeline

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 18 - 练习 1：构建检索器", style="bold blue")
console.print("=" * 60, style="bold blue")

pipeline = RAGPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, top_k=TOP_K)
pipeline.load()
pipeline.split()

console.print(f"文档数量：{pipeline.document_summary()['document_count']}", style="green")
console.print(f"chunk 数量：{pipeline.chunk_summary()['chunk_count']}", style="green")
console.print("\n[bold cyan]chunk 预览：[/bold cyan]")
for line in pipeline.chunk_previews():
    console.print(line, style="yellow")

