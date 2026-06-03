"""投递记录统计器。"""

from __future__ import annotations

from collections import Counter
import sys
from pathlib import Path


DAY_DIR = Path(__file__).resolve().parents[1]
if str(DAY_DIR) not in sys.path:
    sys.path.insert(0, str(DAY_DIR))

from config import WEEKLY_APPLICATION_GOAL

try:
    from .schemas import ApplicationRecord
except ImportError:
    from schemas import ApplicationRecord


class ApplicationTracker:
    """统计投递进度。"""

    def __init__(self, records: list[ApplicationRecord]) -> None:
        self.records = records

    def build_summary(self) -> dict[str, object]:
        """生成投递统计摘要。"""

        status_counter = Counter(record.status for record in self.records)
        channel_counter = Counter(record.channel for record in self.records)
        progress = round(len(self.records) / WEEKLY_APPLICATION_GOAL * 100)
        return {
            "total": len(self.records),
            "weekly_goal": WEEKLY_APPLICATION_GOAL,
            "progress_percent": min(progress, 100),
            "status_counter": dict(status_counter),
            "channel_counter": dict(channel_counter),
            "next_actions": [record.next_action for record in self.records],
        }

    def build_follow_up_list(self) -> list[str]:
        """生成需要跟进的事项。"""

        return [
            f"{record.company} - {record.role}：{record.next_action}"
            for record in self.records
            if "跟进" in record.next_action or "等待" in record.next_action
        ]


if __name__ == "__main__":
    # 练习题答案 4：
    # 如何统计投递进度？
    # 如何添加：读取投递记录，创建 ApplicationTracker，调用 build_summary()。
    from data_loader import load_applications

    tracker = ApplicationTracker(load_applications())
    print("练习题答案 4：投递统计")
    print(tracker.build_summary())
