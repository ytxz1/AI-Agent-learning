"""Embedding 模块。

这个模块提供一个离线可用的简化 embedding，同时也保留了接入 OpenAI Embeddings 的入口。
Embedding 的作用是把“文字”变成“数字向量”，这样程序才能计算两段文字是否相似。
"""

from __future__ import annotations

import hashlib
import math
import re
import sys
from pathlib import Path
from typing import List

# 兼容直接运行 day15/modules/embeddings.py 的情况。
# 直接运行时，Python 默认只认识 modules 目录，不认识上一层 day15/config.py。
# 所以这里把 day15 根目录加入 sys.path。
DAY15_DIR = Path(__file__).resolve().parent.parent
if str(DAY15_DIR) not in sys.path:
    sys.path.insert(0, str(DAY15_DIR))

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


class HybridEmbeddingModel:
    """在线优先、本地兜底的 Embedding 模型。

    为什么需要这个类：
    `OpenAIEmbeddings(...)` 初始化成功，不代表后面的 API 请求一定成功。
    例如 base_url 不匹配、模型名不支持、网络异常，都可能在 embed_documents() 时才报错。
    所以这里把每一次在线调用都包起来，失败就自动切换成本地 SimpleEmbeddingModel。
    """

    def __init__(self):
        # 本地模型始终可用。
        self.local_model = SimpleEmbeddingModel()

        # 在线模型默认不可用，只有 API Key 和依赖都正常时才启用。
        self.online_model = None
        self.api_enabled = False

        if OPENAI_API_KEY:
            try:
                from langchain_openai import OpenAIEmbeddings

                self.online_model = OpenAIEmbeddings(
                    model=EMBEDDING_MODEL,
                    openai_api_key=OPENAI_API_KEY,
                    openai_api_base=OPENAI_BASE_URL,
                )
                self.api_enabled = True
            except Exception:
                self.online_model = None
                self.api_enabled = False

    @property
    def mode(self) -> str:
        """返回当前 Embedding 模式，方便调试。"""

        return "在线 API" if self.api_enabled else "本地兜底"

    def _disable_online(self):
        """关闭在线模式，后续都使用本地兜底。"""

        self.online_model = None
        self.api_enabled = False

    def embed_query(self, text: str) -> List[float]:
        """把单个查询文本转成向量。"""

        if self.online_model is not None:
            try:
                return list(self.online_model.embed_query(text))
            except Exception:
                self._disable_online()
        return self.local_model.embed_query(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """批量把文档文本转成向量。"""

        if self.online_model is not None:
            try:
                vectors = self.online_model.embed_documents(texts)
                return [list(vector) for vector in vectors]
            except Exception:
                self._disable_online()
        return self.local_model.embed_documents(texts)


def get_embedding_model():
    """获取 Embedding 模型。

    返回 HybridEmbeddingModel：
    - 有 API Key 时优先使用在线 Embedding。
    - 在线调用失败时自动回退本地 Embedding。
    - 没有 API Key 时直接使用本地 Embedding。
    """

    return HybridEmbeddingModel()

