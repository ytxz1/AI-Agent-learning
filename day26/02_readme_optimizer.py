"""练习 02：完善 README。

README 是 GitHub 项目的门面。
这个脚本会检查目标项目 README 是否包含关键内容。
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from config import get_target_project_dir
from modules.readme_reviewer import ReadmeReviewer


console = Console()


def main() -> None:
    """运行 README 优化检查。"""

    reviewer = ReadmeReviewer(get_target_project_dir())

    console.rule("[bold green]练习 02：完善 README")
    table = Table(title="README 检查结果")
    table.add_column("检查项")
    table.add_column("状态")
    table.add_column("建议")

    for check in reviewer.review():
        table.add_row(check.title, "通过" if check.passed else "需要优化", check.suggestion)
    console.print(table)

    console.print("\nREADME 优化建议：")
    for tip in reviewer.generate_improvement_tips():
        console.print("- ", tip)

    # 练习题答案：
    # 题目：README 最应该写清楚哪三件事？
    # 如何添加：
    # 1. 项目是什么；2. 怎么运行；3. 有什么效果或亮点。


if __name__ == "__main__":
    main()
