"""Day 17 - 练习 3：Markdown 标题切分。

练习目标：
理解 Markdown 文档可以按标题结构切分，而不是只按字符长度硬切。

参考答案：
先筛选出 .md 文档，再调用 split_markdown_headers() 按 #、##、### 标题拆分。
"""

from __future__ import annotations

import os
import sys

# 让脚本可以直接导入 config 和 modules。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import DOCS_DIR
from modules.pipeline import DocumentPipeline
from modules.splitter import split_markdown_headers

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 17 - 练习 3：Markdown 标题切分", style="bold blue")
console.print("=" * 60, style="bold blue")

# 加载全部文档。
pipeline = DocumentPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR)
pipeline.load()

# 只挑选 Markdown 文档，因为本练习专门演示 Markdown 标题切分。
md_docs = [doc for doc in pipeline.documents if doc.metadata.get("file_type") == ".md"]
if not md_docs:
    console.print("没有找到 Markdown 文档。", style="red")
else:
    # 对第一份 Markdown 文档按标题结构切分。
    chunks = split_markdown_headers(md_docs[0])
    for index, chunk in enumerate(chunks, 1):
        console.print(f"\n[bold cyan]Chunk {index}[/bold cyan]", style="cyan")

        # 只展示前 200 个字符，避免输出过长。
        console.print(chunk.page_content[:200], style="yellow")

        # metadata 中会保留文件来源和标题层级等信息。
        console.print(f"metadata = {chunk.metadata}", style="green")
