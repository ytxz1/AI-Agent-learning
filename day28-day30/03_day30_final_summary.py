"""Day30 练习：总结复盘。

目标：
1. 汇总岗位、投递和面试复盘；
2. 生成 30 天冲刺总结；
3. 输出下一轮行动计划。
"""

from __future__ import annotations

from rich.console import Console

from modules.data_loader import load_applications, load_interviews, load_jobs
from modules.report_writer import write_markdown
from modules.sprint_report import SprintReportBuilder


console = Console()


def main() -> None:
    """运行 Day30 总结复盘。"""

    console.rule("[bold green]Day30：总结复盘")
    report = SprintReportBuilder().build_markdown_report(
        load_jobs(),
        load_applications(),
        load_interviews(),
    )
    output_path = write_markdown("day30_final_summary.md", report)

    console.print(report)
    console.print("\n已写入：", output_path)

    # 练习题答案：
    # 题目：30 天结束后是不是就停止学习？
    # 如何添加：
    # 不是。30 天只是完成第一轮闭环，后面要根据投递和面试反馈继续迭代项目。


if __name__ == "__main__":
    main()
