"""
Day 19 - 项目 2：RAG 问答系统 - 向量嵌入

本示例演示 Embedding 的核心概念：
1. 什么是向量嵌入
2. 为什么需要嵌入
3. 使用 OpenAI/DeepSeek 的 Embedding 模型
4. 向量相似度计算

知识点：
1. Embedding 将文本映射到高维向量空间
2. 语义相似的文本，向量距离更近
3. 余弦相似度是最常用的相似度度量
"""

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import OPENAI_API_KEY, OPENAI_BASE_URL, EMBEDDING_MODEL
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 19 - 向量嵌入", style="bold blue")
console.print("=" * 60, style="bold blue")

# ============================================================
# 1. 什么是向量嵌入
# ============================================================
console.print("\n[bold cyan]1. 什么是向量嵌入[/bold cyan]")
console.print(Panel(
    "向量嵌入（Embedding）是将文本转换为数字向量的过程。\n\n"
    "例如：\n"
    "  '猫' -> [0.2, 0.8, -0.1, ...]  (1536 维)\n"
    "  '狗' -> [0.3, 0.7, -0.2, ...]  (1536 维)\n"
    "  '汽车' -> [-0.5, 0.1, 0.9, ...] (1536 维)\n\n"
    "语义相似的文本，向量更接近：\n"
    "  猫 和 狗 的向量距离近（都是宠物）\n"
    "  猫 和 汽车 的向量距离远（无关概念）",
    title="向量嵌入",
    style="cyan"
))

# ============================================================
# 2. 使用 Embedding 模型
# ============================================================
console.print("\n[bold cyan]2. 使用 Embedding 模型[/bold cyan]")

try:
    from langchain_openai import OpenAIEmbeddings

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_BASE_URL,
    )

    # 生成单个文本的嵌入
    text = "Python 是一种编程语言"
    vector = embeddings.embed_query(text)
    console.print(f"  文本：{text}", style="white")
    console.print(f"  向量维度：{len(vector)}", style="green")
    console.print(f"  前 5 个值：{vector[:5]}", style="yellow")

    # 批量生成嵌入
    texts = [
        "Python 是一种编程语言",
        "Python 是高级开发语言",
        "今天天气很好",
    ]
    vectors = embeddings.embed_documents(texts)
    console.print(f"\n  批量嵌入：{len(vectors)} 个文本", style="green")
    for i, (t, v) in enumerate(zip(texts, vectors)):
        console.print(f"  [{i+1}] {t} -> 维度 {len(v)}", style="white")

    # ============================================================
    # 3. 计算相似度
    # ============================================================
    console.print("\n[bold cyan]3. 计算向量相似度（余弦相似度）[/bold cyan]")

    def cosine_similarity(a, b):
        """计算两个向量的余弦相似度"""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0

    # 计算相似度矩阵
    sim_table = Table(title="文本相似度矩阵", show_header=True)
    sim_table.add_column("", style="cyan", width=25)
    for t in texts:
        sim_table.add_column(t[:12], style="green", width=12)

    for i, t1 in enumerate(texts):
        row = [t1[:25]]
        for j, t2 in enumerate(texts):
            sim = cosine_similarity(vectors[i], vectors[j])
            row.append(f"{sim:.4f}")
        sim_table.add_row(*row)

    console.print(sim_table)

    console.print(Panel(
        "相似度解读：\n"
        "  1.0 = 完全相同\n"
        "  0.8+ = 高度相似\n"
        "  0.5-0.8 = 有一定关联\n"
        "  <0.5 = 关联较弱\n\n"
        "'Python编程语言' 和 'Python高级语言' 相似度高\n"
        "'Python编程语言' 和 '今天天气' 相似度低",
        title="相似度解读",
        style="green"
    ))

except Exception as e:
    console.print(f"  Embedding 模型调用失败：{e}", style="red")
    console.print("  这可能是因为 API 密钥或网络问题", style="yellow")
    console.print("  但核心概念不变：文本 -> 向量 -> 相似度计算", style="white")

console.print("\n向量嵌入演示完成！", style="bold green")
