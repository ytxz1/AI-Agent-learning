"""Day 15 - 06 RAG Chain 演示"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE, TOP_K
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.rag_chain import RAGChain
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
    rag_chain = RAGChain(retriever)

    print("=" * 60)
    print("RAG Chain 演示")
    print("=" * 60)

    questions = [
        "什么是 RAG？",
        "Python 的特点是什么？",
        "AI Agent 有什么作用？",
    ]

    for question in questions:
        print("\n用户：", question)
        answer = rag_chain.answer(question)
        print("助手：", answer)


if __name__ == "__main__":
    main()

