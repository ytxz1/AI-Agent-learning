"""练习 04：CORS 跨域配置。

当前端项目和后端 API 不在同一个域名、端口或协议时，就会遇到跨域问题。
例如：
- 前端：http://localhost:5173
- 后端：http://127.0.0.1:8000

FastAPI 可以通过 CORSMiddleware 允许指定前端地址访问后端。
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from rich.console import Console

from config import ALLOWED_ORIGINS
from modules.app_factory import create_app


console = Console()


def main() -> None:
    """运行 CORS 配置演示。"""

    client = TestClient(create_app())

    console.rule("[bold green]练习 04：CORS 跨域配置")
    console.print("当前允许的前端来源：")
    for origin in ALLOWED_ORIGINS:
        console.print(" -", origin)

    response = client.options(
        "/api/agent/chat",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    console.print("\nCORS 预检请求状态码：", response.status_code)
    console.print("允许来源响应头：", response.headers.get("access-control-allow-origin"))

    # 练习题答案：
    # 题目：如果你的前端运行在 http://localhost:8080，怎么允许它访问？
    # 如何添加：
    # 1. 复制 .env.example 为 .env；
    # 2. 在 ALLOWED_ORIGINS 后面追加 http://localhost:8080；
    # 3. 重启 FastAPI 服务。


if __name__ == "__main__":
    main()
