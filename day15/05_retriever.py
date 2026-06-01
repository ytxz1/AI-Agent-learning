"""Day 15 - 05 检索器演示。

这个脚本展示 RAG 的第五步：把向量库搜索封装成 Retriever。
以后 RAGChain 只需要调用 retriever.retrieve(question)，不用关心底层细节。
"""

import os
import sys

# 添加 day15 目录到 Python 模块搜索路径，避免直接运行时报导入错误。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE, TOP_K
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.retriever import Retriever
from modules.splitter import split_documents
from modules.vector_store import SimpleVectorStore


def main():
    # 前半部分仍然是标准 RAG 准备流程：
    # 加载文档 -> 切分文本 -> 获取 Embedding -> 构建向量库。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    embedding_model = get_embedding_model()
    store = SimpleVectorStore(embedding_model)
    store.add_documents(chunks)

    # Retriever 是对向量库检索能力的进一步封装。
    retriever = Retriever(store, TOP_K)

    question = "为什么要切分文本？"

    # 调用 retrieve 后会返回 Top-K 个 SearchResult。
    results = retriever.retrieve(question)

    print("=" * 60)
    print("检索器演示")
    print("=" * 60)
    print("问题：", question)

    # 打印每个检索结果的排名、相似度、来源和文本内容。
    for idx, item in enumerate(results, 1):
        print(f"\nTop {idx} | score={item.score:.4f} | source={item.document.metadata['source']}")
        print(item.document.page_content)


if __name__ == "__main__":
    main()

