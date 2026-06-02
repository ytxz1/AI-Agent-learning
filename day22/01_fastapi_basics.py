"""练习 01：FastAPI 基础。

目标：
1. 创建一个最小 FastAPI 应用；
2. 定义首页接口 /；
3. 定义健康检查接口 /health；
4. 用 TestClient 模拟请求，不需要真的启动服务器。
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient
from rich.console import Console


console = Console()


def create_basic_app() -> FastAPI:
    """创建一个最小 FastAPI 应用。"""

    app = FastAPI(title="Day22 练习 01：FastAPI 基础")

    @app.get("/")
    def root() -> dict[str, str]:
        """首页接口。"""

        return {"message": "你好，FastAPI！这是我的第一个 API。"}

    @app.get("/health")
    def health_check() -> dict[str, str]:
        """健康检查接口。"""

        return {"status": "ok"}

    return app


def main() -> None:
    """运行本练习。"""

    app = create_basic_app()
    client = TestClient(app)

    console.rule("[bold green]练习 01：FastAPI 基础")

    root_response = client.get("/")
    health_response = client.get("/health")

    console.print("GET / 返回：", root_response.json())
    console.print("GET /health 返回：", health_response.json())

    # 练习题答案：
    # 题目：如何新增一个 /about 接口，返回项目说明？
    # 如何添加：在 create_basic_app() 函数中继续写 @app.get('/about') 即可。
    # 参考代码：
    # @app.get("/about")
    # def about() -> dict[str, str]:
    #     return {"project": "Day22 FastAPI 入门"}


if __name__ == "__main__":
    main()
