"""Day28 练习：投递实习岗位。

目标：
1. 读取目标岗位；
2. 根据关键词计算匹配度；
3. 生成岗位匹配报告。
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from modules.data_loader import load_jobs
from modules.job_matcher import JobMatcher
from modules.report_writer import write_markdown


console = Console()


def main() -> None:
    """运行 Day28 岗位投递准备。"""

    console.rule("[bold green]Day28：投递实习岗位")
    ranked_jobs = JobMatcher().rank_jobs(load_jobs())

    table = Table(title="岗位匹配度")
    table.add_column("公司")
    table.add_column("岗位")
    table.add_column("分数")
    table.add_column("建议")

    md_lines = ["# Day28 岗位匹配报告", ""]
    for job in ranked_jobs:
        table.add_row(str(job["company"]), str(job["role"]), str(job["score"]), str(job["suggestion"]))
        md_lines.append(f"- {job['company']}｜{job['role']}：{job['score']} 分")
        md_lines.append(f"  - 匹配关键词：{', '.join(job['matched_keywords'])}")
        md_lines.append(f"  - 建议：{job['suggestion']}")

    console.print(table)
    output_path = write_markdown("day28_job_match_report.md", "\n".join(md_lines))
    console.print("已写入：", output_path)

    # 练习题答案：
    # 题目：投递岗位时为什么要看关键词匹配？
    # 如何添加：
    # 因为岗位名称可能很宽泛，关键词能帮助你判断项目经历是否真的匹配 JD。


if __name__ == "__main__":
    main()
