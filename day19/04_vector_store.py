"""
Day 19 - 项目 2：RAG 问答系统 - 向量数据库

本示例演示向量数据库的核心概念和使用：
1. 什么是向量数据库
2. 使用 ChromaDB 作为本地向量存储
3. 文档的存入和检索
4. 相似度搜索

知识点：
1. 向量数据库专门用于存储和检索高维向量
2. ChromaDB 是轻量级本地向量数据库
3. 相似度搜索是向量数据库的核心功能
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 19 - 向量数据库", style="bold blue")
console.print("=" * 60, style="bold blue")

# ============================================================
# 1. 什么是向量数据库
# ============================================================
console.print("\n[bold cyan]1. 什么是向量数据库[/bold cyan]")
console.print(Panel(
    "向量数据库是专门存储和检索高维向量的数据库。\n\n"
    "传统数据库：SELECT * WHERE name = 'Python'（精确匹配）\n"
    "向量数据库：找到与查询最相似的 K 个结果（模糊搜索）\n\n"
    "常用向量数据库：\n"
    "  - ChromaDB：轻量级，适合本地开发\n"
    "  - FAISS：Facebook 开源，性能优秀\n"
    "  - Pinecone：云端托管服务\n"
    "  - Weaviate：开源，支持多种搜索",
    title="向量数据库",
    style="cyan"
))

# ============================================================
# 2. 准备文档
# ============================================================
console.print("\n[bold cyan]2. 准备文档数据[/bold cyan]")

current_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(current_dir, "documents")

# 加载文档
dir_loader = DirectoryLoader(docs_dir, glob="*.txt", loader_cls=TextLoader,
                              loader_kwargs={"encoding": "utf-8"})
docs = dir_loader.load()

# 分割文档
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
split_docs = splitter.split_documents(docs)

console.print(f"  加载 {len(docs)} 个文档，分割为 {len(split_docs)} 个文本块", style="green")

# ============================================================
# 3. 使用 ChromaDB 存储向量
# ============================================================
console.print("\n[bold cyan]3. 使用 ChromaDB 存储向量[/bold cyan]")

try:
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import Chroma
    from config import OPENAI_API_KEY, OPENAI_BASE_URL, EMBEDDING_MODEL

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_BASE_URL,
    )

    # 创建向量数据库（存入文档）
    persist_dir = os.path.join(current_dir, "chroma_db")
    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=persist_dir,
    )
    console.print(f"  已将 {len(split_docs)} 个文本块存入 ChromaDB", style="green")
    console.print(f"  数据库路径：{persist_dir}", style="dim")

    # ============================================================
    # 4. 相似度搜索
    # ============================================================
    console.print("\n[bold cyan]4. 相似度搜索[/bold cyan]")

    query = "Python 有什么特点？"
    console.print(f"  查询：{query}", style="white")

    results = vectorstore.similarity_search(query, k=3)
    console.print(f"  找到 {len(results)} 个相关结果：", style="green")
    for i, doc in enumerate(results):
        source = os.path.basename(doc.metadata.get("source", "unknown"))
        console.print(f"  [{i+1}] ({source}) {doc.page_content[:80]}...", style="yellow")

    # ============================================================
    # 5. 带分数的搜索
    # ============================================================
    console.print("\n[bold cyan]5. 带相似度分数的搜索[/bold cyan]")

    results_with_scores = vectorstore.similarity_search_with_score(query, k=3)
    for i, (doc, score) in enumerate(results_with_scores):
        source = os.path.basename(doc.metadata.get("source", "unknown"))
        console.print(f"  [{i+1}] 分数={score:.4f} ({source}) {doc.page_content[:60]}...", style="yellow")

except Exception as e:
    console.print(f"  向量数据库操作失败：{e}", style="red")
    console.print("  可能需要安装 chromadb: pip install chromadb", style="yellow")

console.print("\n向量数据库演示完成！", style="bold green")
