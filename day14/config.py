from dotenv import load_dotenv
from pathlib import Path
import os


current_dir = Path(__file__).parent
env_path = current_dir / ".env"
example_env_path = current_dir / ".env.example"

# 优先读取真正的 .env；如果没有，再用 .env.example 作为兜底。
load_dotenv(dotenv_path=env_path)
if not os.getenv("OPENAI_API_KEY") and example_env_path.exists():
    load_dotenv(dotenv_path=example_env_path)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-chat")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
MAX_ROUNDS = int(os.getenv("MAX_ROUNDS", "5"))

