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

# 兼容两种运行方式：
# 1. 作为包导入：from modules.vector_store import PersistentVectorStore
# 2. 直接运行：python day16/modules/vector_store.py
try:
    from .loader import DocumentItem
except ImportError:
    from loader import DocumentItem


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """计算两个向量的余弦相似度。"""
    # dot 是点积，表示两个向量在方向上的重合程度。
    dot = sum(x * y for x, y in zip(a, b))

    # norm 是向量长度。
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    # 如果某个向量全是 0，就无法计算相似度，直接返回 0。
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


@dataclass
class SearchResult:
    """检索结果。

    document：被检索出来的文本块。
    score：相似度分数，越高表示越相关。
    """

    document: DocumentItem
    score: float


@dataclass
class VectorRecord:
    """向量库里保存的单条记录。

    page_content：文本块原文。
    metadata：来源、路径、chunk_index 等信息。
    vector：文本块对应的向量。
    """

    page_content: str
    metadata: dict
    vector: List[float]


class PersistentVectorStore:
    """一个轻量可持久化向量库。

    这里不用真实的第三方向量库，而是用 JSON 文件模拟“存储 + 检索”流程，
    方便学习 Day 16 的底层逻辑。
    """

    def __init__(self, embedding_model, db_path: str):
        # embedding_model 负责把文本转成向量。
        self.embedding_model = embedding_model

        # db_path 是向量库 JSON 文件保存位置。
        self.db_path = Path(db_path)

        # records 是内存中的向量库数据。
        self.records: List[VectorRecord] = []

    def add_documents(self, documents: List[DocumentItem]):
        """把文档块加入向量库。"""
        if not documents:
            return

        # 先取出所有文本，批量做 Embedding。
        texts = [doc.page_content for doc in documents]
        vectors = self.embedding_model.embed_documents(texts)

        # 每个文本块保存成一条 VectorRecord。
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

        # 用户问题也要先转成向量，才能和文档向量比较。
        query_vector = self.embedding_model.embed_query(query)
        scored: List[SearchResult] = []

        for record in self.records:
            # 如果传了 metadata_filter，就先做条件过滤。
            if metadata_filter:
                matched = all(record.metadata.get(key) == value for key, value in metadata_filter.items())
                if not matched:
                    continue

            # 计算问题向量和当前文档向量的相似度。
            score = _cosine_similarity(query_vector, record.vector)
            scored.append(
                SearchResult(
                    document=DocumentItem(page_content=record.page_content, metadata=record.metadata),
                    score=score,
                )
            )

        # 按分数从高到低排序，最后返回前 k 条。
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:k]

    def stats(self) -> Dict:
        """返回向量库的基本统计信息。"""
        sources = {}
        for item in self.records:
            # 统计每个来源文件贡献了多少个文本块。
            source = item.metadata.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1

        return {
            "record_count": len(self.records),
            "source_counts": sources,
            "db_path": str(self.db_path),
        }

    def save(self):
        """把向量库保存到磁盘。"""
        # 确保保存目录存在。
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # dataclass 转成普通 dict 后才能 JSON 序列化。
        payload = [asdict(record) for record in self.records]
        self.db_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self):
        """从磁盘加载向量库。"""
        if not self.db_path.exists():
            self.records = []
            return

        # 从 JSON 文件恢复 VectorRecord 列表。
        data = json.loads(self.db_path.read_text(encoding="utf-8"))
        self.records = [VectorRecord(**item) for item in data]
