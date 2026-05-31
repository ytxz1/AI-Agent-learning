"""Day 12 的基础配置。

这个文件只负责读取环境变量，不放业务逻辑。
这样做的好处是：配置和代码分离，后面更容易改模型、改重试次数。
"""

from dotenv import load_dotenv
from pathlib import Path
import os


# 以当前文件所在目录为基准，读取同目录下的 .env 文件。
CURRENT_DIR = Path(__file__).parent
load_dotenv(CURRENT_DIR / ".env")

# 下面这些变量会被其他模块直接导入使用。
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "mock-structured-model")
MAX_RETRY = int(os.getenv("MAX_RETRY", "2"))

