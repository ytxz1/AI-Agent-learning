"""
Day 19 - 项目 2：RAG 问答系统 - 检索器

本示例演示检索器的使用和高级检索策略：
1. 基本检索（similarity_search）
2. 带分数的检索
3. MMR 检索（最大边际相关性）
4. 多查询检索

知识点：
1. Retriever 是 RAG 中连接文档和 LLM 的桥梁
2. 检索质量直接决定 RAG 回答的质量
3. MMR 可以在相关性和多样性之间平衡
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 19 - 检索器", style="bold blue")
console.print("=" * 60, style="bold blue")

current_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(current_dir, "documents")

# 加载并分割文档
dir_loader = DirectoryLoader(docs_dir, glob="*.txt", loader_cls=TextLoader,
                              loader_kwargs={"encoding": "utf-8"})
docs = dir_loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
split_docs = splitter.split_documents(docs)

try:
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import Chroma
    from config import OPENAI_API_KEY, OPENAI_BASE_URL, EMBEDDING_MODEL

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_BASE_URL,
    )

    persist_dir = os.path.join(current_dir, "chroma_db")
    if os.path.exists(persist_dir):
        vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    else:
        vectorstore = Chroma.from_documents(split_docs, embeddings, persist_directory=persist_dir)

    # ============================================================
    # 1. 基本检索
    # ============================================================
    console.print("\n[bold cyan]1. 基本检索（similarity_search）[/bold cyan]")

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    query = "LangChain 有哪些组件？"
    console.print(f"  查询：{query}", style="white")
    results = retriever.invoke(query)
    for i, doc in enumerate(results):
        source = os.path.basename(doc.metadata.get("source", "unknown"))
        console.print(f"  [{i+1}] ({source}) {doc.page_content[:70]}...", style="yellow")

    # ============================================================
    # 2. MMR 检索（多样性）
    # ============================================================
    console.print("\n[bold cyan]2. MMR 检索（最大边际相关性）[/bold cyan]")
    console.print(Panel(
        "普通检索：返回最相似的 K 个结果（可能高度重复）\n"
        "MMR 检索：在相关性和多样性之间平衡\n\n"
        "MMR 会去重，返回更多样化的结果\n"
        "适合需要不同角度信息的场景",
        title="MMR vs 普通检索",
        style="cyan"
    ))

    mmr_retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.5}
    )

    query = "人工智能的应用"
    console.print(f"  查询：{query}", style="white")

    console.print("\n  [普通检索]", style="bold")
    normal_results = retriever.invoke(query)
    for i, doc in enumerate(normal_results):
        console.print(f"  [{i+1}] {doc.page_content[:70]}...", style="yellow")

    console.print("\n  [MMR 检索]", style="bold")
    mmr_results = mmr_retriever.invoke(query)
    for i, doc in enumerate(mmr_results):
        console.print(f"  [{i+1}] {doc.page_content[:70]}...", style="green")

except Exception as e:
    console.print(f"  检索操作失败：{e}", style="red")

console.print(Panel(
    "检索策略选择：\n"
    "  - 普通检索：大多数场景足够\n"
    "  - MMR 检索：需要多样化结果时使用\n"
    "  - k 值：通常 3-5 个结果即可\n"
    "  - chunk_size 影响检索粒度",
    title="检索最佳实践",
    style="green"
))

console.print("\n检索器演示完成！", style="bold green")
