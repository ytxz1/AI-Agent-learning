"""练习 03：连接后端 API。

Day25 可以连接 Day23 的后端接口：
POST /api/agent/chat

如果后端没启动，本脚本也不会崩掉，而是返回 api-error。
"""

from __future__ import annotations

from rich.console import Console

from config import AGENT_API_URL
from modules.api_client import AgentAPIClient


console = Console()


def main() -> None:
    """测试后端 API 连接。"""

    console.rule("[bold green]练习 03：连接后端 API")
    client = AgentAPIClient(AGENT_API_URL)
    response = client.chat("Day25 如何连接后端 API？")
    console.print(response.model_dump())

    # 练习题答案：
    # 题目：如果后端端口不是 8000，应该改哪里？
    # 如何添加：
    # 复制 .env.example 为 .env，然后修改 AGENT_API_URL。
    # 例如：http://127.0.0.1:9000/api/agent/chat


if __name__ == "__main__":
    main()
