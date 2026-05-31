"""
Day 12 - 文本分割器：将长文档切分成小块

本示例演示文本分割的核心概念和方法：
1. 为什么要分割文本
2. 三种分割器的对比
3. 分割参数对 RAG 效果的影响

知识点：
1. chunk_size - 每个文本块的大小
2. chunk_overlap - 块之间的重叠
3. 不同分割器的适用场景
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)
from langchain_core.documents import Document
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 12 - 文本分割器", style="bold blue")
console.print("=" * 60, style="bold blue")

# ============================================================
# 1. 为什么要分割文本
# ============================================================
console.print("\n[bold cyan]1. 为什么要分割文本[/bold cyan]")
console.print(Panel(
    "LLM 有 Token 限制（如 4096、8192、128K）\n"
    "一篇长文档可能超过限制，必须切分成小块\n\n"
    "分割的好处：\n"
    "  1. 适应 LLM 的上下文窗口\n"
    "  2. 提高检索精度（只返回相关段落）\n"
    "  3. 减少无关信息的干扰\n\n"
    "分割的挑战：\n"
    "  - 切太碎：丢失上下文\n"
    "  - 太大：检索不精确",
    title="为什么分割", style="cyan"
))

# ============================================================
# 2. RecursiveCharacterTextSplitter（推荐）
# ============================================================
console.print("\n[bold cyan]2. RecursiveCharacterTextSplitter（推荐）[/bold cyan]")
console.print("按优先级递归分割：\n -> \n -> 句号 -> 空格 -> 字符")

sample_text = """Python 是一种高级编程语言。它由 Guido van Rossum 创建。

Python 的特点包括：语法简洁、易于学习、丰富的库。
它广泛应用于 Web 开发、数据科学、人工智能等领域。

LangChain 是构建 LLM 应用的框架。它提供了模块化的组件。
RAG 是一种结合检索和生成的技术，能让 LLM 基于外部知识回答问题。"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=80,       # 每个块最多 80 个字符
    chunk_overlap=20,    # 块之间重叠 20 个字符
    separators=["\n\n", "\n", "。", "，", " ", ""],  # 分割优先级
)

chunks = splitter.split_text(sample_text)
console.print(f"  原文长度：{len(sample_text)} 字符", style="white")
console.print(f"  分割后：{len(chunks)} 个块", style="green")
for i, chunk in enumerate(chunks):
    console.print(f"  块 {i+1}（{len(chunk)} 字符）：{chunk[:50]}...", style="yellow")

# ============================================================
# 3. chunk_size 和 chunk_overlap 的影响
# ============================================================
console.print("\n[bold cyan]3. 分割参数对比[/bold cyan]")

table = Table(title="不同参数的分割效果", show_header=True)
table.add_column("chunk_size", style="cyan", width=12)
table.add_column("chunk_overlap", style="yellow", width=14)
table.add_column("块数", style="green", width=6)
table.add_column("特点", style="white", width=35)

for size, overlap in [(50, 10), (100, 20), (200, 50), (500, 100)]:
    s = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    c = s.split_text(sample_text)
    if size <= 50:
        feat = "细粒度，检索精确但可能丢失上下文"
    elif size <= 100:
        feat = "平衡，适合大多数场景"
    elif size <= 200:
        feat = "较大块，保留更多上下文"
    else:
        feat = "大块，上下文完整但可能不精确"
    table.add_row(str(size), str(overlap), str(len(c)), feat)

console.print(table)

# ============================================================
# 4. 对 Document 对象进行分割
# ============================================================
console.print("\n[bold cyan]4. 对 Document 对象进行分割[/bold cyan]")

# 加载文档
current_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(current_dir, "documents")

from langchain_community.document_loaders import TextLoader, DirectoryLoader

dir_loader = DirectoryLoader(docs_dir, glob="*.txt", loader_cls=TextLoader,
                              loader_kwargs={"encoding": "utf-8"})
docs = dir_loader.load()

console.print(f"  加载了 {len(docs)} 个文档", style="white")

# 分割
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
split_docs = splitter.split_documents(docs)

console.print(f"  分割后：{len(split_docs)} 个文本块", style="green")
for i, doc in enumerate(split_docs[:5]):
    source = os.path.basename(doc.metadata.get("source", "unknown"))
    console.print(f"  [{i+1}] ({source}) {doc.page_content[:60]}...", style="yellow")

# ============================================================
# 5. 最佳实践
# ============================================================
console.print(Panel(
    "最佳实践：\n"
    "  1. 推荐使用 RecursiveCharacterTextSplitter\n"
    "  2. chunk_size: 200-500（中文）或 500-1000（英文）\n"
    "  3. chunk_overlap: chunk_size 的 10%-20%\n"
    "  4. 根据文档类型调整分隔符\n"
    "  5. 分割后检查是否有截断或语义断裂",
    title="文本分割最佳实践",
    style="green"
))

console.print("\n文本分割演示完成！", style="bold green")
