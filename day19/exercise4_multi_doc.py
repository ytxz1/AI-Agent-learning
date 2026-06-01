"""
Day 19 - 练习 4（挑战）：多文档智能问答系统

任务：支持多种来源的文档问答，带来源引用。

新增内容（标注 [新增]）：
  1. [新增] 多文档来源管理
  2. [新增] 带来源引用的回答
  3. [新增] 文档过滤检索
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME, EMBEDDING_MODEL
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 19 - 练习 4：多文档智能问答", style="bold blue")
console.print("=" * 60, style="bold blue")

current_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(current_dir, "documents")

# 加载文档
dir_loader = DirectoryLoader(docs_dir, glob="*.txt", loader_cls=TextLoader,
                              loader_kwargs={"encoding": "utf-8"})
docs = dir_loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
split_docs = splitter.split_documents(docs)

# [新增] 文档来源统计
console.print("\n[bold cyan][新增] 已加载文档来源：[/bold cyan]")
source_count = {}
for doc in split_docs:
    src = os.path.basename(doc.metadata.get("source", "unknown"))
    source_count[src] = source_count.get(src, 0) + 1

table = Table(title="文档来源统计", show_header=True)
table.add_column("文件", style="cyan")
table.add_column("文本块数", style="green")
for src, count in source_count.items():
    table.add_row(src, str(count))
console.print(table)

try:
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_BASE_URL)
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, model=MODEL_NAME, temperature=0.7)

    vectorstore = Chroma.from_documents(split_docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # [新增] 带来源引用的 RAG 提示词
    rag_prompt = ChatPromptTemplate.from_template(
        "根据以下上下文回答问题。回答时请引用信息来源。\n\n"
        "上下文：\n{context}\n\n问题：{question}\n\n回答（请注明引用来源）："
    )

    def format_docs_with_source(docs):
        parts = []
        for doc in docs:
            src = os.path.basename(doc.metadata.get("source", "unknown"))
            parts.append(f"[来源: {src}] {doc.page_content}")
        return "\n\n".join(parts)

    rag_chain = ({"context": retriever | format_docs_with_source, "question": RunnablePassthrough()}
                 | rag_prompt | llm | StrOutputParser())

    # 测试
    questions = [
        "Python 有什么特点？",
        "LangChain 的 RAG 流程是什么？",
        "AI 的发展历史是怎样的？",
    ]

    for q in questions:
        console.print(f"\n[bold]问：{q}[/bold]")
        console.print("-" * 50)
        # 展示检索来源
        results = retriever.invoke(q)
        for i, doc in enumerate(results):
            src = os.path.basename(doc.metadata.get("source", "unknown"))
            console.print(f"  [来源] {src}: {doc.page_content[:50]}...", style="dim")
        # 生成带引用的回答
        answer = rag_chain.invoke(q)
        console.print(f"  答：{answer}", style="green")

except Exception as e:
    console.print(f"  操作失败：{e}", style="red")

console.print("\n练习 4 完成！", style="bold green")
