"""Day22 FastAPI 入门项目主入口。

推荐启动方式：
    uvicorn main:app --reload

然后访问：
    http://127.0.0.1:8000/docs

为什么这里不默认让 python main.py 一直启动服务？
因为学习脚本经常需要快速运行和退出，如果 main.py 一运行就占住终端，
会让你误以为程序卡住了。想用 python main.py 启动服务时，可以在 .env 中设置：
    RUN_SERVER=1
"""

from __future__ import annotations

from rich.console import Console

from config import DOCS_URL, HOST, PORT, REDOC_URL, RUN_SERVER
from modules.app_factory import create_app


console = Console()

# uvicorn main:app --reload 会寻找这个 app 对象。
app = create_app()


def main() -> None:
    """打印 Day22 项目的启动说明。"""

    console.rule("[bold green]Day 22 - FastAPI 入门项目")
    console.print("这个文件已经创建好了 FastAPI 应用对象：[bold]app[/bold]")
    console.print()
    console.print("[bold]推荐启动命令：[/bold]")
    console.print("  uvicorn main:app --reload")
    console.print()
    console.print("[bold]启动后访问：[/bold]")
    console.print(f"  Swagger 自动文档：http://{HOST}:{PORT}{DOCS_URL}")
    console.print(f"  ReDoc 自动文档：  http://{HOST}:{PORT}{REDOC_URL}")
    console.print(f"  首页接口：        http://{HOST}:{PORT}/")
    console.print(f"  健康检查：        http://{HOST}:{PORT}/api/health")
    console.print()

    if RUN_SERVER:
        # 只有 RUN_SERVER=1 时才真正启动服务。
        # reload=True 更适合命令行 uvicorn main:app --reload，这里保持 False 更稳定。
        import uvicorn

        uvicorn.run(app, host=HOST, port=PORT, reload=False)
    else:
        console.print("当前 RUN_SERVER=0，所以 main.py 只打印说明，不占用终端。")
        console.print("如果想直接用 python main.py 启动服务，请把 .env 里的 RUN_SERVER 改成 1。")


if __name__ == "__main__":
    # 练习题答案 5：
    # 如何从 main.py 启动或查看 FastAPI 项目？
    # 答案：默认运行 python main.py 查看启动说明；
    # 真正启动服务推荐使用 uvicorn main:app --reload。
    main()
