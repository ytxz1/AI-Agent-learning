from dotenv import load_dotenv
from pathlib import Path
import os


current_dir = Path(__file__).parent
load_dotenv(current_dir / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-chat")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-v3")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "220"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
TOP_K = int(os.getenv("TOP_K", "3"))

