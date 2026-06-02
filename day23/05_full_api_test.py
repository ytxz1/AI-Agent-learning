"""练习 05：完整 API 测试。

这个脚本把 Day23 的关键接口全部调用一遍：
- 首页
- 健康检查
- 工具列表
- 普通 Agent 问答
- 流式 Agent 问答
- 错误处理
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from rich.console import Console

from modules.app_factory import create_app


console = Console()


def main() -> None:
    """运行完整 API 测试。"""

    client = TestClient(create_app())

    console.rule("[bold green]练习 05：完整 API 测试")

    checks = [
        ("首页", client.get("/")),
        ("健康检查", client.get("/api/health")),
        ("工具列表", client.get("/api/tools")),
        (
            "普通问答",
            client.post(
                "/api/agent/chat",
                json={"question": "2 + 3 * 4 等于多少？", "use_tools": True},
            ),
        ),
        (
            "错误处理",
            client.post("/api/agent/chat", json={"question": "   ", "use_tools": True}),
        ),
    ]

    for name, response in checks:
        console.print(f"\n{name}：状态码 {response.status_code}")
        console.print(response.json())

    with client.stream(
        "POST",
        "/api/agent/stream",
        json={"question": "Day23 的 API 有什么用？", "use_tools": True},
    ) as stream_response:
        console.print("\n流式问答：状态码", stream_response.status_code)
        first_line = next(line for line in stream_response.iter_lines() if line)
        console.print("第一个流式片段：", first_line)

    # 练习题答案：
    # 题目：如何把这个完整测试变成自动化断言？
    # 如何添加：
    # 可以在每次请求后写 assert response.status_code == 200。
    # 例如：
    # assert client.get('/api/health').status_code == 200


if __name__ == "__main__":
    main()
