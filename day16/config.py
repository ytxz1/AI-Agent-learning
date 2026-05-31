"""Day 16 配置文件。

这里统一管理：
- 切分参数
- Top-K
- 向量库保存路径
- Embedding 相关配置

这样后面调试时，只需要改这里，不需要到处改代码。
"""

from __future__ import annotations

from dotenv import load_dotenv
from pathlib import Path
import os


CURRENT_DIR = Path(__file__).parent
ENV_PATH = CURRENT_DIR / ".env"
EXAMPLE_ENV_PATH = CURRENT_DIR / ".env.example"

# 优先读取真正的 .env；如果没有，再允许用 .env.example 兜底。
load_dotenv(ENV_PATH)
if EXAMPLE_ENV_PATH.exists():
    load_dotenv(EXAMPLE_ENV_PATH, override=False)


# 文档切块大小。值越大，每个块里包含的信息越多。
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "240"))

# 切块重叠大小。用于保留上下文连接。
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "60"))

# 搜索时返回多少条结果。
TOP_K = int(os.getenv("TOP_K", "3"))

# 向量库保存文件。
VECTOR_DB_FILE = os.getenv("VECTOR_DB_FILE", str(CURRENT_DIR / "vector_db.json"))

# 本地 embedding 的维度。
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "128"))

# 在线 Embedding 配置（可选）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-v3")

