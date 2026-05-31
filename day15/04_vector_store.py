"""Day 15 - 04 向量库演示"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.splitter import split_documents
from modules.vector_store import SimpleVectorStore


def main():
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    embedding_model = get_embedding_model()
    store = SimpleVectorStore(embedding_model)
    store.add_documents(chunks)

    print("=" * 60)
    print("向量库存储与搜索演示")
    print("=" * 60)
    question = "什么是 RAG？"
    results = store.similarity_search(question, k=3)
    print("问题：", question)
    for idx, item in enumerate(results, 1):
        print(f"\n结果 {idx} | score={item.score:.4f} | source={item.document.metadata['source']}")
        print(item.document.page_content[:180])


if __name__ == "__main__":
    main()

