"""Day 20 配置文件。

这里统一管理 Coding Agent 需要的基础参数：
- 工作区目录
- API 配置
- 模型配置
- 预览长度
- 默认显示数量
"""

from __future__ import annotations

from dotenv import load_dotenv
from pathlib import Path
import os


CURRENT_DIR = Path(__file__).parent
ENV_PATH = CURRENT_DIR / ".env"
EXAMPLE_ENV_PATH = CURRENT_DIR / ".env.example"

# 先读真实 .env，如果没有再用 .env.example 做兜底。
load_dotenv(ENV_PATH)
if EXAMPLE_ENV_PATH.exists():
    load_dotenv(EXAMPLE_ENV_PATH, override=False)


WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", ".")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
PLAN_MODEL = os.getenv("PLAN_MODEL", "deepseek-chat")
CODE_MODEL = os.getenv("CODE_MODEL", "deepseek-chat")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
MAX_FILES_PREVIEW = int(os.getenv("MAX_FILES_PREVIEW", "5"))
MAX_FILE_PREVIEW_CHARS = int(os.getenv("MAX_FILE_PREVIEW_CHARS", "220"))
DEFAULT_TOP_N = int(os.getenv("DEFAULT_TOP_N", "5"))

