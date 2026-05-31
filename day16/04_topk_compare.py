"""练习 4：对比 Top-K 效果。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE, VECTOR_DB_FILE
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.splitter import split_documents
from modules.vector_store import PersistentVectorStore


if __name__ == "__main__":
    # 对比返回 1 条和 3 条结果时的差异。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    store = PersistentVectorStore(get_embedding_model(), VECTOR_DB_FILE)
    store.add_documents(chunks)

    question = "AI Agent 为什么要结合向量检索？"
    print("Top 1：")
    for item in store.similarity_search(question, k=1):
        print(item.score, item.document.metadata, item.document.page_content)

    print("\nTop 3：")
    for item in store.similarity_search(question, k=3):
        print(item.score, item.document.metadata, item.document.page_content)

