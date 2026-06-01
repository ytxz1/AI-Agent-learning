"""Day 1 - 练习 4：文件操作。"""

from __future__ import annotations

from rich.console import Console

from config import OUTPUT_REPORT_FILE, SAMPLE_NOTES_FILE
from modules.basics import count_words
from modules.file_tools import append_line, read_text_file, summarize_text_file, write_text_file


console = Console()

console.print("=" * 60, style="bold blue")
console.print("文件读取", style="bold blue")
console.print("=" * 60, style="bold blue")

text = read_text_file(SAMPLE_NOTES_FILE)
console.print(text, style="green")

summary = summarize_text_file(SAMPLE_NOTES_FILE)
console.print("\n[bold cyan]文件统计：[/bold cyan]")
console.print(summary, style="yellow")

top_words = count_words(text)
report_lines = [
    "Day 1 文件操作报告",
    f"来源文件：{SAMPLE_NOTES_FILE}",
    f"字符数：{summary['char_count']}",
    f"行数：{summary['line_count']}",
    f"单词数：{summary['word_count']}",
    "高频词：",
]
report_lines.extend([f"- {word}: {count}" for word, count in top_words])

write_text_file(OUTPUT_REPORT_FILE, "\n".join(report_lines))
append_line(OUTPUT_REPORT_FILE, "报告生成完成。")

console.print(f"\n报告已生成：{OUTPUT_REPORT_FILE}", style="bold green")

