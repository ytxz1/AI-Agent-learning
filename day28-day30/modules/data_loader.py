"""JSON 数据加载工具。"""

from __future__ import annotations

import json
import sys
from pathlib import Path


DAY_DIR = Path(__file__).resolve().parents[1]
if str(DAY_DIR) not in sys.path:
    sys.path.insert(0, str(DAY_DIR))

from config import APPLICATION_FILE, INTERVIEW_FILE, JOB_FILE

try:
    from .schemas import ApplicationRecord, InterviewReview, JobTarget
except ImportError:
    from schemas import ApplicationRecord, InterviewReview, JobTarget


def load_jobs(path: Path = JOB_FILE) -> list[JobTarget]:
    """读取目标岗位列表。"""

    data = json.loads(path.read_text(encoding="utf-8"))
    return [JobTarget(**item) for item in data]


def load_applications(path: Path = APPLICATION_FILE) -> list[ApplicationRecord]:
    """读取投递记录。"""

    data = json.loads(path.read_text(encoding="utf-8"))
    return [ApplicationRecord(**item) for item in data]


def load_interviews(path: Path = INTERVIEW_FILE) -> list[InterviewReview]:
    """读取面试复盘记录。"""

    data = json.loads(path.read_text(encoding="utf-8"))
    return [InterviewReview(**item) for item in data]


if __name__ == "__main__":
    # 练习题答案 2：
    # 如何读取三类求职数据？
    # 如何添加：分别调用 load_jobs、load_applications、load_interviews。
    print("练习题答案 2：岗位数量", len(load_jobs()))
    print("投递记录数量", len(load_applications()))
    print("面试复盘数量", len(load_interviews()))
