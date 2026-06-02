"""检索器模块。

Retriever 是 RAG 里的“检索员”。
它负责接收用户问题，然后调用向量库找出最相关的文本块。
把检索逻辑单独封装成类，可以让后面的 RAGChain 不用关心底层向量库细节。
"""

from __future__ import annotations

from typing import List

# 兼容两种运行方式：
# 1. 从 day15/05_retriever.py 导入：from modules.retriever import Retriever
#    这时 retriever.py 属于 modules 包，必须使用相对导入 .vector_store。
# 2. 直接运行 day15/modules/retriever.py
#    这时它没有包身份，相对导入会失败，所以退回普通导入 vector_store。
try:
    from .vector_store import SearchResult, SimpleVectorStore
except ImportError:
    from vector_store import SearchResult, SimpleVectorStore


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
