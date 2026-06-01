"""RAG 问答链。

RAGChain 负责把“检索结果”和“用户问题”组合起来生成最终回答。
它是 Day 15 项目的最后一环：
文档加载 -> 文本切分 -> 向量化 -> 检索 -> 生成答案。
"""

from __future__ import annotations

from config import MODEL_NAME, OPENAI_API_KEY, OPENAI_BASE_URL
from .retriever import Retriever


class RAGChain:
    """一个最小版 RAG 问答链。"""

    def __init__(self, retriever: Retriever, llm=None):
        # retriever 负责根据问题找资料。
        self.retriever = retriever

        # llm 负责根据资料生成自然语言回答。
        # 如果外部没有传入 llm，就尝试根据配置创建一个。
        self.llm = llm or self._build_llm()

    def _build_llm(self):
        """根据环境变量构建聊天模型。

        没有 API Key 时返回 None，后续会使用离线 fallback 回答。
        """

        if not OPENAI_API_KEY:
            return None
        try:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_BASE_URL,
                model=MODEL_NAME,
                temperature=0.2,
            )
        except Exception:
            # 如果 LangChain 依赖缺失、网络不可用或配置错误，仍然允许本地流程继续运行。
            return None

    def _fallback_answer(self, question: str, context_text: str) -> str:
        """没有可用大模型时，直接把检索结果整理成一个离线答案。"""

        if not context_text.strip():
            return "知识库中没有找到相关内容。"
        return (
            f"根据知识库内容，我找到如下相关信息：\n\n{context_text}\n\n"
            f"问题是：{question}\n"
            "由于当前没有可用的大模型 API，这里先给出基于检索结果的离线回答。"
        )

    def answer(self, question: str) -> str:
        """回答用户问题。

        步骤：
        1. 先用 retriever 检索相关资料。
        2. 把资料整理成 context。
        3. 如果有真实大模型，就让模型根据 context 回答。
        4. 如果没有真实大模型，就返回离线整理版答案。
        """

        results = self.retriever.retrieve(question)
        if not results:
            return "没有检索到相关资料。"

        context_lines = []
        for idx, item in enumerate(results, 1):
            source = item.document.metadata.get("source", "unknown")
            # 每条资料都保留来源和相似度，方便你检查检索结果是否合理。
            context_lines.append(
                f"[{idx}] 来源：{source} | 相似度：{item.score:.4f}\n{item.document.page_content}"
            )
        context_text = "\n\n".join(context_lines)

        if self.llm:
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_core.output_parsers import StrOutputParser

            # Prompt 明确告诉模型：只能根据给定资料回答。
            # 这是 RAG 防止模型乱编的重要约束。
            prompt = ChatPromptTemplate.from_template(
                "你是一个知识库助手。请只根据给定资料回答问题。\n\n"
                "资料：\n{context}\n\n"
                "问题：{question}\n\n"
                "回答要求：\n"
                "1. 只根据资料回答。\n"
                "2. 如果资料不足，请明确说明。\n"
                "3. 语言自然、简洁、准确。\n"
            )

            # LangChain 表达式链：Prompt -> LLM -> 字符串输出解析器。
            chain = prompt | self.llm | StrOutputParser()
            return chain.invoke({"context": context_text, "question": question})

        return self._fallback_answer(question, context_text)

