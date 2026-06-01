"""Chat Completions 客户端。

这个模块把“构造请求、发送请求、失败兜底、记录日志”集中封装起来。
"""

from __future__ import annotations

import json
from pathlib import Path

from config import (
    CHAT_COMPLETIONS_URL,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    REQUEST_LOG_FILE,
    RESPONSE_LOG_FILE,
    TEMPERATURE,
    TIMEOUT_SECONDS,
    USE_MOCK_WHEN_FAILED,
)
from .http_client import APIRequestError, post_json
from .mock_api import mock_chat_completion


class ChatAPIClient:
    """一个最小可用的 Chat Completions 客户端。"""

    def __init__(self):
        self.model = OPENAI_MODEL
        self.api_key = OPENAI_API_KEY
        self.api_available = bool(self.api_key)

    def build_messages(self, user_input: str, system_prompt: str | None = None) -> list[dict]:
        """构造 messages 参数。"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_input})
        return messages

    def build_payload(self, messages: list[dict], temperature: float = TEMPERATURE) -> dict:
        """构造请求体。"""
        return {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

    def _headers(self) -> dict:
        """构造请求头。"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _write_json(self, path: Path, data: dict) -> None:
        """记录请求或响应，方便学习时查看。"""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def chat(self, user_input: str, system_prompt: str | None = None) -> dict:
        """发送一次聊天请求。"""
        messages = self.build_messages(user_input, system_prompt=system_prompt)
        payload = self.build_payload(messages)
        self._write_json(REQUEST_LOG_FILE, payload)

        if not self.api_available:
            response = mock_chat_completion(messages, model=self.model)
            self._write_json(RESPONSE_LOG_FILE, response)
            return response

        try:
            response = post_json(
                CHAT_COMPLETIONS_URL,
                headers=self._headers(),
                payload=payload,
                timeout=TIMEOUT_SECONDS,
            )
        except APIRequestError:
            if not USE_MOCK_WHEN_FAILED:
                raise
            response = mock_chat_completion(messages, model=self.model)

        self._write_json(RESPONSE_LOG_FILE, response)
        return response

