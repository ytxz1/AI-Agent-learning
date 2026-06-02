"""面试题库管理器。

Day27 准备的面试题主要围绕：
- 项目经历；
- FastAPI；
- 工程化；
- 部署；
- 前端；
- RAG；
- 自我反思。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


DAY27_DIR = Path(__file__).resolve().parents[1]
if str(DAY27_DIR) not in sys.path:
    sys.path.insert(0, str(DAY27_DIR))

try:
    from .schemas import InterviewQuestion
except ImportError:
    from schemas import InterviewQuestion


class InterviewBank:
    """读取和筛选面试题。"""

    def __init__(self, question_file: Path | None = None) -> None:
        self.question_file = question_file or DAY27_DIR / "data" / "interview_questions.json"
        self.questions = self._load_questions()

    def _load_questions(self) -> list[InterviewQuestion]:
        data = json.loads(self.question_file.read_text(encoding="utf-8"))
        return [InterviewQuestion(**item) for item in data]

    def list_questions(self) -> list[InterviewQuestion]:
        """返回全部面试题。"""

        return self.questions

    def filter_by_category(self, category: str) -> list[InterviewQuestion]:
        """按分类筛选面试题。"""

        return [question for question in self.questions if question.category == category]


if __name__ == "__main__":
    # 练习题答案 5：
    # 如何查看面试题库？
    # 如何添加：创建 InterviewBank，调用 list_questions()。
    bank = InterviewBank()
    print("练习题答案 5：面试题数量", len(bank.list_questions()))
    for question in bank.list_questions():
        print(question.model_dump())
