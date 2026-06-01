"""
Day 19 - 项目 2：RAG 问答系统 - 文档加载器

本示例演示如何使用 LangChain 加载各种格式的文档：
1. TextLoader - 加载纯文本文件
2. DirectoryLoader - 加载整个目录
3. 各种格式的加载方式

知识点：
1. Document 对象的结构（page_content + metadata）
2. 不同格式的加载器选择
3. 批量加载文档
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_core.documents import Document
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 19 - 文档加载器", style="bold blue")
console.print("=" * 60, style="bold blue")

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(current_dir, "documents")

# ============================================================
# 1. 手动创建 Document 对象
# ============================================================
console.print("\n[bold cyan]1. 手动创建 Document 对象[/bold cyan]")
console.print("Document 是 LangChain 中文档的基本单位，包含 page_content 和 metadata")

# 手动创建一个 Document
doc = Document(
    page_content="Python 是一种高级编程语言，以简洁易读著称。",
    metadata={"source": "manual", "topic": "Python", "page": 1}
)

console.print(f"  page_content: {doc.page_content}", style="green")
console.print(f"  metadata: {doc.metadata}", style="yellow")

# ============================================================
# 2. 使用 TextLoader 加载单个文件
# ============================================================
console.print("\n[bold cyan]2. 使用 TextLoader 加载单个文本文件[/bold cyan]")

sample_path = os.path.join(docs_dir, "sample.txt")
loader = TextLoader(sample_path, encoding="utf-8")
docs = loader.load()

console.print(f"  加载了 {len(docs)} 个文档", style="green")
console.print(f"  文件来源: {docs[0].metadata['source']}", style="yellow")
console.print(f"  内容预览: {docs[0].page_content[:100]}...", style="white")

# ============================================================
# 3. 使用 DirectoryLoader 加载整个目录
# ============================================================
console.print("\n[bold cyan]3. 使用 DirectoryLoader 加载整个目录[/bold cyan]")

dir_loader = DirectoryLoader(
    docs_dir,
    glob="*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)
all_docs = dir_loader.load()

console.print(f"  共加载 {len(all_docs)} 个文档", style="green")
for i, doc in enumerate(all_docs):
    source = os.path.basename(doc.metadata["source"])
    console.print(f"  [{i+1}] {source}: {doc.page_content[:60]}...", style="white")

# ============================================================
# 4. Document 的 metadata 管理
# ============================================================
console.print("\n[bold cyan]4. Document 的 metadata 管理[/bold cyan]")
console.print("metadata 用于存储文档的附加信息，如来源、页码、作者等")

for doc in all_docs:
    doc.metadata["file_name"] = os.path.basename(doc.metadata["source"])
    doc.metadata["char_count"] = len(doc.page_content)

table = Table(title="文档列表", show_header=True)
table.add_column("文件名", style="cyan")
table.add_column("字符数", style="yellow")
table.add_column("来源", style="dim")
for doc in all_docs:
    table.add_row(
        doc.metadata["file_name"],
        str(doc.metadata["char_count"]),
        doc.metadata["source"]
    )
console.print(table)

# ============================================================
# 5. 支持的文档格式
# ============================================================
console.print("\n[bold cyan]5. LangChain 支持的文档格式[/bold cyan]")

formats = Table(title="常用文档加载器", show_header=True)
formats.add_column("格式", style="cyan", width=15)
formats.add_column("加载器", style="green", width=25)
formats.add_column("说明", style="white", width=30)
formats.add_row("TXT", "TextLoader", "纯文本文件")
formats.add_row("PDF", "PyPDFLoader", "PDF 文档")
formats.add_row("DOCX", "Docx2txtLoader", "Word 文档")
formats.add_row("CSV", "CSVLoader", "CSV 表格")
formats.add_row("HTML", "BSHTMLLoader", "网页文件")
formats.add_row("JSON", "JSONLoader", "JSON 数据")
formats.add_row("Markdown", "UnstructuredMarkdownLoader", "Markdown 文件")
formats.add_row("目录", "DirectoryLoader", "批量加载目录下的文件")
console.print(formats)

console.print(Panel(
    "关键概念：\n"
    "  - Document = page_content（内容）+ metadata（元数据）\n"
    "  - TextLoader 适合单个文件\n"
    "  - DirectoryLoader 适合批量加载\n"
    "  - metadata 用于存储来源、页码等附加信息",
    title="文档加载要点",
    style="green"
))

console.print("\n文档加载演示完成！", style="bold green")
