"""响应解析模块。

API 返回的是一个字典，真正有用的回答通常在：
response["choices"][0]["message"]["content"]
这个模块专门练习如何安全地解析响应。
"""

from __future__ import annotations


def extract_message_text(response: dict) -> str:
    """从 Chat Completions 响应中提取助手回复。"""
    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(f"无法从响应中提取文本：{exc}") from exc


def summarize_response(response: dict) -> dict:
    """提取响应中的关键信息，方便展示和调试。"""
    usage = response.get("usage") or {}
    return {
        "id": response.get("id"),
        "model": response.get("model"),
        "is_mock": bool(response.get("mock", False)),
        "finish_reason": (response.get("choices") or [{}])[0].get("finish_reason"),
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
    }

