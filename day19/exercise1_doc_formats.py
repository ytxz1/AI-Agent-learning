"""
Day 19 - 练习 1（基础）：加载不同格式的文档

任务：尝试加载不同格式的文档，对比 Document 对象的结构。

新增内容（标注 [新增]）：
  1. [新增] 手动创建 Document 对象
  2. [新增] 从不同来源加载文档
  3. [新增] 修改和管理 metadata
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_core.documents import Document
from rich.console import Console
from rich.table import Table

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 19 - 练习 1：加载不同格式的文档", style="bold blue")
console.print("=" * 60, style="bold blue")

# [新增] 1. 手动创建 Document
console.print("\n[bold cyan][新增] 1. 手动创建 Document[/bold cyan]")

docs = [
    Document(page_content="Python 是一种高级编程语言。", metadata={"source": "wiki", "topic": "Python"}),
    Document(page_content="Java 是面向对象的编程语言。", metadata={"source": "wiki", "topic": "Java"}),
    Document(page_content="JavaScript 是 Web 前端的核心语言。", metadata={"source": "web", "topic": "JS"}),
]

for doc in docs:
    console.print(f"  内容：{doc.page_content}", style="green")
    console.print(f"  元数据：{doc.metadata}", style="yellow")
    console.print()

# [新增] 2. 从文本文件加载
console.print("[bold cyan][新增] 2. 从文本文件加载[/bold cyan]")

from langchain_community.document_loaders import TextLoader

current_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(current_dir, "documents")

for fname in os.listdir(docs_dir):
    if fname.endswith(".txt"):
        fpath = os.path.join(docs_dir, fname)
        loader = TextLoader(fpath, encoding="utf-8")
        loaded = loader.load()
        console.print(f"  {fname}: {len(loaded)} 个文档, {len(loaded[0].page_content)} 字符", style="green")

# [新增] 3. metadata 管理
console.print("\n[bold cyan][新增] 3. metadata 管理[/bold cyan]")

for doc in docs:
    doc.metadata["loaded_at"] = "2026-05-30"
    doc.metadata["word_count"] = len(doc.page_content)

table = Table(title="文档 metadata", show_header=True)
table.add_column("主题", style="cyan")
table.add_column("来源", style="green")
table.add_column("字数", style="yellow")
table.add_column("加载时间", style="white")
for doc in docs:
    table.add_row(
        doc.metadata.get("topic", "N/A"),
        doc.metadata.get("source", "N/A"),
        str(doc.metadata.get("word_count", 0)),
        doc.metadata.get("loaded_at", "N/A"),
    )
console.print(table)

console.print("\n练习 1 完成！", style="bold green")
