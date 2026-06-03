"""补充练习：Offer 冲刺检查清单。

这个脚本把 Day28-Day30 最后阶段要做的事情整理成清单。
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from modules.report_writer import write_markdown
from modules.sprint_report import SprintReportBuilder


console = Console()


def main() -> None:
    """生成 Offer 冲刺清单。"""

    console.rule("[bold green]Offer 冲刺检查清单")
    checklist = SprintReportBuilder().build_checklist()

    table = Table(title="最终检查清单")
    table.add_column("事项")
    table.add_column("状态")
    table.add_column("建议")

    md_lines = ["# Offer 冲刺检查清单", ""]
    for item in checklist:
        status = "完成" if item.done else "待完成"
        table.add_row(item.title, status, item.suggestion)
        md_lines.append(f"- [{ 'x' if item.done else ' ' }] {item.title}：{item.suggestion}")

    console.print(table)
    output_path = write_markdown("offer_sprint_checklist.md", "\n".join(md_lines))
    console.print("已写入：", output_path)

    # 练习题答案：
    # 题目：冲刺阶段最重要的事情是什么？
    # 如何添加：
    # 不是继续无限做新功能，而是投递、反馈、复盘、迭代，形成求职闭环。


if __name__ == "__main__":
    main()
