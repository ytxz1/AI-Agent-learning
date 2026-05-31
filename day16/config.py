"""Day 16 的配置文件。

这里统一管理切块参数、Top-K、向量库保存路径等设置。
这样后面调试时，只需要改这里，不需要到处改代码。
"""

from dotenv import load_dotenv
from pathlib import Path
import os


CURRENT_DIR = Path(__file__).parent
load_dotenv(CURRENT_DIR / ".env")

# 文档切块大小。值越大，每个块包含的信息越多。
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "240"))

# 切块重叠大小。用于保留上下文连接。
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "60"))

# 检索时返回多少条结果。
TOP_K = int(os.getenv("TOP_K", "3"))

# 向量库保存文件。
VECTOR_DB_FILE = os.getenv("VECTOR_DB_FILE", str(CURRENT_DIR / "vector_db.json"))

# Embedding 维度。
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "128"))

