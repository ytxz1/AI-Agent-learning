"""岗位匹配分析器。

Day28 的重点是投递实习岗位。
投递不能只看岗位名称，还要看关键词是否和你的项目匹配。
"""

from __future__ import annotations

import sys
from pathlib import Path


DAY_DIR = Path(__file__).resolve().parents[1]
if str(DAY_DIR) not in sys.path:
    sys.path.insert(0, str(DAY_DIR))

try:
    from .schemas import JobTarget
except ImportError:
    from schemas import JobTarget


class JobMatcher:
    """分析岗位和当前项目能力的匹配度。"""

    owned_skills = {
        "Python",
        "FastAPI",
        "LLM",
        "RAG",
        "Agent",
        "OpenAI API",
        "LangChain",
        "Docker",
        "Streamlit",
        "GitHub",
        "Prompt",
    }

    def score_job(self, job: JobTarget) -> dict[str, object]:
        """给单个岗位打匹配分。"""

        matched = [keyword for keyword in job.jd_keywords if keyword in self.owned_skills]
        score = round(len(matched) / max(len(job.jd_keywords), 1) * 100)
        return {
            "company": job.company,
            "role": job.role,
            "score": score,
            "matched_keywords": matched,
            "missing_keywords": [keyword for keyword in job.jd_keywords if keyword not in matched],
            "priority": job.priority,
            "suggestion": self._build_suggestion(score),
        }

    def rank_jobs(self, jobs: list[JobTarget]) -> list[dict[str, object]]:
        """按匹配分排序岗位。"""

        return sorted([self.score_job(job) for job in jobs], key=lambda item: item["score"], reverse=True)

    def _build_suggestion(self, score: int) -> str:
        """根据匹配分生成投递建议。"""

        if score >= 80:
            return "高度匹配，优先投递，并在沟通中突出项目经历。"
        if score >= 50:
            return "中等匹配，可以投递，但要补充岗位缺失关键词。"
        return "匹配度偏低，建议谨慎投递或先补强相关能力。"


if __name__ == "__main__":
    # 练习题答案 3：
    # 如何给岗位打匹配分？
    # 如何添加：读取岗位后，调用 JobMatcher.rank_jobs()。
    from data_loader import load_jobs

    matcher = JobMatcher()
    for item in matcher.rank_jobs(load_jobs()):
        print(item)
