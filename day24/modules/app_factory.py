"""FastAPI 应用工厂。

Day24 的应用工厂专门为部署准备：
- 创建 FastAPI 应用；
- 注册首页；
- 注册部署检查路由；
- 在生产环境可以关闭 Swagger 文档。

本项目为了学习方便，默认保留 /docs。
"""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI


DAY24_DIR = Path(__file__).resolve().parents[1]
if str(DAY24_DIR) not in sys.path:
    sys.path.insert(0, str(DAY24_DIR))

from config import APP_NAME, APP_VERSION, DOCS_URL, REDOC_URL, is_production

try:
    from .routes import router
    from .schemas import Message
except ImportError:
    from routes import router
    from schemas import Message


def create_app() -> FastAPI:
    """创建 FastAPI 应用对象。"""

    app = FastAPI(
        title=APP_NAME,
        version=APP_VERSION,
        description="Day24：Docker 基础、镜像构建、容器运行和部署上线。",
        docs_url=None if is_production() else DOCS_URL,
        redoc_url=None if is_production() else REDOC_URL,
    )

    @app.get("/", response_model=Message, tags=["首页"])
    def root() -> Message:
        """首页接口。"""

        return Message(message="Day24 部署上线 API 已启动，请访问 /api/health 查看健康状态。")

    app.include_router(router)
    return app


if __name__ == "__main__":
    # 练习题答案 4：
    # 如何确认应用创建成功？
    # 如何添加：调用 create_app()，打印标题和路由数量。
    demo_app = create_app()
    print("练习题答案 4：应用创建成功")
    print("应用标题：", demo_app.title)
    print("路由数量：", len(demo_app.routes))
