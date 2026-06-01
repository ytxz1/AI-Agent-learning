"""Day 15 的统一配置文件。

这个文件专门负责读取环境变量和保存默认参数。
把配置集中放在这里有一个好处：后面的所有代码都不用到处写死参数。
如果你想调整模型、切分长度、检索数量，只需要改这里或者改 `.env`。
"""

from pathlib import Path
import os

from dotenv import load_dotenv


# 当前文件所在目录，也就是 day15 文件夹。
current_dir = Path(__file__).parent

# 加载 day15/.env 文件。
# 如果 .env 不存在，程序不会报错，而是继续使用下面写好的默认值。
load_dotenv(current_dir / ".env")

# 大模型 API Key。
# 没有填写时，项目会自动退回到本地模拟方案，方便你先理解 RAG 流程。
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# API 地址。
# 默认值使用 DeepSeek 兼容接口；如果你用 OpenAI，可以在 .env 中改成 https://api.openai.com/v1。
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")

# 聊天模型名称，用于最终根据检索资料生成回答。
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-chat")

# Embedding 模型名称，用于把文本变成向量。
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-v3")

# 每个文本块的最大长度。
# RAG 一般不会把整篇文档直接塞给模型，而是切成小块后检索最相关的部分。
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "220"))

# 相邻文本块之间重复保留的字符数。
# overlap 可以减少“刚好在切分位置断句”导致的上下文丢失。
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

# 每次检索返回最相关的几个文本块。
TOP_K = int(os.getenv("TOP_K", "3"))

