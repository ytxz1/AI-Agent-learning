"""Day 15 - 04 向量库演示。

这个脚本展示 RAG 的第四步：把文本块和向量存入向量库，
然后根据用户问题搜索最相似的文本块。
"""

import os
import sys

# 保证当前脚本可以正常导入 day15 内部模块。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.splitter import split_documents
from modules.vector_store import SimpleVectorStore


def main():
    # 1. 加载文档。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)

    # 2. 切分文档。
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)

    # 3. 获取 Embedding 模型。
    embedding_model = get_embedding_model()

    # 4. 创建向量库，并把切分后的文本块加入向量库。
    store = SimpleVectorStore(embedding_model)
    store.add_documents(chunks)

    print("=" * 60)
    print("向量库存储与搜索演示")
    print("=" * 60)

    # 用一个固定问题演示相似度搜索。
    question = "什么是 RAG？"
    results = store.similarity_search(question, k=3)

    print("问题：", question)
    for idx, item in enumerate(results, 1):
        print(f"\n结果 {idx} | score={item.score:.4f} | source={item.document.metadata['source']}")
        print(item.document.page_content[:180])


if __name__ == "__main__":
    main()

