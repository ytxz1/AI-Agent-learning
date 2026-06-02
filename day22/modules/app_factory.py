"""FastAPI 应用工厂。

应用工厂的意思是：用一个函数 create_app() 来创建 FastAPI 应用。
这样做的好处：
- main.py 可以很短，只需要 app = create_app()；
- 测试脚本可以复用 create_app()；
- 后面要添加中间件、跨域配置、异常处理时，都可以集中放在这里。
"""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI


# 让这个文件也支持直接运行。
DAY22_DIR = Path(__file__).resolve().parents[1]
if str(DAY22_DIR) not in sys.path:
    sys.path.insert(0, str(DAY22_DIR))

from config import APP_NAME, APP_VERSION, DOCS_URL, REDOC_URL

try:
    from .routes import router
    from .schemas import Message
except ImportError:
    from routes import router
    from schemas import Message


def create_app() -> FastAPI:
    """创建并返回 FastAPI 应用对象。"""

    app = FastAPI(
        title=APP_NAME,
        version=APP_VERSION,
        description=(
            "Day22 的 FastAPI 入门项目，重点学习路由、请求参数、响应模型和自动文档。"
        ),
        docs_url=DOCS_URL,
        redoc_url=REDOC_URL,
    )

    @app.get("/", response_model=Message, tags=["首页"])
    def root() -> Message:
        """首页接口。

        打开 http://127.0.0.1:8000/ 时会看到这条消息。
        """

        return Message(message="欢迎来到 Day22 FastAPI 入门 API，请访问 /docs 查看自动文档。")

    # 把 routes.py 中定义的业务接口挂载到应用上。
    app.include_router(router)
    return app


if __name__ == "__main__":
    # 练习题答案 4：
    # 如何确认 create_app() 创建出来的是一个 FastAPI 应用？
    # 答案：调用 create_app()，然后查看它注册的路由数量。
    demo_app = create_app()
    print("练习题答案 4：FastAPI 应用创建成功")
    print("应用标题：", demo_app.title)
    print("已注册路由数量：", len(demo_app.routes))
