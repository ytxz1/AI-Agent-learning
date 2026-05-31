from dotenv import load_dotenv
from pathlib import Path
import os

# 获取当前文件所在目录
current_dir = Path(__file__).parent
# 构建 .env 文件的完整路径
env_path = current_dir / ".env"

# 加载 .env 文件中的环境变量
load_dotenv(dotenv_path=env_path)

# 从环境变量中读取 API 密钥
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# DeepSeek API 的基础 URL
OPENAI_BASE_URL = "https://api.deepseek.com"
# 使用的模型名称
MODEL_NAME = "deepseek-chat"
