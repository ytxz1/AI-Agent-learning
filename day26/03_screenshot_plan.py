"""练习 03：添加截图和 GIF 计划。

一个有截图的 GitHub 项目更容易被别人理解。
这个脚本会生成建议截图清单。
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from modules.doc_generator import build_screenshot_plan


console = Console()


def main() -> None:
    """打印截图计划。"""

    console.rule("[bold green]练习 03：截图和 GIF 计划")
    table = Table(title="建议截图清单")
    table.add_column("标题")
    table.add_column("页面")
    table.add_column("用途")
    table.add_column("文件名")

    for plan in build_screenshot_plan():
        table.add_row(plan.title, plan.target_page, plan.purpose, plan.file_name)
    console.print(table)

    # 练习题答案：
    # 题目：为什么 README 里最好放截图？
    # 如何添加：
    # 截图能让别人不用运行项目，也能快速理解项目效果和完成度。


if __name__ == "__main__":
    main()
