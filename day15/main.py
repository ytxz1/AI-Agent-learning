"""Day 15 - RAG 基础项目入口。

如果你只想看 Day 15 的完整效果，直接运行这个文件即可：
python main.py
"""

import os
import sys

# 把 day15 目录加入 sys.path，保证从 VS Code 或终端直接运行都不会导入失败。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.rag_chain import RAGChain
from modules.retriever import Retriever
from modules.splitter import split_documents
from modules.vector_store import SimpleVectorStore
from config import CHUNK_OVERLAP, CHUNK_SIZE, TOP_K


def build_rag_system():
    """构建完整 RAG 系统，并返回中间结果。

    返回 documents 和 chunks 是为了让 main() 可以打印统计信息；
    返回 rag_chain 是为了后续直接问答。
    """

    # 1. 找到 documents 文件夹。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")

    # 2. 加载知识库文档。
    documents = load_documents(docs_dir)

    # 3. 切分文本，减少单个文本块长度。
    chunks = split_documents(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    # 4. 获取 Embedding 模型。
    embedding_model = get_embedding_model()

    # 5. 创建向量库，并把 chunks 写入向量库。
    vector_store = SimpleVectorStore(embedding_model)
    vector_store.add_documents(chunks)

    # 6. 创建检索器。
    retriever = Retriever(vector_store, top_k=TOP_K)

    # 7. 创建 RAG 问答链。
    rag_chain = RAGChain(retriever)

    return documents, chunks, rag_chain


def main():
    print("=" * 60)
    print("Day 15 - RAG 基础项目")
    print("=" * 60)

    # 构建完整系统。
    documents, chunks, rag_chain = build_rag_system()

    print(f"已加载文档数量：{len(documents)}")
    print(f"已切分文本块数量：{len(chunks)}")

    # 如果 documents 目录为空，后面就没有资料可以检索。
    if not documents:
        print("documents 目录中没有可用文档。")
        return

    # 示例问题：用来验证 RAG 是否能从本地知识库里找到信息。
    examples = [
        "什么是 RAG？",
        "Python 有什么特点？",
        "为什么要把文档切分成小块？",
    ]

    for question in examples:
        print("\n用户：", question)

        # RAGChain 会自动完成“检索资料 + 生成回答”。
        answer = rag_chain.answer(question)
        print("助手：", answer)


if __name__ == "__main__":
    main()

