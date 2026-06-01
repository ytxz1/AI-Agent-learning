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
    # 如果没有安装 langchain-openai，在线 Embedding 不可用。
    # 但项目仍然可以使用本地 Embedding 跑通流程。
    OpenAIEmbeddings = None


class SimpleEmbeddingModel:
    """一个轻量的本地 embedding 模型。"""

    def __init__(self, dimension: int = EMBEDDING_DIM):
        # 向量维度来自 config.py。
        # 本地模式默认 128 维，足够演示相似度检索流程。
        self.dimension = dimension

    def _tokenize(self, text: str) -> List[str]:
        """把文本拆成 token。"""
        # 这个正则会保留英文、数字和中文。
        # 它不是专业分词器，但适合教学演示。
        tokens = re.findall(r"[A-Za-z0-9\u4e00-\u9fff]+", text.lower())
        return tokens or ["empty"]

    def embed_query(self, text: str) -> List[float]:
        """把一段文本转成向量。"""
        # 先创建一个全 0 的向量。
        vector = [0.0] * self.dimension

        for token in self._tokenize(text):
            # 用 md5 把 token 稳定映射到某个向量下标。
            # 同一个 token 每次都会落到同一个位置。
            digest = hashlib.md5(token.encode("utf-8")).hexdigest()
            index = int(digest, 16) % self.dimension
            vector[index] += 1.0

        # 归一化可以避免长文本因为 token 更多而天然分数更高。
        norm = math.sqrt(sum(v * v for v in vector)) or 1.0
        return [v / norm for v in vector]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """批量把文本转成向量。"""
        return [self.embed_query(text) for text in texts]


class HybridEmbeddingModel:
    """在线 Embedding + 本地 Embedding 的混合实现。"""

    def __init__(self):
        # 本地模型始终可用，用来兜底。
        self.local_model = SimpleEmbeddingModel()

        # 在线模型需要 API Key 和 langchain-openai 依赖都存在。
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
                # 初始化在线模型失败时，不让程序崩溃，改用本地模型。
                self.online_model = None
                self.api_enabled = False

    def embed_query(self, text: str) -> List[float]:
        """优先在线 embedding，失败后回退到本地 embedding。"""
        if self.online_model is not None:
            try:
                return list(self.online_model.embed_query(text))
            except Exception:
                # 一旦在线调用失败，就关闭在线模式，后续都走本地兜底。
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
                # 批量在线 Embedding 失败时，同样回退到本地。
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
