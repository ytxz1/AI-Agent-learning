"""
Day 13 - RAG 模块：文档检索问答

整合 Day 12 的 RAG 知识，构建文档问答系统。
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from config import OPENAI_API_KEY, OPENAI_BASE_URL, EMBEDDING_MODEL
from rich.console import Console

console = Console()


class RAGModule:
    """RAG 文档问答模块

    功能：
    1. 加载文档目录
    2. 分割文本
    3. 向量化存储
    4. 检索问答
    """

    def __init__(self, docs_dir: str = None, llm=None):
        """
        初始化 RAG 模块。

        参数:
            docs_dir: 文档目录路径，默认为 documents/
            llm: LLM 实例（可选，由 Agent 传入）
        """
        self.docs_dir = docs_dir or os.path.join(os.path.dirname(__file__), "documents")
        self.llm = llm
        self.retriever = None
        self.chain = None
        self.document_count = 0
        self.chunk_count = 0
        self._initialized = False

    def init(self):
        """初始化 RAG 系统：加载文档 -> 分割 -> 向量化"""
        try:
            # 检查文档目录
            if not os.path.exists(self.docs_dir):
                return "文档目录不存在"

            # 加载文档
            loader = DirectoryLoader(self.docs_dir, glob="*.txt",
                                      loader_cls=TextLoader,
                                      loader_kwargs={"encoding": "utf-8"})
            docs = loader.load()
            if not docs:
                return "文档目录为空"
            self.document_count = len(docs)

            # 分割
            splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
            split_docs = splitter.split_documents(docs)
            self.chunk_count = len(split_docs)

            # 向量化
            embeddings = OpenAIEmbeddings(
                model=EMBEDDING_MODEL,
                openai_api_key=OPENAI_API_KEY,
                openai_api_base=OPENAI_BASE_URL,
            )
            persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
            vs = Chroma.from_documents(split_docs, embeddings, persist_directory=persist_dir)
            self.retriever = vs.as_retriever(search_kwargs={"k": 3})

            self._initialized = True
            return f"初始化完成：{self.document_count} 个文档，{self.chunk_count} 个文本块"

        except Exception as e:
            self._initialized = False
            return f"初始化失败：{e}"

    def query(self, question: str) -> str:
        """基于文档回答问题"""
        if not self._initialized or not self.retriever:
            return "RAG 系统未初始化"

        try:
            # 检索
            docs = self.retriever.invoke(question)

            # 构建上下文
            context = "\n\n".join(d.page_content for d in docs)

            # 用 LLM 生成回答
            if self.llm:
                prompt = ChatPromptTemplate.from_template(
                    "根据以下上下文回答问题。如果找不到相关信息，请说明。\n\n上下文：{context}\n\n问题：{question}\n\n回答："
                )
                chain = prompt | self.llm | StrOutputParser()
                return chain.invoke({"context": context, "question": question})
            else:
                return f"检索到 {len(docs)} 个相关文档，但未配置 LLM"

        except Exception as e:
            return f"RAG 查询失败：{e}"

    def search_only(self, query: str) -> list:
        """仅检索文档，不调用 LLM"""
        if not self._initialized or not self.retriever:
            return []
        return self.retriever.invoke(query)


if __name__ == "__main__":
    console.print("=" * 60, style="bold blue")
    console.print("Day 13 - RAG 模块测试", style="bold blue")
    console.print("=" * 60, style="bold blue")

    rag = RAGModule()
    result = rag.init()
    console.print(f"  {result}", style="green")

    if rag._initialized:
        console.print("\n[bold cyan]测试检索：[/bold cyan]")
        results = rag.search_only("Python")
        for i, d in enumerate(results):
            console.print(f"  [{i+1}] {d.page_content[:60]}...", style="yellow")

    console.print("\n[bold green]RAG 模块测试完成[/bold green]")
