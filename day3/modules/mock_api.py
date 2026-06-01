"""本地模拟 API。

当没有 API Key、网络不可用或请求失败时，可以用这个模块模拟 Chat Completions 响应。
这样 Day 3 的学习重点不会被网络环境卡住。
"""

from __future__ import annotations

import time
from uuid import uuid4


def mock_chat_completion(messages: list[dict], model: str = "mock-chat") -> dict:
    """返回一个类似 Chat Completions 的模拟响应。"""
    user_messages = [item["content"] for item in messages if item.get("role") == "user"]
    latest_question = user_messages[-1] if user_messages else "你好"
    answer = (
        "这是本地模拟回复。\n"
        f"我收到的问题是：{latest_question}\n"
        "真实 API 调用时，choices[0].message.content 会放模型回答。"
    )
    return {
        "id": f"chatcmpl-mock-{uuid4().hex[:8]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": answer,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        },
        "mock": True,
    }

