"""Day28-Day30 投递与冲刺配置文件。

这三天的重点不是继续堆新功能，而是把前面 27 天的成果用于求职：
- Day28：投递实习岗位；
- Day29：跟进面试；
- Day30：总结复盘，准备下一轮冲刺。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


DAY_DIR = Path(__file__).resolve().parent
load_dotenv(DAY_DIR / ".env")


CANDIDATE_NAME = os.getenv("CANDIDATE_NAME", "你的名字")
TARGET_ROLE = os.getenv("TARGET_ROLE", "AI Agent 实习生")
TARGET_CITY = os.getenv("TARGET_CITY", "北京/上海/深圳/杭州/远程")
TARGET_COMPANY_TYPE = os.getenv("TARGET_COMPANY_TYPE", "AI 应用公司/互联网公司/创业公司")
WEEKLY_APPLICATION_GOAL = int(os.getenv("WEEKLY_APPLICATION_GOAL", "15"))

JOB_FILE = DAY_DIR / os.getenv("JOB_FILE", "data/job_targets.json")
APPLICATION_FILE = DAY_DIR / os.getenv("APPLICATION_FILE", "data/application_records.json")
INTERVIEW_FILE = DAY_DIR / os.getenv("INTERVIEW_FILE", "data/interview_reviews.json")
OUTPUT_DIR = DAY_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
