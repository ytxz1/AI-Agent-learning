"""完整练习：Day28-Day30 求职冲刺工作流。

一次性运行：
1. 岗位匹配；
2. 投递统计；
3. 面试准备；
4. 冲刺总结。
"""

from __future__ import annotations

from rich.console import Console

from modules.application_tracker import ApplicationTracker
from modules.data_loader import load_applications, load_interviews, load_jobs
from modules.interview_planner import InterviewPlanner
from modules.job_matcher import JobMatcher
from modules.report_writer import write_json, write_markdown
from modules.sprint_report import SprintReportBuilder


console = Console()


def main() -> None:
    """运行完整冲刺工作流。"""

    console.rule("[bold green]Day28-Day30 完整冲刺工作流")
    jobs = load_jobs()
    applications = load_applications()
    interviews = load_interviews()

    ranked_jobs = JobMatcher().rank_jobs(jobs)
    application_summary = ApplicationTracker(applications).build_summary()
    interview_plan = InterviewPlanner().build_preparation_plan()
    final_report = SprintReportBuilder().build_markdown_report(jobs, applications, interviews)

    console.print("岗位匹配 Top 结果：", ranked_jobs)
    console.print("投递统计：", application_summary)
    console.print("面试准备：", interview_plan)

    md_path = write_markdown("full_sprint_workflow.md", final_report)
    json_path = write_json(
        "full_sprint_workflow.json",
        {
            "ranked_jobs": ranked_jobs,
            "application_summary": application_summary,
            "interview_plan": interview_plan,
        },
    )

    console.print("Markdown 输出：", md_path)
    console.print("JSON 输出：", json_path)

    # 练习题答案：
    # 题目：为什么要把岗位、投递、面试放在一个工作流里？
    # 如何添加：
    # 因为求职不是单点动作，岗位筛选、投递、跟进、面试复盘必须连起来才有效。


if __name__ == "__main__":
    main()
