"""
Day 19 - 项目 2：交互式 RAG 文档问答助手

整合所有 RAG 知识，构建一个完整的文档问答系统。
运行方式：python main.py
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
from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
    MODEL_NAME,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    TEMPERATURE,
    TOP_K,
)
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 19 - RAG 文档问答助手", style="bold blue")
console.print("=" * 60, style="bold blue")

current_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(current_dir, "documents")

# ============================================================
# 1. 初始化 RAG 系统
# ============================================================
console.print("\n[bold cyan]正在初始化 RAG 系统...[/bold cyan]")

# 1. 加载文档。
# DirectoryLoader 会扫描 documents/ 下的 txt 文件，并用 TextLoader 读取内容。
dir_loader = DirectoryLoader(docs_dir, glob="*.txt", loader_cls=TextLoader,
                              loader_kwargs={"encoding": "utf-8"})
docs = dir_loader.load()
console.print(f"  加载了 {len(docs)} 个文档", style="green")

# 2. 分割文档。
# chunk_size 和 chunk_overlap 来自 config.py，方便你后续调参。
splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
split_docs = splitter.split_documents(docs)
console.print(f"  分割为 {len(split_docs)} 个文本块", style="green")

try:
    # 3. 创建 Embedding 模型。
    # 它负责把文档块和用户问题转换成向量。
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_BASE_URL,
    )

    # 4. 创建或加载 Chroma 向量数据库。
    # 如果 chroma_db 已存在，就复用旧索引；否则重新从文档创建。
    persist_dir = os.path.join(current_dir, "chroma_db")
    if os.path.exists(persist_dir):
        vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
        console.print("  已加载现有向量数据库", style="green")
    else:
        vectorstore = Chroma.from_documents(split_docs, embeddings, persist_directory=persist_dir)
        console.print("  已创建新的向量数据库", style="green")

    # 5. 创建检索器。
    # TOP_K 控制每次检索返回多少个相关文本块。
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})

    # 6. 创建聊天模型。
    # 模型会根据检索到的上下文生成最终回答。
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    )

    # 7. RAG 提示词。
    # 这里明确要求模型“根据上下文回答”，减少模型乱编。
    rag_prompt = ChatPromptTemplate.from_template(
        "你是一个基于文档的问答助手。请根据以下检索到的上下文来回答问题。\n"
        "如果上下文中没有相关信息，请说明你不确定。回答要简洁准确。\n\n"
        "上下文：\n{context}\n\n"
        "问题：{question}\n\n"
        "回答："
    )

    def format_docs(docs):
        """把检索到的 Document 列表拼接成 prompt 中的 context。"""
        return "\n\n".join(doc.page_content for doc in docs)

    # 8. RAG Chain。
    # 输入问题后，会先检索 context，再把 question 和 context 交给模型。
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    console.print("  RAG 系统初始化完成！", style="bold green")

    # ============================================================
    # 2. 交互式问答
    # ============================================================
    def show_menu():
        table = Table(title="Day 19 - RAG 文档问答助手", show_header=True)
        table.add_column("命令", style="green", width=12)
        table.add_column("说明", style="white")
        table.add_row("直接输入", "基于文档提问")
        table.add_row("search", "只检索文档（不调用 LLM）")
        table.add_row("docs", "查看已加载的文档")
        table.add_row("example", "查看示例问题")
        table.add_row("q", "退出程序")
        console.print(table)

    def show_examples():
        examples = [
            "Python 有什么特点？",
            "LangChain 有哪些核心组件？",
            "AI 的发展历史是怎样的？",
            "RAG 的流程是什么？",
            "Transformer 是什么？",
        ]
        console.print("\n[bold cyan]示例问题：[/bold cyan]")
        for i, ex in enumerate(examples, 1):
            console.print(f"  {i}. {ex}", style="yellow")

    def search_only(query):
        """只检索文档，不调用 LLM。

        这个命令适合调试 RAG：先确认检索结果对不对，再看模型回答。
        """
        results = retriever.invoke(query)
        console.print(f"\n检索到 {len(results)} 个相关文档：", style="green")
        for i, doc in enumerate(results):
            source = os.path.basename(doc.metadata.get("source", "unknown"))
            console.print(f"  [{i+1}] ({source})", style="cyan")
            console.print(f"      {doc.page_content[:150]}...", style="white")

    def show_docs():
        """显示已加载的文档。"""
        console.print("\n[bold cyan]已加载的文档：[/bold cyan]")
        for doc in docs:
            source = os.path.basename(doc.metadata.get("source", "unknown"))
            chars = len(doc.page_content)
            console.print(f"  - {source}（{chars} 字符）", style="green")

    console.print(Panel.fit(
        "Day 19 - RAG 文档问答助手\n"
        "基于文档进行智能问答，输入 example 查看示例",
        style="bold green"
    ))
    show_menu()

    while True:
        try:
            user_input = input("\n你：").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n再见！", style="bold red")
            break

        if not user_input:
            continue

        cmd = user_input.lower()
        if cmd == "q":
            console.print("\n再见！", style="bold red")
            break
        elif cmd == "search":
            q = input("  搜索词：").strip()
            if q:
                search_only(q)
            continue
        elif cmd == "docs":
            show_docs()
            continue
        elif cmd == "example":
            show_examples()
            continue

        # RAG 问答
        console.print("\n  [检索相关文档...]", style="dim")
        retrieved = retriever.invoke(user_input)
        for i, doc in enumerate(retrieved[:2]):
            source = os.path.basename(doc.metadata.get("source", "unknown"))
            console.print(f"  [{i+1}] ({source}) {doc.page_content[:60]}...", style="dim")

        console.print("  [生成回答...]", style="dim")
        with console.status("[bold green]思考中..."):
            answer = rag_chain.invoke(user_input)
        console.print(f"\n助手：{answer}", style="bold green")

except Exception as e:
    console.print(f"\n初始化失败：{e}", style="red")
    import traceback
    traceback.print_exc()
