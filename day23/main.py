"""Day23 Agent API 主入口。

推荐启动方式：
    cd day23
    uvicorn main:app --reload

启动后访问：
    http://127.0.0.1:8000/docs
"""

from __future__ import annotations

from rich.console import Console

from config import DOCS_URL, HOST, PORT, REDOC_URL, RUN_SERVER
from modules.app_factory import create_app


console = Console()

# Uvicorn 会寻找 main.py 中的 app 对象。
app = create_app()


def main() -> None:
    """打印项目启动说明。"""

    console.rule("[bold green]Day 23 - 集成项目 API")
    console.print("Agent API 应用已经创建完成。")
    console.print()
    console.print("[bold]推荐启动命令：[/bold]")
    console.print("  cd day23")
    console.print("  uvicorn main:app --reload")
    console.print()
    console.print("[bold]启动后访问：[/bold]")
    console.print(f"  Swagger 文档：http://{HOST}:{PORT}{DOCS_URL}")
    console.print(f"  ReDoc 文档：  http://{HOST}:{PORT}{REDOC_URL}")
    console.print(f"  Agent 问答：  POST http://{HOST}:{PORT}/api/agent/chat")
    console.print(f"  流式问答：    POST http://{HOST}:{PORT}/api/agent/stream")
    console.print()

    if RUN_SERVER:
        import uvicorn

        uvicorn.run(app, host=HOST, port=PORT, reload=False)
    else:
        console.print("当前 RUN_SERVER=0，所以 main.py 只打印说明，不占用终端。")
        console.print("真正启动服务推荐使用：uvicorn main:app --reload")


if __name__ == "__main__":
    # 练习题答案 7：
    # 如何启动 Day23 API？
    # 如何添加：默认运行 python main.py 查看说明；
    # 正式启动使用 uvicorn main:app --reload。
    main()
