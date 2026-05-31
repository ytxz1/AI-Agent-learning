"""Day 15 - 02 文本切分演示"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.loader import load_documents
from modules.splitter import split_documents
from config import CHUNK_OVERLAP, CHUNK_SIZE


def main():
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)

    print("=" * 60)
    print("文本切分演示")
    print("=" * 60)
    print(f"原始文档数量：{len(documents)}")
    print(f"切分后文本块数量：{len(chunks)}")
    for idx, chunk in enumerate(chunks[:5], 1):
        print(f"\nChunk {idx} | source={chunk.metadata['source']} | index={chunk.metadata['chunk_index']}")
        print(chunk.page_content)


if __name__ == "__main__":
    main()

