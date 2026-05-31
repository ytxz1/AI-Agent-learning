"""Day 13 - 输出解析模块：把自然语言整理成结构化结果。

这个练习文件用于演示：
- 如何把用户输入变成 JSON
- 如何从文本里提取关键词、实体和意图
- 如何在 LLM 不可用时用规则兜底
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from modules.output_parser import OutputParserModule

console = Console()


def main() -> None:
    """运行一个小型的输出解析演示。"""
    console.print("=" * 60, style="bold blue")
    console.print("Day 13 - 输出解析模块演示", style="bold blue")
    console.print("=" * 60, style="bold blue")

    parser = OutputParserModule()
    init_result = parser.init()
    console.print(f"初始化结果：{init_result}", style="green")

    samples = parser.demo_samples()
    for index, sample in enumerate(samples, 1):
        console.print(f"\n[bold cyan]样例 {index}[/bold cyan]", style="cyan")
        console.print(f"原始输入：{sample}", style="yellow")
        console.print("结构化输出：", style="magenta")
        console.print(parser.query(sample), style="green")

    console.print("\n[bold green]输出解析模块演示完成[/bold green]")


if __name__ == "__main__":
    main()
