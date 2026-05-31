"""
Day 12 - 练习 3（进阶）：构建自定义知识库

任务：创建自己的知识库文件，构建 RAG 问答系统。

新增内容（标注 [新增]）：
  1. [新增] 创建自定义知识库文档
  2. [新增] 构建完整的 RAG 问答链
  3. [新增] 对比有 RAG 和无 RAG 的回答
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME, EMBEDDING_MODEL
from rich.console import Console
from rich.panel import Panel

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 12 - 练习 3：构建自定义知识库", style="bold blue")
console.print("=" * 60, style="bold blue")

# [新增] 1. 创建自定义知识库
console.print("\n[bold cyan][新增] 1. 创建自定义知识库[/bold cyan]")

custom_docs = [
    Document(page_content="RAG 是 Retrieval Augmented Generation 的缩写，即检索增强生成。它结合了信息检索和文本生成两种技术，让 LLM 能够基于外部知识库回答问题。", metadata={"source": "custom_kb", "topic": "RAG"}),
    Document(page_content="RAG 的核心流程包括：文档加载、文本分割、向量嵌入、向量存储、相似度检索、上下文增强生成。每个步骤都影响最终的问答质量。", metadata={"source": "custom_kb", "topic": "RAG流程"}),
    Document(page_content="向量嵌入是将文本转换为数字向量的过程。语义相似的文本会被映射到向量空间中相近的位置。常用的嵌入模型有 OpenAI Embedding、BGE、M3E 等。", metadata={"source": "custom_kb", "topic": "Embedding"}),
    Document(page_content="向量数据库是专门存储和检索高维向量的数据库。常见的有 ChromaDB、FAISS、Pinecone、Weaviate。ChromaDB 适合本地开发，FAISS 性能最好。", metadata={"source": "custom_kb", "topic": "VectorDB"}),
    Document(page_content="文本分割是 RAG 中的关键步骤。chunk_size 太大会导致检索不精确，太小会丢失上下文。推荐 chunk_size=200-500，overlap=10%-20%。", metadata={"source": "custom_kb", "topic": "TextSplit"}),
]

console.print(f"  创建了 {len(custom_docs)} 个自定义知识文档", style="green")
for doc in custom_docs:
    console.print(f"  - [{doc.metadata['topic']}] {doc.page_content[:50]}...", style="white")

# [新增] 2. 构建 RAG 问答链
console.print("\n[bold cyan][新增] 2. 构建 RAG 问答链[/bold cyan]")

try:
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_BASE_URL)
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, model=MODEL_NAME, temperature=0.7)

    # 分割
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    split_docs = splitter.split_documents(custom_docs)

    # 向量存储
    vectorstore = Chroma.from_documents(split_docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # RAG Chain
    rag_prompt = ChatPromptTemplate.from_template(
        "根据以下上下文回答问题。如果上下文中没有相关信息，请说明。\n\n"
        "上下文：\n{context}\n\n问题：{question}\n\n回答："
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = ({"context": retriever | format_docs, "question": RunnablePassthrough()} | rag_prompt | llm | StrOutputParser())

    # [新增] 3. 对比测试
    console.print("\n[bold cyan][新增] 3. 对比：有 RAG vs 无 RAG[/bold cyan]")

    test_q = "什么是 RAG？它的核心流程是什么？"
    console.print(f"\n  问题：{test_q}", style="white")

    # 无 RAG
    console.print("\n  [无 RAG]", style="bold red")
    direct = (ChatPromptTemplate.from_template("{question}") | llm | StrOutputParser())
    r1 = direct.invoke({"question": test_q})
    console.print(f"  {r1[:200]}...", style="red")

    # 有 RAG
    console.print("\n  [有 RAG]", style="bold green")
    r2 = rag_chain.invoke(test_q)
    console.print(f"  {r2}", style="green")

except Exception as e:
    console.print(f"  操作失败：{e}", style="red")

console.print("\n练习 3 完成！", style="bold green")
