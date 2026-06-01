"""检索器模块。

Retriever 是 RAG 里的“检索员”。
它负责接收用户问题，然后调用向量库找出最相关的文本块。
把检索逻辑单独封装成类，可以让后面的 RAGChain 不用关心底层向量库细节。
"""

from __future__ import annotations

from typing import List

from .vector_store import SearchResult, SimpleVectorStore


class Retriever:
    """基于向量库的简单检索器。"""

    def __init__(self, vector_store: SimpleVectorStore, top_k: int = 3):
        # vector_store 是真正保存文档向量并执行相似度搜索的对象。
        self.vector_store = vector_store

        # top_k 表示每次返回多少条最相关结果。
        self.top_k = top_k

    def retrieve(self, question: str) -> List[SearchResult]:
        """根据问题返回 Top-K 检索结果。"""

        return self.vector_store.similarity_search(question, k=self.top_k)

