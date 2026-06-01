"""Embedding 模块。

这个模块提供一个离线可用的简化 embedding，同时也保留了接入 OpenAI Embeddings 的入口。
Embedding 的作用是把“文字”变成“数字向量”，这样程序才能计算两段文字是否相似。
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import List

from config import OPENAI_API_KEY, OPENAI_BASE_URL, EMBEDDING_MODEL


class SimpleEmbeddingModel:
    """一个本地可运行的简化 Embedding 模型。

    真实项目一般使用 OpenAI、通义、智谱等 Embedding API。
    这里为了让你不配置 API Key 也能跑通流程，写了一个哈希版向量模型。
    它不适合生产环境，但非常适合理解 RAG 的数据流。
    """

    def __init__(self, dimension: int = 128):
        # dimension 表示向量维度。
        # 维度越大，可以容纳的信息越多，但计算也会稍微变慢。
        self.dimension = dimension

    def _tokenize(self, text: str) -> List[str]:
        """把文本拆成简单 token。

        这里使用正则保留英文、数字和中文字符。
        """

        tokens = re.findall(r"[A-Za-z0-9\u4e00-\u9fff]+", text.lower())
        return tokens or ["empty"]

    def embed_query(self, text: str) -> List[float]:
        """把一段文本转换成一个归一化向量。"""

        # 先创建一个全 0 向量。
        vec = [0.0] * self.dimension

        for token in self._tokenize(text):
            # 用 md5 把 token 稳定映射到一个向量下标。
            # 同一个词每次都会落到同一个位置，这样才能比较相似度。
            digest = hashlib.md5(token.encode("utf-8")).hexdigest()
            index = int(digest, 16) % self.dimension
            vec[index] += 1.0

        # 对向量做归一化，避免长文本因为词更多而天然分数更高。
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """批量把多段文本转换成向量。"""

        return [self.embed_query(text) for text in texts]


def get_embedding_model():
    """获取 Embedding 模型。

    如果配置了 OPENAI_API_KEY，就优先尝试使用真实 Embedding API。
    如果没有配置或者依赖不可用，就使用本地 SimpleEmbeddingModel。
    """

    if OPENAI_API_KEY:
        try:
            from langchain_openai import OpenAIEmbeddings

            return OpenAIEmbeddings(
                model=EMBEDDING_MODEL,
                openai_api_key=OPENAI_API_KEY,
                openai_api_base=OPENAI_BASE_URL,
            )
        except Exception:
            # API 依赖安装失败、模型名错误、网络异常等情况都不影响本地演示。
            pass
    return SimpleEmbeddingModel()

