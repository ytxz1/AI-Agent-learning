"""简单向量库存储与检索"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple

from .loader import DocumentItem


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


@dataclass
class SearchResult:
    document: DocumentItem
    score: float


class SimpleVectorStore:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.documents: List[DocumentItem] = []
        self.vectors: List[List[float]] = []

    def add_documents(self, documents: List[DocumentItem]):
        self.documents.extend(documents)
        texts = [doc.page_content for doc in documents]
        if hasattr(self.embedding_model, "embed_documents"):
            vectors = self.embedding_model.embed_documents(texts)
        else:
            vectors = [self.embedding_model.embed_query(text) for text in texts]
        self.vectors.extend(vectors)

    def similarity_search(self, query: str, k: int = 3) -> List[SearchResult]:
        if not self.documents:
            return []

        query_vector = self.embedding_model.embed_query(query)
        scored: List[Tuple[float, DocumentItem]] = []
        for doc, vector in zip(self.documents, self.vectors):
            score = _cosine_similarity(query_vector, vector)
            scored.append((score, doc))
        scored.sort(key=lambda item: item[0], reverse=True)

        return [SearchResult(document=doc, score=score) for score, doc in scored[:k]]

