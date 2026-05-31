"""RAG 检索链模块。

它把检索和回答串在一起：
1. 接收用户问题
2. 调用 Retriever 找相关 chunk
3. 构造上下文
4. 使用在线模型生成回答
"""

from __future__ import annotations

from typing import Iterable

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config import ANSWER_STYLE, MODEL_NAME, OPENAI_API_KEY, OPENAI_BASE_URL, TEMPERATURE
from .loader import DocumentItem
from .retriever import RetrievalResult, SimpleRetriever, format_retrieval_summary


class RAGChain:
    """一个可运行的 RAG 检索链。"""

    def __init__(self, chunks: Iterable[DocumentItem], top_k: int = 3, max_context_chars: int = 1600):
        self.top_k = top_k
        self.max_context_chars = max_context_chars
        self.retriever = SimpleRetriever(chunks)
        self.llm = self._build_llm()

    def _build_llm(self):
        """按需构建在线模型。"""
        if not OPENAI_API_KEY:
            return None
        try:
            return ChatOpenAI(
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_BASE_URL,
                model=MODEL_NAME,
                temperature=TEMPERATURE,
            )
        except Exception:
            return None

    def retrieve(self, question: str) -> list[RetrievalResult]:
        """检索最相关的 chunk。"""
        return self.retriever.retrieve(question, top_k=self.top_k)

    def build_context(self, results: Iterable[RetrievalResult]) -> str:
        """把检索结果拼接成上下文。"""
        parts = []
        total = 0
        for result in results:
            chunk = result.chunk
            source = chunk.metadata.get("file_name", "unknown")
            idx = chunk.metadata.get("chunk_index", 0) + 1
            text = chunk.page_content.strip()
            block = f"【来源：{source}｜chunk {idx}】\n{text}"
            if total + len(block) > self.max_context_chars:
                remaining = self.max_context_chars - total
                if remaining <= 0:
                    break
                block = block[:remaining]
            parts.append(block)
            total += len(block)
        return "\n\n".join(parts)

    def _build_prompt(self):
        """构建回答提示词。"""
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你是一个严谨的 RAG 助手。你必须严格根据提供的上下文回答问题。"
                    "如果上下文不足，请明确说明哪些信息缺失，不要编造。"
                    f"回答风格要求：{ANSWER_STYLE}。",
                ),
                (
                    "human",
                    "请根据下面的检索上下文回答问题。\n\n"
                    "【问题】\n{question}\n\n"
                    "【检索上下文】\n{context}\n\n"
                    "请给出简洁、准确、可读的回答。",
                ),
            ]
        )

    def answer_with_context(self, question: str, context: str) -> str:
        """根据上下文生成回答。"""
        if self.llm is not None:
            try:
                prompt = self._build_prompt()
                chain = prompt | self.llm | StrOutputParser()
                return chain.invoke({"question": question, "context": context})
            except Exception as exc:
                summary = self._extract_summary(context)
                return (
                    "在线生成失败，已切换到离线兜底模式。\n"
                    f"可用上下文摘要：{summary}\n"
                    f"问题：{question}\n"
                    f"错误原因：{exc}"
                )

        summary = self._extract_summary(context)
        return (
            f"根据检索到的资料，{summary}\n\n"
            f"针对问题「{question}」，当前没有可用的在线模型，因此返回基于上下文的摘要回答。"
        )

    def _extract_summary(self, context: str) -> str:
        """从上下文中提炼一个简短摘要。"""
        lines = [line.strip() for line in context.splitlines() if line.strip()]
        if not lines:
            return "没有检索到有效资料。"
        first = lines[0]
        if len(first) > 120:
            first = first[:120] + "..."
        return first

    def query(self, question: str) -> dict:
        """完整执行一次检索链。"""
        results = self.retrieve(question)
        context = self.build_context(results)
        answer = self.answer_with_context(question, context)
        return {
            "question": question,
            "retrieval_summary": format_retrieval_summary(results),
            "context": context,
            "answer": answer,
            "api_enabled": self.llm is not None,
        }
