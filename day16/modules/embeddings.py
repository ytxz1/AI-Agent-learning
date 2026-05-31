"""Embedding 模块。

这个版本使用一个轻量的本地 embedding，实现“文本 -> 向量”的基本过程。
它不依赖外部 API，所以 Day 16 可以离线学习。
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import List

from config import EMBEDDING_DIM


class SimpleEmbeddingModel:
    """一个简单的本地 embedding 模型。

    思路：
    - 把文本切成 token
    - 对 token 做哈希
    - 映射到固定维度向量
    - 统计频次并归一化
    """

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

        # 归一化，避免文本长度对向量影响太大。
        norm = math.sqrt(sum(v * v for v in vector)) or 1.0
        return [v / norm for v in vector]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """把多段文本一次性转成向量。"""
        return [self.embed_query(text) for text in texts]


def get_embedding_model() -> SimpleEmbeddingModel:
    """返回当前项目使用的 embedding 模型。"""
    return SimpleEmbeddingModel()

