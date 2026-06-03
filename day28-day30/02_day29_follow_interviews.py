"""Day29 练习：跟进面试。

目标：
1. 统计投递记录；
2. 生成需要跟进的公司列表；
3. 生成面试准备清单。
"""

from __future__ import annotations

from rich.console import Console

from modules.application_tracker import ApplicationTracker
from modules.data_loader import load_applications
from modules.interview_planner import InterviewPlanner
from modules.report_writer import write_markdown


console = Console()


def main() -> None:
    """运行 Day29 跟进面试准备。"""

    console.rule("[bold green]Day29：跟进面试")
    tracker = ApplicationTracker(load_applications())
    planner = InterviewPlanner()

    summary = tracker.build_summary()
    follow_up_list = tracker.build_follow_up_list()
    preparation_plan = planner.build_preparation_plan()

    md_lines = [
        "# Day29 面试跟进报告",
        "",
        f"- 已投递数量：{summary['total']}",
        f"- 本周目标：{summary['weekly_goal']}",
        f"- 完成进度：{summary['progress_percent']}%",
        "",
        "## 需要跟进",
    ]
    md_lines.extend([f"- {item}" for item in follow_up_list])
    md_lines.extend(["", "## 面试准备清单"])
    md_lines.extend([f"- {item}" for item in preparation_plan])

    console.print(summary)
    console.print("\n需要跟进：")
    for item in follow_up_list:
        console.print("- ", item)
    console.print("\n面试准备：")
    for item in preparation_plan:
        console.print("- ", item)

    output_path = write_markdown("day29_interview_follow_up.md", "\n".join(md_lines))
    console.print("已写入：", output_path)

    # 练习题答案：
    # 题目：投递后为什么要记录 next_action？
    # 如何添加：
    # 因为投递不是一次性动作，记录 next_action 可以提醒你何时跟进、准备什么。


if __name__ == "__main__":
    main()
