"""面试准备与复盘工具。"""

from __future__ import annotations

import sys
from pathlib import Path


DAY_DIR = Path(__file__).resolve().parents[1]
if str(DAY_DIR) not in sys.path:
    sys.path.insert(0, str(DAY_DIR))

try:
    from .schemas import InterviewReview
except ImportError:
    from schemas import InterviewReview


class InterviewPlanner:
    """生成面试准备清单和复盘摘要。"""

    base_questions = [
        "请介绍一下你的 AI Agent 项目。",
        "你为什么选择 FastAPI？",
        "RAG 的流程是什么？",
        "Agent 工具调用是怎么理解的？",
        "Docker 部署时为什么监听 0.0.0.0？",
        "Streamlit 前端如何保存聊天记录？",
        "这个项目如果继续优化，你会做什么？",
    ]

    def build_preparation_plan(self) -> list[str]:
        """生成面试前准备清单。"""

        return [
            "准备 1 分钟项目介绍。",
            "准备 3 个项目难点和解决方案。",
            "准备 FastAPI、RAG、Docker、Streamlit 的项目场景表达。",
            "检查 GitHub 仓库 README、截图和运行命令。",
            "准备向面试官提问的 2 个问题。",
        ]

    def summarize_reviews(self, reviews: list[InterviewReview]) -> dict[str, object]:
        """总结面试复盘。"""

        all_questions = []
        all_good_points = []
        all_to_improve = []
        for review in reviews:
            all_questions.extend(review.questions)
            all_good_points.extend(review.good_points)
            all_to_improve.extend(review.to_improve)

        return {
            "interview_count": len(reviews),
            "questions": all_questions,
            "good_points": all_good_points,
            "to_improve": all_to_improve,
        }


if __name__ == "__main__":
    # 练习题答案 5：
    # 如何生成面试准备清单？
    # 如何添加：创建 InterviewPlanner，调用 build_preparation_plan()。
    planner = InterviewPlanner()
    print("练习题答案 5：面试准备清单")
    for item in planner.build_preparation_plan():
        print("-", item)
