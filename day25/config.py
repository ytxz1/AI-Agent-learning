"""Day25 前端界面项目配置文件。

Day25 的重点是 Streamlit 前端页面。
配置项主要包括：
- 页面标题；
- 后端 Agent API 地址；
- 默认运行模式；
- 页面主题色。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


DAY25_DIR = Path(__file__).resolve().parent
load_dotenv(DAY25_DIR / ".env")


APP_TITLE = os.getenv("APP_TITLE", "Day25 AI Agent Web 界面")
APP_SUBTITLE = os.getenv("APP_SUBTITLE", "把后端 API 变成用户可以直接操作的页面")
AGENT_API_URL = os.getenv("AGENT_API_URL", "http://127.0.0.1:8000/api/agent/chat")
DEFAULT_MODE = os.getenv("DEFAULT_MODE", "local")
PRIMARY_COLOR = os.getenv("PRIMARY_COLOR", "#0F766E")
ACCENT_COLOR = os.getenv("ACCENT_COLOR", "#F59E0B")
