"""Day 15 - 05 检索器演示"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE, TOP_K
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.retriever import Retriever
from modules.splitter import split_documents
from modules.vector_store import SimpleVectorStore


def main():
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    embedding_model = get_embedding_model()
    store = SimpleVectorStore(embedding_model)
    store.add_documents(chunks)
    retriever = Retriever(store, TOP_K)

    question = "为什么要切分文本？"
    results = retriever.retrieve(question)

    print("=" * 60)
    print("检索器演示")
    print("=" * 60)
    print("问题：", question)
    for idx, item in enumerate(results, 1):
        print(f"\nTop {idx} | score={item.score:.4f} | source={item.document.metadata['source']}")
        print(item.document.page_content)


if __name__ == "__main__":
    main()

