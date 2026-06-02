"""练习 01：整理代码结构。

目标：
1. 扫描目标项目文件；
2. 检查 README、requirements、主入口、modules 是否存在；
3. 输出结构优化建议。
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from config import get_target_project_dir
from modules.project_scanner import ProjectScanner


console = Console()


def main() -> None:
    """运行代码结构检查。"""

    project_dir = get_target_project_dir()
    scanner = ProjectScanner(project_dir)

    console.rule("[bold green]练习 01：整理代码结构")
    console.print("目标项目：", project_dir)

    table = Table(title="结构检查结果")
    table.add_column("检查项")
    table.add_column("状态")
    table.add_column("建议")

    for check in scanner.check_structure():
        table.add_row(check.title, "通过" if check.passed else "需要优化", check.suggestion)
    console.print(table)

    console.print("\n前 10 个文件：")
    for project_file in scanner.list_files()[:10]:
        console.print(project_file.model_dump())

    # 练习题答案：
    # 题目：GitHub 项目最少应该有哪些文件？
    # 如何添加：
    # 至少建议有 README.md、requirements.txt、main.py 或 app.py、modules 目录。


if __name__ == "__main__":
    main()
