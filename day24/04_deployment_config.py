"""练习 04：部署配置检查。

这个脚本会读取 config.py 中的配置，并检查部署前要注意的关键点。
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from config import DOCS_URL, ENVIRONMENT, HOST, PORT, REDOC_URL, SERVICE_NAME
from modules.deployment_info import get_deploy_checklist


console = Console()


def main() -> None:
    """打印部署配置和检查清单。"""

    console.rule("[bold green]练习 04：部署配置检查")

    table = Table(title="当前部署配置")
    table.add_column("配置项", style="cyan")
    table.add_column("当前值")
    table.add_row("SERVICE_NAME", SERVICE_NAME)
    table.add_row("ENVIRONMENT", ENVIRONMENT)
    table.add_row("HOST", HOST)
    table.add_row("PORT", str(PORT))
    table.add_row("DOCS_URL", DOCS_URL)
    table.add_row("REDOC_URL", REDOC_URL)
    console.print(table)

    console.print("\n部署检查清单：")
    for item in get_deploy_checklist():
        status = "通过" if item.passed else "需要处理"
        console.print(f"- {item.title}：{status}，建议：{item.suggestion}")

    # 练习题答案：
    # 题目：生产环境是否一定要开放 /docs？
    # 如何添加：
    # 不一定。内部项目可以保留，公开项目建议关闭或加访问控制。
    # 本项目在 ENVIRONMENT=production 时会关闭 docs_url 和 redoc_url。


if __name__ == "__main__":
    main()
