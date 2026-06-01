"""Day 3 配置文件。

Day 3 的主题是 API 调用入门。
这里集中管理 API Key、Base URL、模型名、超时时间和兜底开关。
"""

from __future__ import annotations

from dotenv import load_dotenv
from pathlib import Path
import os


BASE_DIR = Path(__file__).parent
ENV_PATH = BASE_DIR / ".env"
EXAMPLE_ENV_PATH = BASE_DIR / ".env.example"
OUTPUT_DIR = BASE_DIR / "output"

load_dotenv(ENV_PATH)
if EXAMPLE_ENV_PATH.exists():
    load_dotenv(EXAMPLE_ENV_PATH, override=False)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "30"))
USE_MOCK_WHEN_FAILED = os.getenv("USE_MOCK_WHEN_FAILED", "true").lower() == "true"

CHAT_COMPLETIONS_URL = f"{OPENAI_BASE_URL}/chat/completions"
REQUEST_LOG_FILE = OUTPUT_DIR / "last_request.json"
RESPONSE_LOG_FILE = OUTPUT_DIR / "last_response.json"

