"""Day23 集成项目 API 的配置文件。

Day23 的主题是：把前面写过的 Agent 能力包装成 FastAPI 接口。
所以配置里除了 FastAPI 基础信息，还会包含：
- OpenAI API 配置；
- 跨域 CORS 配置；
- 路由前缀；
- 服务启动地址和端口。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


DAY23_DIR = Path(__file__).resolve().parent
load_dotenv(DAY23_DIR / ".env")


# FastAPI 应用基础配置。
APP_NAME = os.getenv("APP_NAME", "Day23 Agent API 集成项目")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
API_PREFIX = os.getenv("API_PREFIX", "/api")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
DOCS_URL = os.getenv("DOCS_URL", "/docs")
REDOC_URL = os.getenv("REDOC_URL", "/redoc")
RUN_SERVER = os.getenv("RUN_SERVER", "0") == "1"


# OpenAI 配置。
# 如果 OPENAI_API_KEY 为空，AgentService 会自动走本地模拟回答。
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip() or None
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


# CORS 跨域配置。
# .env 中用逗号分隔多个地址。
raw_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173",
)
ALLOWED_ORIGINS = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


# 示例知识库文件。
KNOWLEDGE_FILE = DAY23_DIR / "data" / "agent_knowledge.txt"
