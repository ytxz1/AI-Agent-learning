"""Day 15 - RAG 基础项目入口"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.rag_chain import RAGChain
from modules.retriever import Retriever
from modules.splitter import split_documents
from modules.vector_store import SimpleVectorStore
from config import CHUNK_OVERLAP, CHUNK_SIZE, TOP_K


def build_rag_system():
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    chunks = split_documents(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    embedding_model = get_embedding_model()
    vector_store = SimpleVectorStore(embedding_model)
    vector_store.add_documents(chunks)
    retriever = Retriever(vector_store, top_k=TOP_K)
    rag_chain = RAGChain(retriever)
    return documents, chunks, rag_chain


def main():
    print("=" * 60)
    print("Day 15 - RAG 基础项目")
    print("=" * 60)

    documents, chunks, rag_chain = build_rag_system()
    print(f"已加载文档数量：{len(documents)}")
    print(f"已切分文本块数量：{len(chunks)}")

    if not documents:
        print("documents 目录中没有可用文档。")
        return

    examples = [
        "什么是 RAG？",
        "Python 有什么特点？",
        "为什么要把文档切分成小块？",
    ]

    for question in examples:
        print("\n用户：", question)
        answer = rag_chain.answer(question)
        print("助手：", answer)


if __name__ == "__main__":
    main()

