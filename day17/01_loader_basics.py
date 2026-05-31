"""Day 17 - 练习 1：文档加载基础。"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import DOCS_DIR
from modules.pipeline import DocumentPipeline

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 17 - 练习 1：文档加载基础", style="bold blue")
console.print("=" * 60, style="bold blue")

pipeline = DocumentPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR)
pipeline.load()

summary = pipeline.document_summary()
console.print(f"文档数量：{summary['document_count']}", style="green")
console.print(f"总字符数：{summary['total_chars']}", style="green")
console.print(f"文件类型：{summary['file_types']}", style="green")

console.print("\n[bold cyan]文档预览：[/bold cyan]")
for line in pipeline.document_previews():
    console.print(line, style="yellow")

