"""后端 API 客户端。

Day25 的前端可以连接 Day23 的后端：
POST http://127.0.0.1:8000/api/agent/chat

如果后端没有启动，API 客户端会返回清楚的错误说明，
页面不会因为 requests 报错而崩掉。
"""

from __future__ import annotations

import sys
from pathlib import Path

import requests


DAY25_DIR = Path(__file__).resolve().parents[1]
if str(DAY25_DIR) not in sys.path:
    sys.path.insert(0, str(DAY25_DIR))

try:
    from .schemas import ChatResponse
except ImportError:
    from schemas import ChatResponse


class AgentAPIClient:
    """调用 Agent 后端 API 的客户端。"""

    def __init__(self, api_url: str, timeout: int = 20) -> None:
        self.api_url = api_url
        self.timeout = timeout

    def chat(self, question: str, use_tools: bool = True) -> ChatResponse:
        """调用后端 Agent 问答接口。"""

        try:
            response = requests.post(
                self.api_url,
                json={"question": question, "use_tools": use_tools},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            return ChatResponse(
                answer=(
                    "调用后端 API 失败。\n"
                    "请确认 Day23 后端是否已经启动，或者切换到本地模拟模式。\n"
                    f"错误信息：{exc}"
                ),
                source="api-error",
                used_tools=["api_client"],
            )

        data = response.json()
        return ChatResponse(
            answer=data.get("answer", "后端没有返回 answer 字段。"),
            source=data.get("source", "api"),
            used_tools=data.get("used_tools", []),
        )


if __name__ == "__main__":
    # 练习题答案 3：
    # 如何测试 API 客户端？
    # 如何添加：创建 AgentAPIClient，传入后端地址，然后调用 chat()。
    # 如果后端没启动，会返回 api-error，而不是让程序崩掉。
    client = AgentAPIClient("http://127.0.0.1:8000/api/agent/chat")
    result = client.chat("Day25 如何连接后端？")
    print("练习题答案 3：API 客户端测试结果")
    print(result.model_dump())
