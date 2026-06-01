"""Day 15 - 03 Embedding 演示。

这个脚本展示 RAG 的第三步：把文本转换成向量。
向量是一组数字，后续可以用它计算文本之间的相似度。
"""

import os
import sys

# 让当前脚本能够找到 modules 和 config。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.embeddings import get_embedding_model


def main():
    print("=" * 60)
    print("Embedding 演示")
    print("=" * 60)

    # 如果配置了 OPENAI_API_KEY，这里会优先使用真实 Embedding 模型；
    # 否则使用本地 SimpleEmbeddingModel。
    model = get_embedding_model()

    # 用一小段文本演示“文字 -> 向量”的过程。
    sample_text = "Python 是一门高级编程语言"
    vector = model.embed_query(sample_text)

    print(f"文本：{sample_text}")
    print(f"向量长度：{len(vector)}")

    # 只打印前 10 维，避免终端输出太长。
    print(f"前 10 维：{vector[:10]}")


if __name__ == "__main__":
    main()

