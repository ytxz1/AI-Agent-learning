"""Day24 部署上线项目主入口。

推荐本地启动：
    cd day24
    uvicorn main:app --reload

推荐 Docker 启动：
    docker compose up --build
"""

from __future__ import annotations

from rich.console import Console

from config import DOCS_URL, HOST, PORT, REDOC_URL, RUN_SERVER
from modules.app_factory import create_app


console = Console()

# Uvicorn 会通过 main:app 找到这个对象。
app = create_app()


def main() -> None:
    """打印 Day24 启动和部署说明。"""

    console.rule("[bold green]Day 24 - 部署上线")
    console.print("部署上线 API 应用已经创建完成。")
    console.print()
    console.print("[bold]本地启动：[/bold]")
    console.print("  cd day24")
    console.print("  uvicorn main:app --reload")
    console.print()
    console.print("[bold]Docker 启动：[/bold]")
    console.print("  cd day24")
    console.print("  docker compose up --build")
    console.print()
    console.print("[bold]启动后访问：[/bold]")
    console.print(f"  Swagger 文档：http://127.0.0.1:{PORT}{DOCS_URL}")
    console.print(f"  ReDoc 文档：  http://127.0.0.1:{PORT}{REDOC_URL}")
    console.print(f"  健康检查：    http://127.0.0.1:{PORT}/api/health")
    console.print()

    if RUN_SERVER:
        import uvicorn

        uvicorn.run(app, host=HOST, port=PORT, reload=False)
    else:
        console.print("当前 RUN_SERVER=0，所以 main.py 只打印说明，不占用终端。")
        console.print("真正启动服务推荐使用：uvicorn main:app --reload")


if __name__ == "__main__":
    # 练习题答案 5：
    # 如何启动 Day24 项目？
    # 如何添加：本地用 uvicorn，容器用 docker compose up --build。
    main()
