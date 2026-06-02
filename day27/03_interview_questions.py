"""练习 03：常见面试题准备。

目标：
1. 读取面试题库；
2. 按分类展示问题；
3. 写入 output/interview_questions.md。
"""

from __future__ import annotations

from collections import defaultdict

from rich.console import Console

from modules.interview_bank import InterviewBank
from modules.report_writer import write_markdown


console = Console()


def main() -> None:
    """运行面试题准备。"""

    console.rule("[bold green]练习 03：常见面试题")
    bank = InterviewBank()
    grouped = defaultdict(list)
    for question in bank.list_questions():
        grouped[question.category].append(question)

    md_lines = ["# Day27 常见面试题", ""]
    for category, questions in grouped.items():
        console.print(f"\n[bold]{category}[/bold]")
        md_lines.append(f"## {category}")
        md_lines.append("")
        for item in questions:
            console.print("- ", item.question)
            console.print("  提示：", item.answer_hint)
            md_lines.append(f"### {item.question}")
            md_lines.append("")
            md_lines.append(f"回答提示：{item.answer_hint}")
            md_lines.append("")

    output_path = write_markdown("interview_questions.md", "\n".join(md_lines))
    console.print("\n已写入：", output_path)

    # 练习题答案：
    # 题目：准备面试题时，为什么不能只背标准答案？
    # 如何添加：
    # 因为面试官更看重你是否真的做过、是否能讲清楚细节和取舍。


if __name__ == "__main__":
    main()
