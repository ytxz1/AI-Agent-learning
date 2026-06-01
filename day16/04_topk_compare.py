"""练习 4：对比 Top-K 效果。

练习目标：
理解 Top-K 的意义：返回 1 条结果和返回 3 条结果，给后续 RAG 的信息量不同。

参考答案：
分别调用 similarity_search(question, k=1) 和 similarity_search(question, k=3)，
观察返回内容的数量、来源和相关性。
"""

import os
import sys

# 把 day16 加到模块搜索路径，保证导入稳定。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE, VECTOR_DB_FILE
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.splitter import split_documents
from modules.vector_store import PersistentVectorStore


if __name__ == "__main__":
    # 1. 构建向量库。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    store = PersistentVectorStore(get_embedding_model(), VECTOR_DB_FILE)
    store.add_documents(chunks)

    # 2. 准备一个测试问题。
    question = "AI Agent 为什么要结合向量检索？"

    # 3. Top 1 只返回最相关的一条，信息更集中，但可能遗漏重要上下文。
    print("Top 1：")
    for item in store.similarity_search(question, k=1):
        print(item.score, item.document.metadata, item.document.page_content)

    # 4. Top 3 返回三条相关内容，更适合后续交给大模型综合回答。
    print("\nTop 3：")
    for item in store.similarity_search(question, k=3):
        print(item.score, item.document.metadata, item.document.page_content)
