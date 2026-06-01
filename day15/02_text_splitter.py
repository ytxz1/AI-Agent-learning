"""Day 15 - 02 文本切分演示。

这个脚本展示 RAG 的第二步：把长文档切成较短的文本块。
切分后的文本块会被送去做 Embedding 和检索。
"""

import os
import sys

# 保证直接运行当前脚本时，也可以导入 day15 下的 config 和 modules。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.loader import load_documents
from modules.splitter import split_documents
from config import CHUNK_OVERLAP, CHUNK_SIZE


def main():
    # 1. 加载原始文档。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)

    # 2. 按 config.py 中配置的 CHUNK_SIZE 和 CHUNK_OVERLAP 进行切分。
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)

    print("=" * 60)
    print("文本切分演示")
    print("=" * 60)
    print(f"原始文档数量：{len(documents)}")
    print(f"切分后文本块数量：{len(chunks)}")

    # 只展示前 5 个 chunk，避免终端输出太长。
    for idx, chunk in enumerate(chunks[:5], 1):
        print(f"\nChunk {idx} | source={chunk.metadata['source']} | index={chunk.metadata['chunk_index']}")
        print(chunk.page_content)


if __name__ == "__main__":
    main()

