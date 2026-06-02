"""Day26 GitHub 优化项目配置文件。

Day26 的目标不是写一个新的 AI 功能，而是把已有项目整理成：
- 代码结构清楚；
- README 足够详细；
- 截图和演示说明完整；
- 文档适合 GitHub 展示；
- 项目更适合投递简历和实习。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


DAY26_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = DAY26_DIR.parent

load_dotenv(DAY26_DIR / ".env")


PROJECT_NAME = os.getenv("PROJECT_NAME", "AI Agent 实习学习项目")
TARGET_DAY = os.getenv("TARGET_DAY", "day25")
AUTHOR_NAME = os.getenv("AUTHOR_NAME", "你的名字")
GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL", "https://github.com/your-name/ai-agent-learning")
IGNORE_OUTPUT = os.getenv("IGNORE_OUTPUT", "true").lower() == "true"


def get_target_project_dir() -> Path:
    """返回要优化的目标项目目录。"""

    return WORKSPACE_DIR / TARGET_DAY
