"""
Day 12 - 练习 5（综合）：RAG 效果评估

任务：对比不同 RAG 配置的效果，找到最优参数。

新增内容（标注 [新增]）：
  1. [新增] 不同 chunk_size 的 RAG 效果对比
  2. [新增] 不同检索数量 (k) 的效果对比
  3. [新增] RAG 质量评估指标
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
from rich.table import Table
from rich.panel import Panel

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 12 - 练习 5：RAG 效果评估", style="bold blue")
console.print("=" * 60, style="bold blue")

current_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(current_dir, "documents")
dir_loader = DirectoryLoader(docs_dir, glob="*.txt", loader_cls=TextLoader,
                              loader_kwargs={"encoding": "utf-8"})
docs = dir_loader.load()

test_question = "Python 有什么特点和应用领域？"

try:
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_BASE_URL)
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, model=MODEL_NAME, temperature=0.7)

    rag_prompt = ChatPromptTemplate.from_template(
        "根据以下上下文回答问题。\n\n上下文：\n{context}\n\n问题：{question}\n\n回答："
    )
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # [新增] 1. 不同 chunk_size 对比
    console.print("\n[bold cyan][新增] 1. 不同 chunk_size 的 RAG 效果对比[/bold cyan]")
    console.print(f"测试问题：{test_question}\n")

    result_table = Table(title="chunk_size 效果对比", show_header=True)
    result_table.add_column("chunk_size", style="cyan", width=12)
    result_table.add_column("文本块数", style="yellow", width=10)
    result_table.add_column("检索结果数", style="green", width=12)
    result_table.add_column("回答预览", style="white", width=50)

    for chunk_size in [100, 200, 400]:
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=50)
        split_docs = splitter.split_documents(docs)
        vs = Chroma.from_documents(split_docs, embeddings)
        ret = vs.as_retriever(search_kwargs={"k": 3})

        retrieved = ret.invoke(test_question)
        chain = ({"context": ret | format_docs, "question": RunnablePassthrough()} | rag_prompt | llm | StrOutputParser())
        answer = chain.invoke(test_question)

        result_table.add_row(str(chunk_size), str(len(split_docs)), str(len(retrieved)), answer[:50] + "...")

    console.print(result_table)

    # [新增] 2. 不同 k 值对比
    console.print("\n[bold cyan][新增] 2. 不同检索数量 k 的效果对比[/bold cyan]")

    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)
    vs = Chroma.from_documents(split_docs, embeddings)

    k_table = Table(title="检索数量 k 对比", show_header=True)
    k_table.add_column("k", style="cyan", width=6)
    k_table.add_column("检索内容预览", style="yellow", width=60)

    for k in [1, 3, 5]:
        ret = vs.as_retriever(search_kwargs={"k": k})
        results = ret.invoke(test_question)
        preview = " | ".join(r.page_content[:30] for r in results[:3])
        k_table.add_row(str(k), preview + "...")

    console.print(k_table)

    # [新增] 3. 评估建议
    console.print(Panel(
        "[bold]RAG 效果评估维度：[/bold]\n\n"
        "  1. 检索相关性：检索到的文档是否与问题相关？\n"
        "  2. 回答准确性：回答是否基于检索到的文档？\n"
        "  3. 回答完整性：回答是否完整覆盖了问题？\n"
        "  4. 幻觉检测：回答中是否有编造的信息？\n\n"
        "[bold]优化建议：[/bold]\n"
        "  - chunk_size: 200-500（中文场景）\n"
        "  - chunk_overlap: 10%-20%\n"
        "  - k: 3-5（大多数场景足够）\n"
        "  - 使用 MMR 提高多样性",
        title="RAG 评估与优化",
        style="green"
    ))

except Exception as e:
    console.print(f"  操作失败：{e}", style="red")

console.print("\n练习 5 完成！", style="bold green")
