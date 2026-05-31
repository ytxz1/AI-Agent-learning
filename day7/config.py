from dotenv import load_dotenv
import os

load_dotenv()

# 从 .env 文件读取 API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# DeepSeek API 地址
OPENAI_BASE_URL = "https://api.deepseek.com"

# 模型名称
MODEL_NAME = "deepseek-chat"