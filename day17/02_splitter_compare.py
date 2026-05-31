"""Day 17 - 练习 2：切分器对比。"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.table import Table

from config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR
from modules.pipeline import DocumentPipeline

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 17 - 练习 2：切分器对比", style="bold blue")
console.print("=" * 60, style="bold blue")

pipeline = DocumentPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
pipeline.load()
comparisons = pipeline.compare()

table = Table(title="切分器对比", show_header=True)
table.add_column("策略", style="cyan", width=16)
table.add_column("chunk 数量", style="yellow", width=12)
table.add_column("平均长度", style="green", width=12)

for name, chunks in comparisons.items():
    total_chars = sum(len(chunk.page_content) for chunk in chunks)
    avg_chars = round(total_chars / len(chunks), 2) if chunks else 0
    table.add_row(name, str(len(chunks)), str(avg_chars))

console.print(table)

