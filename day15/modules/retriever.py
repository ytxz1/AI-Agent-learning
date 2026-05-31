"""检索器模块"""

from __future__ import annotations

from typing import List

from .vector_store import SearchResult, SimpleVectorStore


class Retriever:
    def __init__(self, vector_store: SimpleVectorStore, top_k: int = 3):
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(self, question: str) -> List[SearchResult]:
        return self.vector_store.similarity_search(question, k=self.top_k)

