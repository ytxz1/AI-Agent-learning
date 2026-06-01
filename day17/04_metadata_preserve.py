"""Day 17 - 练习 4：保留元数据。

练习目标：
观察文档被切成 chunk 后，source、file_name、file_type 等 metadata 是否还在。

参考答案：
调用 pipeline.split_by_type() 后查看前几个 chunk 的 metadata。
"""

from __future__ import annotations

import os
import sys

# 添加 day17 根目录到模块搜索路径。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR
from modules.pipeline import DocumentPipeline

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 17 - 练习 4：保留元数据", style="bold blue")
console.print("=" * 60, style="bold blue")

# 构建文档处理管线。
pipeline = DocumentPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

# 先加载文档，再按文件类型选择切分策略。
pipeline.load()
pipeline.split_by_type()

console.print(f"chunk 数量：{len(pipeline.chunks)}", style="green")

# 只预览前 5 个 chunk，重点看 metadata 是否保留下来。
for index, chunk in enumerate(pipeline.chunks[:5], 1):
    console.print(f"\n[bold cyan]Chunk {index}[/bold cyan]", style="cyan")
    console.print(chunk.page_content[:160], style="yellow")
    console.print(f"metadata = {chunk.metadata}", style="green")
