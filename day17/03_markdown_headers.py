"""Day 17 - 练习 3：Markdown 标题切分。"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import DOCS_DIR
from modules.pipeline import DocumentPipeline
from modules.splitter import split_markdown_headers

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 17 - 练习 3：Markdown 标题切分", style="bold blue")
console.print("=" * 60, style="bold blue")

pipeline = DocumentPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR)
pipeline.load()

md_docs = [doc for doc in pipeline.documents if doc.metadata.get("file_type") == ".md"]
if not md_docs:
    console.print("没有找到 Markdown 文档。", style="red")
else:
    chunks = split_markdown_headers(md_docs[0])
    for index, chunk in enumerate(chunks, 1):
        console.print(f"\n[bold cyan]Chunk {index}[/bold cyan]", style="cyan")
        console.print(chunk.page_content[:200], style="yellow")
        console.print(f"metadata = {chunk.metadata}", style="green")

