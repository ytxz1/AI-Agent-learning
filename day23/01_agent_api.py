"""练习 01：将 Agent 封装成普通 API。

目标：
1. 创建 FastAPI 应用；
2. 调用 POST /api/agent/chat；
3. 观察 AgentResponse 的结构。
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from rich.console import Console

from modules.app_factory import create_app


console = Console()


def main() -> None:
    """运行普通 Agent API 演示。"""

    client = TestClient(create_app())

    console.rule("[bold green]练习 01：Agent 普通 API")
    response = client.post(
        "/api/agent/chat",
        json={
            "question": "Day23 主要学习什么？",
            "use_tools": True,
        },
    )

    console.print("状态码：", response.status_code)
    console.print("响应 JSON：")
    console.print(response.json())

    # 练习题答案：
    # 题目：如何让 Agent 不使用工具？
    # 如何添加：请求 JSON 中设置 "use_tools": False。
    # 示例：
    # client.post('/api/agent/chat', json={'question': '你好', 'use_tools': False})


if __name__ == "__main__":
    main()
