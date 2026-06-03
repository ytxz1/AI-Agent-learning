"""30 天冲刺总结报告生成器。"""

from __future__ import annotations

import sys
from pathlib import Path


DAY_DIR = Path(__file__).resolve().parents[1]
if str(DAY_DIR) not in sys.path:
    sys.path.insert(0, str(DAY_DIR))

from config import CANDIDATE_NAME, TARGET_ROLE

try:
    from .application_tracker import ApplicationTracker
    from .interview_planner import InterviewPlanner
    from .job_matcher import JobMatcher
    from .schemas import ApplicationRecord, InterviewReview, JobTarget, SprintCheckItem
except ImportError:
    from application_tracker import ApplicationTracker
    from interview_planner import InterviewPlanner
    from job_matcher import JobMatcher
    from schemas import ApplicationRecord, InterviewReview, JobTarget, SprintCheckItem


class SprintReportBuilder:
    """生成 Day28-Day30 总结报告。"""

    def build_checklist(self) -> list[SprintCheckItem]:
        """生成最终冲刺检查清单。"""

        return [
            SprintCheckItem(title="简历项目经历已整理", done=True, suggestion="确认 bullet 能体现技术、动作和结果。"),
            SprintCheckItem(title="GitHub README 已完善", done=True, suggestion="补充截图和演示 GIF 会更好。"),
            SprintCheckItem(title="至少准备 10 个岗位", done=False, suggestion="继续从 Boss、拉勾、实习僧筛选岗位。"),
            SprintCheckItem(title="准备 1 分钟项目介绍", done=True, suggestion="每天练 3 遍，控制在 60-90 秒。"),
            SprintCheckItem(title="完成面试复盘", done=True, suggestion="每次面试后当天记录问题和改进点。"),
        ]

    def build_markdown_report(
        self,
        jobs: list[JobTarget],
        applications: list[ApplicationRecord],
        interviews: list[InterviewReview],
    ) -> str:
        """生成 Markdown 总结报告。"""

        matcher = JobMatcher()
        tracker = ApplicationTracker(applications)
        planner = InterviewPlanner()

        ranked_jobs = matcher.rank_jobs(jobs)
        application_summary = tracker.build_summary()
        interview_summary = planner.summarize_reviews(interviews)

        lines = [
            "# Day28-Day30 投递与冲刺总结",
            "",
            f"- 候选人：{CANDIDATE_NAME}",
            f"- 目标岗位：{TARGET_ROLE}",
            "",
            "## 岗位匹配 Top 列表",
        ]
        for job in ranked_jobs:
            lines.append(f"- {job['company']}｜{job['role']}：{job['score']} 分，建议：{job['suggestion']}")

        lines.extend(
            [
                "",
                "## 投递统计",
                f"- 已投递数量：{application_summary['total']}",
                f"- 本周目标：{application_summary['weekly_goal']}",
                f"- 完成进度：{application_summary['progress_percent']}%",
                "",
                "## 面试复盘",
                f"- 面试记录数量：{interview_summary['interview_count']}",
                "- 待改进：",
            ]
        )
        lines.extend([f"  - {item}" for item in interview_summary["to_improve"]])

        lines.extend(["", "## 最终冲刺清单"])
        for item in self.build_checklist():
            status = "完成" if item.done else "待完成"
            lines.append(f"- {item.title}：{status}。建议：{item.suggestion}")

        return "\n".join(lines)


if __name__ == "__main__":
    # 练习题答案 6：
    # 如何生成 30 天冲刺总结？
    # 如何添加：读取 jobs/applications/interviews，然后调用 build_markdown_report()。
    from data_loader import load_applications, load_interviews, load_jobs

    report = SprintReportBuilder().build_markdown_report(
        load_jobs(),
        load_applications(),
        load_interviews(),
    )
    print("练习题答案 6：冲刺总结")
    print(report)
