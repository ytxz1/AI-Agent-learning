"""FastAPI 应用工厂。

Day23 比 Day22 多了几个真实项目常见配置：
- CORS 跨域；
- 统一异常处理；
- Agent 路由注册。

应用工厂能让这些配置集中管理。
"""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


DAY23_DIR = Path(__file__).resolve().parents[1]
if str(DAY23_DIR) not in sys.path:
    sys.path.insert(0, str(DAY23_DIR))

from config import ALLOWED_ORIGINS, APP_NAME, APP_VERSION, DOCS_URL, REDOC_URL

try:
    from .exceptions import AgentAPIError
    from .routes import router
    from .schemas import Message
except ImportError:
    from exceptions import AgentAPIError
    from routes import router
    from schemas import Message


def create_app() -> FastAPI:
    """创建 FastAPI 应用对象。"""

    app = FastAPI(
        title=APP_NAME,
        version=APP_VERSION,
        description="Day23：把 Agent 项目集成为可调用的 FastAPI API。",
        docs_url=DOCS_URL,
        redoc_url=REDOC_URL,
    )

    # CORS 允许前端页面跨域调用后端 API。
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(AgentAPIError)
    async def agent_error_handler(_: Request, exc: AgentAPIError) -> JSONResponse:
        """统一处理 Agent 自定义异常。"""

        return JSONResponse(
            status_code=400,
            content={
                "error": exc.__class__.__name__,
                "detail": exc.detail,
            },
        )

    @app.get("/", response_model=Message, tags=["首页"])
    def root() -> Message:
        """首页接口。"""

        return Message(message="欢迎来到 Day23 Agent API，请访问 /docs 查看接口文档。")

    app.include_router(router)
    return app


if __name__ == "__main__":
    # 练习题答案 6：
    # 如何确认 CORS 和路由都已经挂载？
    # 如何添加：创建 app，查看 user_middleware 和 routes。
    demo_app = create_app()
    print("练习题答案 6：应用创建成功")
    print("中间件数量：", len(demo_app.user_middleware))
    print("路由数量：", len(demo_app.routes))
