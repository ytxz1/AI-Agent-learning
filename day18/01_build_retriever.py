"""Day 18 - 练习 1：构建检索器。

练习目标：
先确认 RAG 检索链的基础资料已经准备好：文档能加载、chunk 能生成。

参考答案：
创建 RAGPipeline，执行 load() 和 split()，再查看文档数量、chunk 数量和 chunk 预览。
"""

from __future__ import annotations

import os
import sys

# 把当前 day18 目录加入模块搜索路径，保证直接运行脚本时导入稳定。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR, TOP_K
from modules.pipeline import RAGPipeline

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 18 - 练习 1：构建检索器", style="bold blue")
console.print("=" * 60, style="bold blue")

# 创建 RAGPipeline。
# 这里还没有真正提问，只是先准备文档和 chunk。
pipeline = RAGPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, top_k=TOP_K)

# 1. 加载 documents/ 下的文档。
pipeline.load()

# 2. 把文档切成 chunk，并在内部创建 RAGChain。
pipeline.split()

# 3. 查看基础统计，确认检索器的数据来源没问题。
console.print(f"文档数量：{pipeline.document_summary()['document_count']}", style="green")
console.print(f"chunk 数量：{pipeline.chunk_summary()['chunk_count']}", style="green")
console.print("\n[bold cyan]chunk 预览：[/bold cyan]")
for line in pipeline.chunk_previews():
    console.print(line, style="yellow")
