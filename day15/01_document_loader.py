"""Day 15 - 01 文档加载演示"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.loader import load_documents


def main():
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    print("=" * 60)
    print("文档加载演示")
    print("=" * 60)
    print(f"加载到 {len(documents)} 份文档")
    for doc in documents:
        print(f"- {doc.metadata['source']}: {doc.page_content[:80]}...")


if __name__ == "__main__":
    main()

