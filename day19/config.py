"""Day 19 的统一配置文件。

重点说明：
1. 聊天模型和 Embedding 模型不一定来自同一个服务商。
2. DeepSeek 的 deepseek-chat 适合聊天，但并不等于它支持 OpenAIEmbeddings。
3. 如果 base_url 不支持 /embeddings 接口，就算 API Key 正确，也可能返回 404。

真实 API Key 请放在 day19/.env 中，不要写进代码，也不要提交到 GitHub。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


# 当前文件所在目录，也就是 day19 文件夹。
CURRENT_DIR = Path(__file__).resolve().parent

# 优先读取真实 .env；如果存在 .env.example，也作为示例兜底读取。
ENV_PATH = CURRENT_DIR / ".env"
EXAMPLE_ENV_PATH = CURRENT_DIR / ".env.example"
load_dotenv(dotenv_path=ENV_PATH)
if EXAMPLE_ENV_PATH.exists():
    load_dotenv(dotenv_path=EXAMPLE_ENV_PATH, override=False)


# 在线模型 API Key。
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# 聊天模型接口地址。你当前可以继续用 DeepSeek。
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com").strip()

# 聊天模型名称。
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-chat").strip()

# Embedding 模型接口地址。
# 默认等于 OPENAI_BASE_URL，但推荐你根据实际服务单独配置。
# 例如 OpenAI 官方 embedding 通常使用：https://api.openai.com/v1
EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", OPENAI_BASE_URL).strip()

# Embedding 模型名称。
# OpenAI 官方常用：text-embedding-3-small / text-embedding-3-large
# 如果你使用第三方平台，要确认该平台真的支持这个模型和 /embeddings 接口。
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small").strip()


# 文档切分和检索参数。
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "200"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
TOP_K = int(os.getenv("TOP_K", "3"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
