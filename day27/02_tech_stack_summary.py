"""练习 02：技术栈梳理。

目标：
把“我用过某技术”改成“我在什么场景下用它解决了什么问题”。
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from modules.profile_loader import load_project_profile
from modules.report_writer import write_markdown
from modules.tech_stack_mapper import TechStackMapper


console = Console()


def main() -> None:
    """运行技术栈梳理。"""

    console.rule("[bold green]练习 02：技术栈梳理")
    mapper = TechStackMapper(load_project_profile())
    rows = mapper.build_stack_table()

    table = Table(title="技术栈面试表达")
    table.add_column("技术")
    table.add_column("项目中怎么用")
    table.add_column("面试提示")

    md_lines = ["# 技术栈梳理", ""]
    for row in rows:
        table.add_row(row["tech"], row["usage"], row["interview_tip"])
        md_lines.append(f"## {row['tech']}")
        md_lines.append("")
        md_lines.append(f"- 项目中怎么用：{row['usage']}")
        md_lines.append(f"- 面试提示：{row['interview_tip']}")
        md_lines.append("")

    console.print(table)
    output_path = write_markdown("tech_stack_summary.md", "\n".join(md_lines))
    console.print("已写入：", output_path)

    # 练习题答案：
    # 题目：面试时说技术栈最常见的问题是什么？
    # 如何添加：
    # 只说“我用过”，但没有说明使用场景、解决问题和掌握程度。


if __name__ == "__main__":
    main()
