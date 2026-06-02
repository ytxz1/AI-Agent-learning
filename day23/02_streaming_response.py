"""练习 02：流式响应。

流式响应适合大模型逐字输出的场景。
用户不需要等完整答案生成完，前端可以一边收到内容一边显示。
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from rich.console import Console

from modules.app_factory import create_app


console = Console()


def main() -> None:
    """运行流式响应演示。"""

    client = TestClient(create_app())

    console.rule("[bold green]练习 02：流式响应")
    with client.stream(
        "POST",
        "/api/agent/stream",
        json={"question": "请用一句话说明 Day23 为什么重要", "use_tools": True},
    ) as response:
        console.print("状态码：", response.status_code)
        console.print("前 10 个流式片段：")
        for index, line in enumerate(response.iter_lines()):
            if line:
                console.print(line)
            if index >= 9:
                break

    # 练习题答案：
    # 题目：流式接口为什么返回 text/event-stream？
    # 如何添加：
    # 在 routes.py 中使用 StreamingResponse(..., media_type='text/event-stream')。
    # 这样前端可以按照 SSE 风格一段一段接收内容。


if __name__ == "__main__":
    main()
