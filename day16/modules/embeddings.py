"""Embedding 模块。

这一版把 Day 16 的 embedding 改成“混合模式”：
- 如果配置了可用的 API Key，就优先使用在线 Embedding
- 如果没有配置，或者在线调用失败，就自动回退到本地 embedding

这样既满足“需要 API 的地方就用 API”的要求，也保证项目可以离线运行。
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import List

from config import EMBEDDING_DIM, EMBEDDING_MODEL, OPENAI_API_KEY, OPENAI_BASE_URL

try:
    from langchain_openai import OpenAIEmbeddings
except Exception:  # pragma: no cover
    OpenAIEmbeddings = None


class SimpleEmbeddingModel:
    """一个轻量的本地 embedding 模型。"""

    def __init__(self, dimension: int = EMBEDDING_DIM):
        self.dimension = dimension

    def _tokenize(self, text: str) -> List[str]:
        """把文本拆成 token。"""
        tokens = re.findall(r"[A-Za-z0-9\u4e00-\u9fff]+", text.lower())
        return tokens or ["empty"]

    def embed_query(self, text: str) -> List[float]:
        """把一段文本转成向量。"""
        vector = [0.0] * self.dimension
        for token in self._tokenize(text):
            digest = hashlib.md5(token.encode("utf-8")).hexdigest()
            index = int(digest, 16) % self.dimension
            vector[index] += 1.0

        norm = math.sqrt(sum(v * v for v in vector)) or 1.0
        return [v / norm for v in vector]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """批量把文本转成向量。"""
        return [self.embed_query(text) for text in texts]


class HybridEmbeddingModel:
    """在线 Embedding + 本地 Embedding 的混合实现。"""

    def __init__(self):
        self.local_model = SimpleEmbeddingModel()
        self.online_model = None
        self.api_enabled = False

        if OPENAI_API_KEY and OpenAIEmbeddings is not None:
            try:
                self.online_model = OpenAIEmbeddings(
                    api_key=OPENAI_API_KEY,
                    base_url=OPENAI_BASE_URL,
                    model=EMBEDDING_MODEL,
                )
                self.api_enabled = True
            except Exception:
                self.online_model = None
                self.api_enabled = False

    def embed_query(self, text: str) -> List[float]:
        """优先在线 embedding，失败后回退到本地 embedding。"""
        if self.online_model is not None:
            try:
                return list(self.online_model.embed_query(text))
            except Exception:
                self.api_enabled = False
                self.online_model = None
        return self.local_model.embed_query(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """优先在线批量 embedding，失败后回退到本地 embedding。"""
        if self.online_model is not None:
            try:
                vectors = self.online_model.embed_documents(texts)
                return [list(vector) for vector in vectors]
            except Exception:
                self.api_enabled = False
                self.online_model = None
        return self.local_model.embed_documents(texts)

    @property
    def mode(self) -> str:
        """当前使用的 embedding 模式。"""
        return "在线 API" if self.api_enabled else "本地兜底"


def get_embedding_model() -> HybridEmbeddingModel:
    """返回当前项目使用的 embedding 模型。"""
    return HybridEmbeddingModel()

