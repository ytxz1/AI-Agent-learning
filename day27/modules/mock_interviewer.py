"""模拟面试评分器。

这个评分器不是大模型，而是一个规则评分器。
它会检查回答是否包含：
- 项目背景；
- 技术栈；
- 具体动作；
- 结果；
- 反思。

这能帮助你发现回答是否太空、太短、没有细节。
"""

from __future__ import annotations

import sys
from pathlib import Path


DAY27_DIR = Path(__file__).resolve().parents[1]
if str(DAY27_DIR) not in sys.path:
    sys.path.insert(0, str(DAY27_DIR))

try:
    from .schemas import MockFeedback
except ImportError:
    from schemas import MockFeedback


class MockInterviewer:
    """根据简单规则给面试回答打分。"""

    keywords = {
        "项目": 15,
        "FastAPI": 15,
        "Streamlit": 10,
        "Docker": 10,
        "API": 10,
        "问题": 10,
        "解决": 10,
        "结果": 10,
        "学习": 10,
    }

    def evaluate(self, question: str, answer: str) -> MockFeedback:
        """评估回答质量。"""

        score = min(100, sum(weight for keyword, weight in self.keywords.items() if keyword in answer))
        if len(answer) >= 120:
            score = min(100, score + 10)

        strengths = []
        improvements = []

        if "FastAPI" in answer or "API" in answer:
            strengths.append("回答中体现了接口化和后端能力。")
        else:
            improvements.append("建议补充具体技术，例如 FastAPI、API、Pydantic。")

        if "问题" in answer and "解决" in answer:
            strengths.append("回答中包含问题和解决方案，比较有项目真实感。")
        else:
            improvements.append("建议补充一个真实困难，以及你如何定位和解决。")

        if "结果" in answer or "完成" in answer:
            strengths.append("回答中提到了产出或结果。")
        else:
            improvements.append("建议用一句话说明项目最终产出了什么。")

        polished_answer = self._polish_answer(answer)

        return MockFeedback(
            question=question,
            answer=answer,
            score=score,
            strengths=strengths or ["回答有基本内容。"],
            improvements=improvements or ["可以继续压缩表达，让回答更有重点。"],
            polished_answer=polished_answer,
        )

    def _polish_answer(self, answer: str) -> str:
        """给出一个更适合面试的表达模板。"""

        return (
            "可以按这个结构优化：\n"
            "1. 先说项目背景和目标；\n"
            "2. 再说你负责的核心功能；\n"
            "3. 说明使用的技术栈；\n"
            "4. 讲一个遇到的问题和解决方案；\n"
            "5. 最后说项目结果和你的收获。\n\n"
            f"你的原回答：{answer}"
        )


if __name__ == "__main__":
    # 练习题答案 6：
    # 如何做一次模拟面试评分？
    # 如何添加：创建 MockInterviewer，调用 evaluate()。
    interviewer = MockInterviewer()
    feedback = interviewer.evaluate(
        "请介绍一下你的项目。",
        "我完成了一个 AI Agent 项目，使用 FastAPI 封装 API，使用 Streamlit 做前端，使用 Docker 准备部署，也解决了没有 API Key 时无法演示的问题，最终完成了可展示的学习作品。",
    )
    print("练习题答案 6：模拟面试反馈")
    print(feedback.model_dump())
