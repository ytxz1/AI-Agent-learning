"""Day 15 - 03 Embedding 演示"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.embeddings import get_embedding_model


def main():
    print("=" * 60)
    print("Embedding 演示")
    print("=" * 60)
    model = get_embedding_model()
    sample_text = "Python 是一门高级编程语言"
    vector = model.embed_query(sample_text)
    print(f"文本：{sample_text}")
    print(f"向量长度：{len(vector)}")
    print(f"前 10 维：{vector[:10]}")


if __name__ == "__main__":
    main()

