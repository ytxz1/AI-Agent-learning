"""Embedding 模块

这个模块提供一个离线可用的简化 embedding，同时也保留了接入 OpenAI Embeddings 的入口。
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import List

from config import OPENAI_API_KEY, OPENAI_BASE_URL, EMBEDDING_MODEL


class SimpleEmbeddingModel:
    def __init__(self, dimension: int = 128):
        self.dimension = dimension

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r"[A-Za-z0-9\u4e00-\u9fff]+", text.lower())
        return tokens or ["empty"]

    def embed_query(self, text: str) -> List[float]:
        vec = [0.0] * self.dimension
        for token in self._tokenize(text):
            digest = hashlib.md5(token.encode("utf-8")).hexdigest()
            index = int(digest, 16) % self.dimension
            vec[index] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]


def get_embedding_model():
    if OPENAI_API_KEY:
        try:
            from langchain_openai import OpenAIEmbeddings

            return OpenAIEmbeddings(
                model=EMBEDDING_MODEL,
                openai_api_key=OPENAI_API_KEY,
                openai_api_base=OPENAI_BASE_URL,
            )
        except Exception:
            pass
    return SimpleEmbeddingModel()

