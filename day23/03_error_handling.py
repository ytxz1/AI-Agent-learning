"""练习 03：错误处理。

API 项目必须处理错误。
如果用户传空问题，不能让程序崩掉，而应该返回稳定的 JSON 错误结构。
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from rich.console import Console

from modules.app_factory import create_app


console = Console()


def main() -> None:
    """运行错误处理演示。"""

    client = TestClient(create_app())

    console.rule("[bold green]练习 03：错误处理")

    response = client.post(
        "/api/agent/chat",
        json={"question": "   ", "use_tools": True},
    )

    console.print("状态码：", response.status_code)
    console.print("错误响应：")
    console.print(response.json())

    # 练习题答案：
    # 题目：如何新增一种自定义错误？
    # 如何添加：
    # 1. 在 modules/exceptions.py 中新增 class XxxError(AgentAPIError)；
    # 2. 在业务代码里 raise XxxError('错误说明')；
    # 3. app_factory.py 中的统一异常处理器会自动返回 JSON。


if __name__ == "__main__":
    main()
