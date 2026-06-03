"""Day 19 - RAG 问答系统：向量数据库 Chroma。

本文件演示：
1. 什么是向量数据库；
2. 如何加载和切分文档；
3. 如何把文本块存入 ChromaDB；
4. 如何做相似度搜索；
5. 为什么 Embedding 调用失败时，Chroma 也会报错。

关键说明：
- ChromaDB 本身只是向量数据库；
- 在把文档存入 ChromaDB 之前，必须先用 Embedding 模型把文本变成向量；
- 如果 Embedding 接口 404，Chroma.from_documents() 也会失败；
- 这不是 API Key 一定错了，而是 embedding base_url 或模型名不支持。
"""

from __future__ import annotations

import hashlib
import math
import os
import shutil
import sys
import warnings
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rich.console import Console
from rich.panel import Panel


# 让脚本从任意目录运行时都能导入 day19/config.py。
DAY19_DIR = Path(__file__).resolve().parent
if str(DAY19_DIR) not in sys.path:
    sys.path.insert(0, str(DAY19_DIR))

from config import EMBEDDING_BASE_URL, EMBEDDING_MODEL, OPENAI_API_KEY


console = Console()

# 屏蔽 langchain-community 当前的维护状态提示，避免干扰学习输出。
# 这不是运行错误，只是库维护方向的提醒。
warnings.filterwarnings(
    "ignore",
    message="`langchain-community` is being sunset.*",
    category=DeprecationWarning,
)


class LocalHashEmbeddings:
    """Chroma 兼容的本地模拟 Embedding 类。

    LangChain 的 Chroma 需要一个对象提供：
    - embed_documents(texts)
    - embed_query(text)

    这个类就是为了在在线 embedding 失败时兜底使用。
    它不能替代真实语义 embedding，但足够演示向量数据库的存储和检索流程。
    """

    def __init__(self, dimension: int = 64) -> None:
        self.dimension = dimension

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """把多段文本转换成向量。"""

        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        """把查询文本转换成向量。"""

        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        """使用 hash 生成固定维度向量。"""

        vector = [0.0] * self.dimension
        tokens = [text[i : i + 2] for i in range(max(len(text) - 1, 1))]

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = digest[0] % self.dimension
            value = (digest[1] / 255.0) * 2 - 1
            vector[index] += value

        norm = math.sqrt(sum(x * x for x in vector)) or 1.0
        return [x / norm for x in vector]


def load_text_documents(docs_dir: Path) -> list[Document]:
    """加载 documents 文件夹中的 txt 文档。

    这里不用 DirectoryLoader，是为了避免 langchain-community 的弃用警告干扰学习输出。
    """

    documents: list[Document] = []
    for file_path in sorted(docs_dir.glob("*.txt")):
        content = file_path.read_text(encoding="utf-8")
        documents.append(
            Document(
                page_content=content,
                metadata={"source": str(file_path)},
            )
        )
    return documents


def build_online_embeddings():
    """创建在线 Embedding 对象。"""

    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=EMBEDDING_BASE_URL,
    )


def choose_embedding_model(texts_for_test: list[str]):
    """优先使用在线 Embedding，失败时切换到本地模拟 Embedding。"""

    if not OPENAI_API_KEY:
        console.print("  未检测到 OPENAI_API_KEY，使用本地模拟 Embedding。", style="yellow")
        return LocalHashEmbeddings(), "本地模拟 Embedding"

    try:
        embeddings = build_online_embeddings()
        # 主动测试一次，避免 Chroma.from_documents 里面才报错导致原因不清楚。
        test_vector = embeddings.embed_query(texts_for_test[0])
        console.print(f"  在线 Embedding 测试成功，维度：{len(test_vector)}", style="green")
        return embeddings, f"在线 Embedding：{EMBEDDING_MODEL}"
    except Exception as error:
        console.print(f"  在线 Embedding 调用失败：{error}", style="red")
        console.print("  这通常说明 embedding 接口地址或模型名不支持，而不是 ChromaDB 未安装。", style="yellow")
        console.print(f"  当前 EMBEDDING_BASE_URL = {EMBEDDING_BASE_URL}", style="cyan")
        console.print(f"  当前 EMBEDDING_MODEL    = {EMBEDDING_MODEL}", style="cyan")
        console.print("  自动切换到本地模拟 Embedding，继续演示 ChromaDB。", style="green")
        return LocalHashEmbeddings(), "本地模拟 Embedding"


