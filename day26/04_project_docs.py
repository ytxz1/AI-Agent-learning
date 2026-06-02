"""练习 04：生成项目文档片段。

这个脚本会生成两个可复制内容：
1. README 项目亮点段落；
2. GitHub 展示检查清单。
"""

from __future__ import annotations

from rich.console import Console

from modules.doc_generator import build_project_showcase_checklist, build_readme_highlight_block
from modules.report_writer import write_text_report


console = Console()


def main() -> None:
    """生成项目文档。"""

    console.rule("[bold green]练习 04：项目文档")
    highlight_block = build_readme_highlight_block()
    checklist = build_project_showcase_checklist()

    highlight_path = write_text_report("readme_highlights.md", highlight_block)
    checklist_path = write_text_report("showcase_checklist.md", checklist)

    console.print("README 亮点段落已生成：", highlight_path)
    console.print("展示检查清单已生成：", checklist_path)

    # 练习题答案：
    # 题目：项目文档应该放在哪里？
    # 如何添加：
    # README 放仓库根目录，详细说明可以放 docs 目录，生成报告可以放 output 目录。


if __name__ == "__main__":
    main()
