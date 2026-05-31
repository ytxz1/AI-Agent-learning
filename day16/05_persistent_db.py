"""练习 5：持久化向量库。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE, VECTOR_DB_FILE
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.splitter import split_documents
from modules.vector_store import PersistentVectorStore


if __name__ == "__main__":
    # 先保存，再重新加载，看看数据是否还在。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    store = PersistentVectorStore(get_embedding_model(), VECTOR_DB_FILE)
    store.add_documents(chunks)
    store.save()

    reload_store = PersistentVectorStore(get_embedding_model(), VECTOR_DB_FILE)
    reload_store.load()
    print("重新加载后的统计：", reload_store.stats())

