"""Day 15 - 06 RAG Chain 演示。

这个脚本展示 Day 15 的完整主线：
文档加载 -> 文本切分 -> 向量化 -> 检索 -> 根据资料回答问题。
"""

import os
import sys

# 让脚本可以从当前 day15 目录导入 config 和 modules。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE, TOP_K
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.rag_chain import RAGChain
from modules.retriever import Retriever
from modules.splitter import split_documents
from modules.vector_store import SimpleVectorStore


def main():
    # 1. 加载知识库文档。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)

    # 2. 把文档切成多个短文本块。
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)

    # 3. 获取 Embedding 模型，把文本转成向量。
    embedding_model = get_embedding_model()

    # 4. 构建向量库，并写入全部文本块。
    store = SimpleVectorStore(embedding_model)
    store.add_documents(chunks)

    # 5. 用向量库创建检索器。
    retriever = Retriever(store, TOP_K)

    # 6. 用检索器创建 RAG 问答链。
    rag_chain = RAGChain(retriever)

    print("=" * 60)
    print("RAG Chain 演示")
    print("=" * 60)

    # 用三道固定问题测试知识库问答效果。
    questions = [
        "什么是 RAG？",
        "Python 的特点是什么？",
        "AI Agent 有什么作用？",
    ]

    for question in questions:
        print("\n用户：", question)

        # answer 内部会先检索资料，再生成回答。
        answer = rag_chain.answer(question)
        print("助手：", answer)


if __name__ == "__main__":
    main()

