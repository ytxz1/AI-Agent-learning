"""Day 19 - RAG 问答系统：向量嵌入 Embedding。

本文件演示：
1. 什么是向量嵌入；
2. 如何调用在线 Embedding 模型；
3. 为什么有 API Key 也可能 404；
4. 在线模型失败时，如何使用本地模拟向量继续学习相似度计算。

重要提醒：
- API Key 只代表“你有访问凭证”；
- 404 通常代表“接口地址或模型不存在/不支持”；
- DeepSeek 的聊天模型地址不一定支持 Embedding 接口；
- 如果你要用 OpenAI 官方 embedding，通常需要：
  EMBEDDING_BASE_URL=https://api.openai.com/v1
  EMBEDDING_MODEL=text-embedding-3-small
"""

from __future__ import annotations

import hashlib
import math
import os
import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


# 让这个文件无论从 day19 目录运行，还是从项目根目录运行，都能导入 config。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import EMBEDDING_BASE_URL, EMBEDDING_MODEL, OPENAI_API_KEY


console = Console()


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算两个向量的余弦相似度。

    余弦相似度越接近 1，说明两个向量方向越接近，也就是文本语义越相似。
    """

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def local_embedding(text: str, dimension: int = 64) -> list[float]:
    """生成一个本地模拟向量。

    这个函数不是为了替代真实 Embedding 模型，而是为了在 API 调用失败时，
    仍然可以继续演示“文本 -> 向量 -> 相似度计算”的核心流程。

    做法：
    - 使用文本的字符片段生成 hash；
    - 把 hash 映射到固定维度向量；
    - 最后做归一化。
    """

    vector = [0.0] * dimension
    tokens = [text[i : i + 2] for i in range(max(len(text) - 1, 1))]

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = digest[0] % dimension
        value = (digest[1] / 255.0) * 2 - 1
        vector[index] += value

    norm = math.sqrt(sum(x * x for x in vector)) or 1.0
    return [x / norm for x in vector]


def build_online_embeddings():
    """创建在线 Embedding 模型。

    如果配置的是不支持 embeddings 的 base_url，这里创建对象可能成功，
    但真正调用 embed_query / embed_documents 时仍然会失败。
    """

    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=EMBEDDING_BASE_URL,
    )


def explain_common_404_reasons(error: Exception) -> None:
    """解释 Embedding 404 的常见原因。"""

    console.print(f"  在线 Embedding 调用失败：{error}", style="red")
    console.print("\n  这通常不是因为你没有 API Key，而是下面原因之一：", style="yellow")
    console.print("  1. EMBEDDING_BASE_URL 不支持 /embeddings 接口。", style="yellow")
    console.print("  2. EMBEDDING_MODEL 在当前服务商不存在。", style="yellow")
    console.print("  3. 聊天模型服务商和 Embedding 模型服务商混用了。", style="yellow")
    console.print("  4. 第三方中转接口只支持 chat completions，不支持 embeddings。", style="yellow")
    console.print("\n  当前配置：", style="cyan")
    console.print(f"  EMBEDDING_BASE_URL = {EMBEDDING_BASE_URL}", style="cyan")
    console.print(f"  EMBEDDING_MODEL    = {EMBEDDING_MODEL}", style="cyan")


def print_similarity_table(texts: list[str], vectors: list[list[float]], title: str) -> None:
    """打印文本相似度矩阵。"""

    sim_table = Table(title=title, show_header=True)
    sim_table.add_column("", style="cyan", width=25)
    for text in texts:
        sim_table.add_column(text[:12], style="green", width=12)

    for i, text_a in enumerate(texts):
        row = [text_a[:25]]
        for j, _ in enumerate(texts):
            row.append(f"{cosine_similarity(vectors[i], vectors[j]):.4f}")
        sim_table.add_row(*row)

    console.print(sim_table)


def main() -> None:
    """运行向量嵌入演示。"""

    console.print("=" * 60, style="bold blue")
    console.print("Day 19 - 向量嵌入", style="bold blue")
    console.print("=" * 60, style="bold blue")

    console.print("\n[bold cyan]1. 什么是向量嵌入[/bold cyan]")
    console.print(
        Panel(
            "向量嵌入（Embedding）是将文本转换为数字向量的过程。\n\n"
            "例如：\n"
            "  '猫' -> [0.2, 0.8, -0.1, ...]\n"
            "  '狗' -> [0.3, 0.7, -0.2, ...]\n"
            "  '汽车' -> [-0.5, 0.1, 0.9, ...]\n\n"
            "语义相似的文本，向量更接近：\n"
            "  猫 和 狗 的向量距离近（都是宠物）\n"
            "  猫 和 汽车 的向量距离远（无关概念）",
            title="向量嵌入",
            style="cyan",
        )
    )

    texts = [
        "Python 是一种编程语言",
        "Python 是高级开发语言",
        "今天天气很好",
    ]

    console.print("\n[bold cyan]2. 使用 Embedding 模型[/bold cyan]")

    vectors: list[list[float]]
    source: str

    if not OPENAI_API_KEY:
        console.print("  没有检测到 OPENAI_API_KEY，使用本地模拟向量。", style="yellow")
        vectors = [local_embedding(text) for text in texts]
        source = "本地模拟向量"
    else:
        try:
            embeddings = build_online_embeddings()
            vector = embeddings.embed_query(texts[0])
            console.print(f"  文本：{texts[0]}", style="white")
            console.print(f"  向量维度：{len(vector)}", style="green")
            console.print(f"  前 5 个值：{vector[:5]}", style="yellow")

            vectors = embeddings.embed_documents(texts)
            source = f"在线模型：{EMBEDDING_MODEL}"
        except Exception as error:
            explain_common_404_reasons(error)
            console.print("\n  为了继续学习核心概念，下面自动切换到本地模拟向量。", style="green")
            vectors = [local_embedding(text) for text in texts]
            source = "本地模拟向量"

    console.print(f"\n  当前向量来源：{source}", style="bold green")
    console.print(f"  文本数量：{len(texts)}", style="white")
    console.print(f"  向量维度：{len(vectors[0])}", style="white")

    console.print("\n[bold cyan]3. 计算向量相似度（余弦相似度）[/bold cyan]")
    print_similarity_table(texts, vectors, "文本相似度矩阵")

    console.print(
        Panel(
            "相似度解释：\n"
            "  1.0 = 完全相同\n"
            "  0.8+ = 高度相似\n"
            "  0.5-0.8 = 有一定关联\n"
            "  <0.5 = 关联较弱\n\n"
            "真实 Embedding 模型的语义效果会比本地模拟向量更好。\n"
            "本地模拟向量只是为了保证没有可用 embedding API 时，代码仍然能跑通。",
            title="相似度解释",
            style="green",
        )
    )

    console.print("\n[bold cyan]4. 如果你想修复在线 Embedding[/bold cyan]")
    console.print("  方案 A：使用 OpenAI 官方 embedding：", style="white")
    console.print("    EMBEDDING_BASE_URL=https://api.openai.com/v1", style="cyan")
    console.print("    EMBEDDING_MODEL=text-embedding-3-small", style="cyan")
    console.print("  方案 B：继续用 DeepSeek 聊天，但 embedding 改用其他支持 /embeddings 的服务。", style="white")
    console.print("  方案 C：暂时使用本地模拟向量，先学习 RAG 流程。", style="white")

    console.print("\n向量嵌入演示完成！", style="bold green")


if __name__ == "__main__":
    # 练习题答案：
    # 为什么有 API Key 还会 404？
    # 答案：API Key 只说明你有权限，但当前 base_url 和 model 必须真的支持 embeddings。
    # 如果服务商只支持聊天模型，不支持 /embeddings，或者模型名不存在，就会返回 404。
    main()
