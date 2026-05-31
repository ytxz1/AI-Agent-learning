from dotenv import load_dotenv
from pathlib import Path
import os

current_dir = Path(__file__).parent
env_path = current_dir / ".env"

load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-chat"
