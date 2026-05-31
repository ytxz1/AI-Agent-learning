"""向量库存储与检索模块。

这个模块是 Day 16 的核心：
1. 存储向量
2. 存储原文
3. 存储元数据
4. 根据问题做相似度搜索
5. 支持保存到磁盘和加载回来
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

from .loader import DocumentItem


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """计算两个向量的余弦相似度。"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


@dataclass
class SearchResult:
    """检索结果。"""

    document: DocumentItem
    score: float


@dataclass
class VectorRecord:
    """向量库里保存的单条记录。"""

    page_content: str
    metadata: dict
    vector: List[float]


class PersistentVectorStore:
    """一个轻量可持久化向量库。

    这里不用真实的第三方向量库，而是用 JSON 文件模拟“存储 + 检索”流程，
    方便学习 Day 16 的底层逻辑。
    """

    def __init__(self, embedding_model, db_path: str):
        self.embedding_model = embedding_model
        self.db_path = Path(db_path)
        self.records: List[VectorRecord] = []

    def add_documents(self, documents: List[DocumentItem]):
        """把文档块加入向量库。"""
        texts = [doc.page_content for doc in documents]
        vectors = self.embedding_model.embed_documents(texts)

        for doc, vector in zip(documents, vectors):
            self.records.append(
                VectorRecord(
                    page_content=doc.page_content,
                    metadata=dict(doc.metadata),
                    vector=vector,
                )
            )

    def similarity_search(
        self,
        query: str,
        k: int = 3,
        metadata_filter: Optional[Dict] = None,
    ) -> List[SearchResult]:
        """根据查询做相似度搜索。"""
        if not self.records:
            return []

        query_vector = self.embedding_model.embed_query(query)
        scored: List[SearchResult] = []

        for record in self.records:
            # 如果传了 metadata_filter，就先做条件过滤。
            if metadata_filter:
                matched = all(record.metadata.get(key) == value for key, value in metadata_filter.items())
                if not matched:
                    continue

            score = _cosine_similarity(query_vector, record.vector)
            scored.append(
                SearchResult(
                    document=DocumentItem(page_content=record.page_content, metadata=record.metadata),
                    score=score,
                )
            )

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:k]

    def stats(self) -> Dict:
        """返回向量库的基本统计信息。"""
        sources = {}
        for item in self.records:
            source = item.metadata.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1

        return {
            "record_count": len(self.records),
            "source_counts": sources,
            "db_path": str(self.db_path),
        }

    def save(self):
        """把向量库保存到磁盘。"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [asdict(record) for record in self.records]
        self.db_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self):
        """从磁盘加载向量库。"""
        if not self.db_path.exists():
            self.records = []
            return

        data = json.loads(self.db_path.read_text(encoding="utf-8"))
        self.records = [VectorRecord(**item) for item in data]

