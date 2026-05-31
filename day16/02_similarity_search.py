"""练习 2：相似度搜索。"""

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
    # 先构建向量库，然后查询一个问题。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    store = PersistentVectorStore(get_embedding_model(), VECTOR_DB_FILE)
    store.add_documents(chunks)
    demo = SearchDemo(store, TOP_K)
    question = "什么是向量数据库？"
    results = demo.search(question)
    print(demo.format_results(results))