def reset_demo_chroma_dir(persist_dir: Path) -> None:
    """清理旧的演示数据库，避免维度不一致导致 Chroma 报错。

    如果之前用 1536 维在线向量建过库，这次用 64 维本地向量继续写入，
    Chroma 会因为集合维度不一致而失败。所以演示脚本每次先清理旧目录。
    """

    if persist_dir.exists():
        shutil.rmtree(persist_dir)


def main() -> None:
    """运行向量数据库演示。"""

    console.print("=" * 60, style="bold blue")
    console.print("Day 19 - 向量数据库", style="bold blue")
    console.print("=" * 60, style="bold blue")

    console.print("\n[bold cyan]1. 什么是向量数据库[/bold cyan]")
    console.print(
        Panel(
            "向量数据库是专门存储和检索高维向量的数据库。\n\n"
            "传统数据库：SELECT * WHERE name = 'Python'（精确匹配）\n"
            "向量数据库：找到与查询最相似的 K 个结果（语义搜索）\n\n"
            "常用向量数据库：\n"
            "  - ChromaDB：轻量级，适合本地开发\n"
            "  - FAISS：本地高性能向量检索\n"
            "  - Pinecone：云端托管服务\n"
            "  - Weaviate：开源，支持多种搜索",
            title="向量数据库",
            style="cyan",
        )
    )

    console.print("\n[bold cyan]2. 准备文档数据[/bold cyan]")
    docs_dir = DAY19_DIR / "documents"
    docs = load_text_documents(docs_dir)

    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    console.print(f"  加载 {len(docs)} 个文档，分割为 {len(split_docs)} 个文本块", style="green")

    console.print("\n[bold cyan]3. 使用 ChromaDB 存储向量[/bold cyan]")
    try:
        from langchain_community.vectorstores import Chroma
    except Exception as error:
        console.print(f"  ChromaDB 导入失败：{error}", style="red")
        console.print("  请先安装依赖：pip install chromadb langchain-community", style="yellow")
        return

    embeddings, embedding_source = choose_embedding_model([doc.page_content for doc in split_docs])
    console.print(f"  当前 Embedding 来源：{embedding_source}", style="green")

    persist_dir = DAY19_DIR / "chroma_db_demo"
    reset_demo_chroma_dir(persist_dir)

    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=str(persist_dir),
    )

    console.print(f"  已将 {len(split_docs)} 个文本块存入 ChromaDB", style="green")
    console.print(f"  数据库路径：{persist_dir}", style="dim")

    console.print("\n[bold cyan]4. 相似度搜索[/bold cyan]")
    query = "Python 有什么特点？"
    console.print(f"  查询：{query}", style="white")

    results = vectorstore.similarity_search(query, k=3)
    console.print(f"  找到 {len(results)} 个相关结果：", style="green")
    for index, doc in enumerate(results, start=1):
        source = Path(doc.metadata.get("source", "unknown")).name
        preview = doc.page_content.replace("\n", " ")[:90]
        console.print(f"  [{index}] ({source}) {preview}...", style="yellow")

    console.print("\n[bold cyan]5. 带分数的搜索[/bold cyan]")
    results_with_scores = vectorstore.similarity_search_with_score(query, k=3)
    for index, (doc, score) in enumerate(results_with_scores, start=1):
        source = Path(doc.metadata.get("source", "unknown")).name
        preview = doc.page_content.replace("\n", " ")[:70]
        console.print(f"  [{index}] 分数={score:.4f} ({source}) {preview}...", style="yellow")

    console.print(
        Panel(
            "注意：\n"
            "  - 如果使用真实 Embedding，搜索结果会更符合语义。\n"
            "  - 如果当前自动切换到了本地模拟 Embedding，结果只用于学习流程。\n"
            "  - ChromaDB 报 404 通常不是数据库问题，而是前面的 Embedding API 调用失败。",
            title="学习提示",
            style="green",
        )
    )

    console.print("\n向量数据库演示完成！", style="bold green")


if __name__ == "__main__":
    # 练习题答案：
    # 为什么 04_vector_store.py 会因为 Embedding 失败而报错？
    # 答案：向量数据库保存的是“向量”，不是原始文本。
    # Chroma.from_documents 会先调用 embedding.embed_documents() 生成向量。
    # 如果 embedding 接口 404，Chroma 自然也无法继续创建向量库。
    main()
