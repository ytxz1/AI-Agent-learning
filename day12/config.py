from dotenv import load_dotenv
from pathlib import Path
import os


CURRENT_DIR = Path(__file__).parent
load_dotenv(CURRENT_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "mock-structured-model")
MAX_RETRY = int(os.getenv("MAX_RETRY", "2"))

