"""Day27 简历优化与面试准备配置文件。

Day27 的目标是把前面做过的项目转化成：
- 简历上的项目经历；
- 面试时能讲清楚的技术栈；
- 常见问题的回答；
- 一分钟自我介绍；
- 模拟面试反馈。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


DAY27_DIR = Path(__file__).resolve().parent
load_dotenv(DAY27_DIR / ".env")


CANDIDATE_NAME = os.getenv("CANDIDATE_NAME", "你的名字")
TARGET_ROLE = os.getenv("TARGET_ROLE", "AI Agent 实习生")
TARGET_COMPANY = os.getenv("TARGET_COMPANY", "目标公司")
PROJECT_NAME = os.getenv("PROJECT_NAME", "AI Agent 实习学习项目")
PROFILE_FILE = DAY27_DIR / os.getenv("PROFILE_FILE", "data/project_profile.json")

OUTPUT_DIR = DAY27_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
