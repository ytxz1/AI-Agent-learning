"""练习 3：元数据过滤。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE, TOP_K, VECTOR_DB_FILE
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.search_demo import SearchDemo
from modules.splitter import split_documents
from modules.vector_store import PersistentVectorStore


if __name__ == "__main__":
    # 只搜索某个来源文件，看看过滤效果。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    store = PersistentVectorStore(get_embedding_model(), VECTOR_DB_FILE)
    store.add_documents(chunks)
    demo = SearchDemo(store, TOP_K)
    results = demo.search("RAG 是什么？", metadata_filter={"source": "rag_notes.txt"})
    print(demo.format_results(results))

