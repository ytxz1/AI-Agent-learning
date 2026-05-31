"""检索器模块。

负责把用户问题和文档 chunk 做相似度匹配，选出最相关的内容。
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from .loader import DocumentItem


def extract_terms(text: str) -> list[str]:
    """提取用于检索的词项。

    这里采用一个轻量策略：
    - 英文单词直接按单词拆
    - 中文则尽量提取连续汉字片段，并附带少量二元词组
    """
    lowered = text.lower()
    english_terms = re.findall(r"[a-zA-Z0-9_]+", lowered)
    cjk_blocks = re.findall(r"[\u4e00-\u9fff]{2,}", text)

    terms: list[str] = []
    terms.extend(english_terms)
    terms.extend(cjk_blocks)

    # 为中文片段补一些二元词组，增强查询命中率
    for block in cjk_blocks:
        if len(block) >= 2:
            terms.extend([block[i : i + 2] for i in range(len(block) - 1)])

    return [term for term in terms if term.strip()]


def build_document_profile(text: str) -> Counter:
    """为一段文本生成词项统计。"""
    return Counter(extract_terms(text))


@dataclass
class RetrievalResult:
    """单条检索结果。"""

    chunk: DocumentItem
    score: float


class SimpleRetriever:
    """一个轻量级的词项检索器。

    它不是向量数据库，但足以帮助你理解 retriever 的工作方式：
    - 先把文档切片
    - 再给每个 chunk 建立“词项画像”
    - 用户提问时，按相似度打分
    - 返回最相关的 top-k chunk
    """

    def __init__(self, chunks: Iterable[DocumentItem]):
        self.chunks = list(chunks)
        self.chunk_profiles = [build_document_profile(chunk.page_content) for chunk in self.chunks]
        self.document_frequency = self._build_document_frequency()
        self.total_documents = max(1, len(self.chunks))

    def _build_document_frequency(self) -> Counter:
        """统计每个词项在多少个 chunk 中出现过。"""
        df = Counter()
        for profile in self.chunk_profiles:
            for term in profile.keys():
                df[term] += 1
        return df

    def _tf_idf_score(self, query_terms: list[str], profile: Counter) -> float:
        """计算查询和 chunk 的简单 tf-idf 相似度。"""
        if not query_terms:
            return 0.0

        query_counter = Counter(query_terms)
        score = 0.0
        for term, q_tf in query_counter.items():
            doc_tf = profile.get(term, 0)
            if doc_tf == 0:
                continue
            df = self.document_frequency.get(term, 1)
            idf = math.log((self.total_documents + 1) / (df + 1)) + 1
            score += q_tf * doc_tf * idf
        return score

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievalResult]:
        """返回 top-k 检索结果。"""
        query_terms = extract_terms(query)
        scored: list[RetrievalResult] = []
        for chunk, profile in zip(self.chunks, self.chunk_profiles):
            score = self._tf_idf_score(query_terms, profile)
            if score > 0:
                scored.append(RetrievalResult(chunk=chunk, score=score))

        scored.sort(key=lambda item: item.score, reverse=True)
        if scored:
            return scored[:top_k]

        # 如果没有任何显式命中，就返回前几个 chunk 做兜底
        return [RetrievalResult(chunk=chunk, score=0.0) for chunk in self.chunks[:top_k]]


def format_retrieval_summary(results: Iterable[RetrievalResult]) -> str:
    """把检索结果整理成可读文本。"""
    lines = []
    for index, result in enumerate(results, 1):
        chunk = result.chunk
        text = " ".join(chunk.page_content.split())
        snippet = text[:180] + ("..." if len(text) > 180 else "")
        lines.append(
            f"[{index}] score={result.score:.4f} | {chunk.metadata.get('file_name', 'unknown')} | chunk {chunk.metadata.get('chunk_index', 0)+1}: {snippet}"
        )
    return "\n".join(lines)

