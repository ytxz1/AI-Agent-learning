"""Day24 部署上线项目配置文件。

Day24 的重点是“把项目部署出去”，所以配置要比普通脚本更重视环境差异：
- 本地开发环境；
- Docker 容器环境；
- 生产服务器环境。

真实项目里，配置通常不会写死在代码中，而是通过 .env 或服务器环境变量传入。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


DAY24_DIR = Path(__file__).resolve().parent
load_dotenv(DAY24_DIR / ".env")


APP_NAME = os.getenv("APP_NAME", "Day24 部署上线 API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
API_PREFIX = os.getenv("API_PREFIX", "/api")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DOCS_URL = os.getenv("DOCS_URL", "/docs")
REDOC_URL = os.getenv("REDOC_URL", "/redoc")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
SERVICE_NAME = os.getenv("SERVICE_NAME", "day24-deploy-api")
RUN_SERVER = os.getenv("RUN_SERVER", "0") == "1"


def is_production() -> bool:
    """判断当前是否是生产环境。"""

    return ENVIRONMENT.lower() == "production"
