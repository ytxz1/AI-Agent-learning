"""练习 05：生成 GitHub 仓库质量报告。

这个脚本会综合：
- 项目结构检查；
- README 检查；
- 项目亮点；
- 下一步行动；

然后写入 output/github_report.md 和 output/github_report.json。
"""

from __future__ import annotations

from rich.console import Console

from config import get_target_project_dir
from modules.github_advisor import GitHubAdvisor
from modules.report_writer import write_github_report


console = Console()


def main() -> None:
    """生成 GitHub 优化报告。"""

    console.rule("[bold green]练习 05：GitHub 质量报告")
    report = GitHubAdvisor(get_target_project_dir()).build_report()
    md_path, json_path = write_github_report(report)

    console.print("当前评分：", f"{report.score}/100")
    console.print("Markdown 报告：", md_path)
    console.print("JSON 报告：", json_path)
    console.print("\n下一步建议：")
    for action in report.next_actions:
        console.print("- ", action)

    # 练习题答案：
    # 题目：评分低是不是说明项目没用？
    # 如何添加：
    # 不是。评分只是提醒 GitHub 展示还有哪些地方可以补充，
    # 比如截图、docs、README 结构，而不是否定代码价值。


if __name__ == "__main__":
    main()
