"""Day 18 配置文件。

这里集中管理：
- 文档目录
- 切分参数
- 检索参数
- 回答展示参数
- 可选的在线模型配置
"""

from __future__ import annotations

from dotenv import load_dotenv
from pathlib import Path
import os


CURRENT_DIR = Path(__file__).parent
ENV_PATH = CURRENT_DIR / ".env"
EXAMPLE_ENV_PATH = CURRENT_DIR / ".env.example"

# 优先加载真正的 .env；如果没有，就允许用 .env.example 作为默认值。
load_dotenv(dotenv_path=ENV_PATH)
if EXAMPLE_ENV_PATH.exists():
    load_dotenv(dotenv_path=EXAMPLE_ENV_PATH, override=False)


DOCS_DIR = os.getenv("DOCS_DIR", "documents")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "320"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "70"))
TOP_K = int(os.getenv("TOP_K", "3"))
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "1600"))
ANSWER_STYLE = os.getenv("ANSWER_STYLE", "concise")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-chat")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

