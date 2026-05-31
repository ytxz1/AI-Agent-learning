"""检索结果展示模块。"""

from __future__ import annotations

from typing import Optional

from config import TOP_K


class SearchDemo:
    """把检索过程包装成更容易看的演示格式。"""

    def __init__(self, vector_store, top_k: int = TOP_K):
        self.vector_store = vector_store
        self.top_k = top_k

    def search(self, question: str, metadata_filter: Optional[dict] = None):
        """执行一次检索。"""
        return self.vector_store.similarity_search(
            question,
            k=self.top_k,
            metadata_filter=metadata_filter,
        )

    def format_results(self, results) -> str:
        """把检索结果格式化成更容易阅读的文本。"""
        if not results:
            return "没有检索到相关内容。"

        lines = []
        for idx, item in enumerate(results, 1):
            source = item.document.metadata.get("source", "unknown")
            chunk_index = item.document.metadata.get("chunk_index", "-")
            lines.append(
                f"[{idx}] 分数：{item.score:.4f} | 来源：{source} | 块编号：{chunk_index}\n"
                f"{item.document.page_content}"
            )
        return "\n\n".join(lines)

