"""简单向量库存储与检索。

真实 RAG 项目通常会用 FAISS、Chroma、Milvus 等向量数据库。
Day 15 为了让你先理解原理，这里自己实现一个最小版内存向量库。
它会保存文本块和对应向量，并用余弦相似度找出最相关的内容。
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple

try:
    from .loader import DocumentItem
except ImportError:
    from loader import DocumentItem


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """计算两个向量的余弦相似度。

    返回值越接近 1，表示两个向量方向越接近，也就是文本语义越相似。
    """

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


@dataclass
class SearchResult:
    """一次检索返回的结果对象。"""

    document: DocumentItem
    score: float


class SimpleVectorStore:
    """最小可用的内存向量库。"""

    def __init__(self, embedding_model):
        # embedding_model 负责把文本转成向量。
        self.embedding_model = embedding_model

        # documents 保存原始文本块。
        self.documents: List[DocumentItem] = []

        # vectors 保存每个文本块对应的向量，顺序和 documents 一一对应。
        self.vectors: List[List[float]] = []

    def add_documents(self, documents: List[DocumentItem]):
        """把一批文本块加入向量库。"""

        self.documents.extend(documents)
        texts = [doc.page_content for doc in documents]

        # 有些 Embedding 模型支持批量 embed_documents，有些只支持单条 embed_query。
        if hasattr(self.embedding_model, "embed_documents"):
            vectors = self.embedding_model.embed_documents(texts)
        else:
            vectors = [self.embedding_model.embed_query(text) for text in texts]

        self.vectors.extend(vectors)

    def similarity_search(self, query: str, k: int = 3) -> List[SearchResult]:
        """根据用户问题检索最相似的 k 个文本块。"""

        if not self.documents:
            return []

        # 先把用户问题也变成向量，这样才能和文档向量比较。
        query_vector = self.embedding_model.embed_query(query)
        scored: List[Tuple[float, DocumentItem]] = []

        for doc, vector in zip(self.documents, self.vectors):
            score = _cosine_similarity(query_vector, vector)
            scored.append((score, doc))

        # 按相似度从高到低排序。
        scored.sort(key=lambda item: item[0], reverse=True)

        return [SearchResult(document=doc, score=score) for score, doc in scored[:k]]

