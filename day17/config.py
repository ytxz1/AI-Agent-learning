"""Day 17 配置文件。

这里集中管理文档目录、切分参数和预览参数。
这样做的好处是：
- 后面调试时可以只改配置，不改业务代码
- 练习不同 chunk_size 时更方便
"""

from __future__ import annotations

from dotenv import load_dotenv
from pathlib import Path
import os


CURRENT_DIR = Path(__file__).parent
ENV_PATH = CURRENT_DIR / ".env"
EXAMPLE_ENV_PATH = CURRENT_DIR / ".env.example"

load_dotenv(dotenv_path=ENV_PATH)
if EXAMPLE_ENV_PATH.exists():
    # .env.example 只作为兜底，不覆盖 .env 中的真实配置。
    load_dotenv(dotenv_path=EXAMPLE_ENV_PATH, override=False)


# 文档目录，默认是 day17/documents。
DOCS_DIR = os.getenv("DOCS_DIR", "documents")

# 每个 chunk 的最大字符数。
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "300"))

# 相邻 chunk 之间重叠的字符数，用来保留上下文连续性。
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "60"))

# 文档预览时最多展示几份文档。
PREVIEW_LIMIT = int(os.getenv("PREVIEW_LIMIT", "3"))

# 每份文档预览最多展示多少字符。
MAX_PREVIEW_CHARS = int(os.getenv("MAX_PREVIEW_CHARS", "160"))

# Markdown 文件常见的标题拆分规则
MARKDOWN_HEADERS = [
    ("#", "一级标题"),
    ("##", "二级标题"),
    ("###", "三级标题"),
]
