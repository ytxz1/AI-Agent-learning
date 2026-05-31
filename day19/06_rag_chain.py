"""
Day 12 - RAG Chain：将检索和生成整合

本示例演示完整的 RAG 流程：
1. RAG 的工作原理
2. 构建 RAG Chain
3. 对比有 RAG 和没有 RAG 的回答

知识点：
1. RAG = Retrieval（检索）+ Augmented（增强）+ Generation（生成）
2. 检索到的文档作为上下文传给 LLM
3. LLM 基于上下文回答问题
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

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 12 - RAG Chain", style="bold blue")
console.print("=" * 60, style="bold blue")

# ============================================================
# 1. RAG 工作原理
# ============================================================
console.print("\n[bold cyan]1. RAG 工作原理[/bold cyan]")
console.print(Panel(
    "用户提问\n"
    "  |\n"
    "  v\n"
    "检索器（Retriever）从向量数据库中找到相关文档\n"
    "  |\n"
    "  v\n"
    "将【问题 + 检索到的文档】组合成 Prompt\n"
    "  |\n"
    "  v\n"
    "LLM 基于上下文生成回答\n"
    "  |\n"
    "  v\n"
    "输出最终答案",
    title="RAG 流程",
    style="cyan"
))

# ============================================================
# 2. 构建 RAG Chain
# ============================================================
console.print("\n[bold cyan]2. 构建 RAG Chain[/bold cyan]")

current_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(current_dir, "documents")

# 加载文档
dir_loader = DirectoryLoader(docs_dir, glob="*.txt", loader_cls=TextLoader,
                              loader_kwargs={"encoding": "utf-8"})
docs = dir_loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
split_docs = splitter.split_documents(docs)
console.print(f"  加载 {len(docs)} 个文档，分割为 {len(split_docs)} 个文本块", style="green")

try:
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

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 创建 LLM
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        model=MODEL_NAME,
        temperature=0.7,
    )

    # RAG 提示词模板
    rag_prompt = ChatPromptTemplate.from_template(
        "你是一个基于文档的问答助手。请根据以下检索到的上下文来回答问题。\n"
        "如果上下文中没有相关信息，请说明你不确定。\n\n"
        "上下文：\n{context}\n\n"
        "问题：{question}\n\n"
        "回答："
    )

    # 辅助函数：将文档列表格式化为字符串
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # 构建 RAG Chain（使用 LCEL）
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    # ============================================================
    # 3. 测试 RAG Chain
    # ============================================================
    console.print("\n[bold cyan]3. 测试 RAG Chain[/bold cyan]")

    questions = [
        "Python 有什么特点？",
        "LangChain 有哪些核心组件？",
        "AI 的发展历史是怎样的？",
        "RAG 的流程是什么？",
    ]

    for q in questions:
        console.print(f"\n[bold]问：{q}[/bold]")
        console.print("-" * 50)
        # 先展示检索到的文档
        retrieved = retriever.invoke(q)
        console.print(f"  [检索到 {len(retrieved)} 个相关文档]", style="dim")
        for i, doc in enumerate(retrieved[:2]):
            source = os.path.basename(doc.metadata.get("source", "unknown"))
            console.print(f"  [{i+1}] ({source}) {doc.page_content[:60]}...", style="dim")
        # 生成回答
        answer = rag_chain.invoke(q)
        console.print(f"  答：{answer}", style="green")

    # ============================================================
    # 4. 对比：有 RAG vs 没有 RAG
    # ============================================================
    console.print("\n[bold cyan]4. 对比：有 RAG vs 没有 RAG[/bold cyan]")

    test_q = "LangChain 的 RAG 流程是什么？"

    console.print(f"\n  问题：{test_q}", style="white")

    console.print("\n  [没有 RAG - 直接问 LLM]", style="bold red")
    direct_prompt = ChatPromptTemplate.from_template("{question}")
    direct_chain = direct_prompt | llm | StrOutputParser()
    direct_answer = direct_chain.invoke({"question": test_q})
    console.print(f"  {direct_answer[:200]}...", style="red")

    console.print("\n  [有 RAG - 基于文档回答]", style="bold green")
    rag_answer = rag_chain.invoke(test_q)
    console.print(f"  {rag_answer}", style="green")

except Exception as e:
    console.print(f"  RAG Chain 构建失败：{e}", style="red")
    import traceback
    traceback.print_exc()

console.print(Panel(
    "RAG 的价值：\n"
    "  1. 让 LLM 基于最新、准确的文档回答\n"
    "  2. 减少幻觉（LLM 编造信息）\n"
    "  3. 可以引用来源，增加可信度\n"
    "  4. 无需微调模型，只需更新文档",
    title="RAG 的价值",
    style="green"
))

console.print("\nRAG Chain 演示完成！", style="bold green")
