"""练习 05：自动文档。

FastAPI 会根据路由、参数、Pydantic 模型自动生成接口文档：
- /docs 是 Swagger UI，适合调试接口；
- /redoc 是 ReDoc，适合阅读接口说明；
- /openapi.json 是机器可读的 OpenAPI 文档。

本练习不启动服务器，而是通过 TestClient 读取 /openapi.json。
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from rich.console import Console

from config import DOCS_URL, HOST, PORT, REDOC_URL
from modules.app_factory import create_app


console = Console()


def main() -> None:
    """运行自动文档演示。"""

    client = TestClient(create_app())
    openapi_response = client.get("/openapi.json")
    openapi_data = openapi_response.json()

    console.rule("[bold green]练习 05：自动文档")
    console.print("Swagger 文档地址：", f"http://{HOST}:{PORT}{DOCS_URL}")
    console.print("ReDoc 文档地址：", f"http://{HOST}:{PORT}{REDOC_URL}")
    console.print("OpenAPI 标题：", openapi_data["info"]["title"])
    console.print("OpenAPI 版本：", openapi_data["info"]["version"])
    console.print("文档中包含的接口路径：")

    for path in openapi_data["paths"]:
        console.print(" -", path)

    # 练习题答案：
    # 题目：如何修改 /docs 的地址？
    # 如何添加：
    # 1. 打开 day22/.env.example，看到 DOCS_URL=/docs；
    # 2. 复制 .env.example 为 .env；
    # 3. 在 .env 中写 DOCS_URL=/api-docs；
    # 4. 重新启动服务后，Swagger 文档地址就会变成 /api-docs。


if __name__ == "__main__":
    main()
