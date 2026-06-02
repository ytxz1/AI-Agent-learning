"""检索结果展示模块。"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

# 兼容直接运行 day16/modules/search_demo.py。
DAY16_DIR = Path(__file__).resolve().parent.parent
if str(DAY16_DIR) not in sys.path:
    sys.path.insert(0, str(DAY16_DIR))

from config import TOP_K


class SearchDemo:
    """把检索过程包装成更容易看的演示格式。"""

    def __init__(self, vector_store, top_k: int = TOP_K):
        # vector_store 负责真正的向量搜索。
        self.vector_store = vector_store

        # top_k 表示默认返回前几条结果。
        self.top_k = top_k

    def search(self, question: str, metadata_filter: Optional[dict] = None):
        """执行一次检索。"""
        # metadata_filter 是可选过滤条件。
        # 例如 {"source": "rag_notes.txt"} 表示只查这个来源文件。
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
            # source 和 chunk_index 都来自文档 metadata。
            source = item.document.metadata.get("source", "unknown")
            chunk_index = item.document.metadata.get("chunk_index", "-")
            lines.append(
                f"[{idx}] 分数：{item.score:.4f} | 来源：{source} | 块编号：{chunk_index}\n"
                f"{item.document.page_content}"
            )
        return "\n\n".join(lines)
