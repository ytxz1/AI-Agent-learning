"""练习 3：元数据过滤。

练习目标：
理解 metadata_filter 的作用：不仅要“语义相似”，还要“来源符合条件”。

参考答案：
在 search() 中传入 metadata_filter={"source": "rag_notes.txt"}，
就可以只搜索 rag_notes.txt 这个来源文件里的文本块。
"""

import os
import sys

# 支持直接运行当前脚本。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE, TOP_K, VECTOR_DB_FILE
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.search_demo import SearchDemo
from modules.splitter import split_documents
from modules.vector_store import PersistentVectorStore


if __name__ == "__main__":
    # 1. 准备完整向量库。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    store = PersistentVectorStore(get_embedding_model(), VECTOR_DB_FILE)
    store.add_documents(chunks)
    demo = SearchDemo(store, TOP_K)

    # 2. 只搜索 rag_notes.txt 这个文件来源。
    # 注意：source 的值来自 loader.py 中写入的 metadata。
    results = demo.search("RAG 是什么？", metadata_filter={"source": "rag_notes.txt"})

    print(demo.format_results(results))
