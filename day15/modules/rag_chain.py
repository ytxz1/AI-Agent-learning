"""RAG 问答链"""

from __future__ import annotations

from typing import List

from config import MODEL_NAME, OPENAI_API_KEY, OPENAI_BASE_URL
from .retriever import Retriever


class RAGChain:
    def __init__(self, retriever: Retriever, llm=None):
        self.retriever = retriever
        self.llm = llm or self._build_llm()

    def _build_llm(self):
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
            return None

    def _fallback_answer(self, question: str, context_text: str) -> str:
        if not context_text.strip():
            return "知识库中没有找到相关内容。"
        return (
            f"根据知识库内容，我找到如下相关信息：\n\n{context_text}\n\n"
            f"问题是：{question}\n"
            "由于当前没有可用的大模型 API，这里先给出基于检索结果的离线回答。"
        )

    def answer(self, question: str) -> str:
        results = self.retriever.retrieve(question)
        if not results:
            return "没有检索到相关资料。"

        context_lines = []
        for idx, item in enumerate(results, 1):
            source = item.document.metadata.get("source", "unknown")
            context_lines.append(
                f"[{idx}] 来源：{source} | 相似度：{item.score:.4f}\n{item.document.page_content}"
            )
        context_text = "\n\n".join(context_lines)

        if self.llm:
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_core.output_parsers import StrOutputParser

            prompt = ChatPromptTemplate.from_template(
                "你是一个知识库助手。请只根据给定资料回答问题。\n\n"
                "资料：\n{context}\n\n"
                "问题：{question}\n\n"
                "回答要求：\n"
                "1. 只根据资料回答。\n"
                "2. 如果资料不足，请明确说明。\n"
                "3. 语言自然、简洁、准确。\n"
            )
            chain = prompt | self.llm | StrOutputParser()
            return chain.invoke({"context": context_text, "question": question})

        return self._fallback_answer(question, context_text)

