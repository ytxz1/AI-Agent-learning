"""
Day 12 - 练习 2（中等）：对比不同分割参数的效果

任务：对比不同 chunk_size 和 chunk_overlap 的分割效果。

新增内容（标注 [新增]）：
  1. [新增] 多种参数组合的分割对比
  2. [新增] 可视化分割结果
  3. [新增] 最佳参数推荐
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from rich.console import Console
from rich.table import Table

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 12 - 练习 2：对比不同分割参数", style="bold blue")
console.print("=" * 60, style="bold blue")

# 加载文档
current_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(current_dir, "documents")
dir_loader = DirectoryLoader(docs_dir, glob="*.txt", loader_cls=TextLoader,
                              loader_kwargs={"encoding": "utf-8"})
docs = dir_loader.load()

# [新增] 参数对比表
console.print("\n[bold cyan][新增] 分割参数对比[/bold cyan]")

table = Table(title="分割参数对比", show_header=True)
table.add_column("chunk_size", style="cyan", width=12)
table.add_column("overlap", style="yellow", width=10)
table.add_column("块数", style="green", width=8)
table.add_column("平均长度", style="white", width=12)
table.add_column("特点", style="white", width=30)

for size, overlap in [(100, 20), (200, 50), (300, 80), (500, 100)]:
    s = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    chunks = s.split_documents(docs)
    avg_len = sum(len(c.page_content) for c in chunks) / len(chunks) if chunks else 0
    if size <= 100:
        feat = "细粒度，检索精确"
    elif size <= 200:
        feat = "平衡，推荐大多数场景"
    elif size <= 300:
        feat = "较大块，保留更多上下文"
    else:
        feat = "大块，适合长文档"
    table.add_row(str(size), str(overlap), str(len(chunks)), f"{avg_len:.0f}", feat)

console.print(table)

# [新增] 展示分割效果
console.print("\n[bold cyan][新增] 具体分割效果展示[/bold cyan]")
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = splitter.split_documents(docs)
for i, chunk in enumerate(chunks[:6]):
    source = os.path.basename(chunk.metadata.get("source", "unknown"))
    console.print(f"  [{i+1}] ({source}, {len(chunk.page_content)}字符) {chunk.page_content[:60]}...", style="yellow")

console.print("\n练习 2 完成！", style="bold green")
