"""练习 1：把切块存入向量库。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE, VECTOR_DB_FILE
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.splitter import split_documents
from modules.vector_store import PersistentVectorStore


if __name__ == "__main__":
    # 先加载文档，再切块，最后存入向量库。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    store = PersistentVectorStore(get_embedding_model(), VECTOR_DB_FILE)
    store.add_documents(chunks)
    print("文档数量：", len(documents))
    print("文本块数量：", len(chunks))
    print("向量库统计：", store.stats())

