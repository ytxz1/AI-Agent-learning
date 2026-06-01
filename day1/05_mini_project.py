"""Day 1 - 综合小项目：学习记录分析器。"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from config import OUTPUT_DIR, SAMPLE_NOTES_FILE
from modules.basics import count_words
from modules.file_tools import read_text_file, summarize_text_file, write_text_file


console = Console()


def build_learning_report() -> str:
    """读取学习笔记并生成一份文本报告。"""
    text = read_text_file(SAMPLE_NOTES_FILE)
    summary = summarize_text_file(SAMPLE_NOTES_FILE)
    top_words = count_words(text)

    lines = [
        "Day 1 综合小项目：学习记录分析器",
        "",
        "一、文件统计",
        f"- 字符数：{summary['char_count']}",
        f"- 行数：{summary['line_count']}",
        f"- 单词数：{summary['word_count']}",
        "",
        "二、高频词",
    ]
    lines.extend([f"- {word}: {count}" for word, count in top_words])
    lines.extend([
        "",
        "三、学习建议",
        "- 先把变量和数据类型练熟。",
        "- 再用条件和循环处理简单数据。",
        "- 最后把重复代码封装成函数。",
    ])
    return "\n".join(lines)


def main() -> None:
    report = build_learning_report()
    output_file = OUTPUT_DIR / "mini_project_report.txt"
    write_text_file(output_file, report)

    table = Table(title="综合小项目输出", show_header=True)
    table.add_column("项目", style="cyan")
    table.add_column("结果", style="green")
    table.add_row("报告文件", str(output_file))
    table.add_row("报告长度", f"{len(report)} 字符")
    console.print(table)
    console.print("\n[bold cyan]报告预览：[/bold cyan]")
    console.print(report, style="yellow")


if __name__ == "__main__":
    main()

