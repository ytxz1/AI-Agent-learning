"""Day 17 - 练习 4：保留元数据。"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR
from modules.pipeline import DocumentPipeline

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 17 - 练习 4：保留元数据", style="bold blue")
console.print("=" * 60, style="bold blue")

pipeline = DocumentPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
pipeline.load()
pipeline.split_by_type()

console.print(f"chunk 数量：{len(pipeline.chunks)}", style="green")
for index, chunk in enumerate(pipeline.chunks[:5], 1):
    console.print(f"\n[bold cyan]Chunk {index}[/bold cyan]", style="cyan")
    console.print(chunk.page_content[:160], style="yellow")
    console.print(f"metadata = {chunk.metadata}", style="green")

