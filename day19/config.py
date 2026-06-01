"""Day 19 的统一配置文件。

Day 19 是完整 RAG 问答系统项目，会用到：
- 在线聊天模型
- 在线 Embedding 模型
- Chroma 向量数据库
- 本地 documents/ 文档目录

真实 API Key 放在 `.env` 中，不要写进代码，也不要提交到 GitHub。
"""

from pathlib import Path
import os

from dotenv import load_dotenv


# 当前文件所在目录，也就是 day19 文件夹。
current_dir = Path(__file__).parent

# 优先读取真实 .env；如果不存在，再读取 .env.example 作为示例兜底。
env_path = current_dir / ".env"
example_env_path = current_dir / ".env.example"
load_dotenv(dotenv_path=env_path)
if example_env_path.exists():
    load_dotenv(dotenv_path=example_env_path, override=False)

# 在线模型 API Key。
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# OpenAI 兼容接口地址。
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")

# 聊天模型，用于最终根据检索上下文生成回答。
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-chat")

# Embedding 模型，用于把文档和问题转换成向量。
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-v3")

# 文档切分和检索参数。
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "200"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
TOP_K = int(os.getenv("TOP_K", "3"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
