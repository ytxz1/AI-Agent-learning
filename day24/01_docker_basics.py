"""练习 01：Docker 基础概念。

这个脚本不需要真的安装 Docker。
它会用中文解释 Day24 最重要的 Docker 概念：
- 镜像 image
- 容器 container
- Dockerfile
- 端口映射
- 环境变量
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table


console = Console()


def main() -> None:
    """打印 Docker 基础概念表。"""

    console.rule("[bold green]练习 01：Docker 基础概念")

    table = Table(title="Docker 入门关键词")
    table.add_column("概念", style="cyan")
    table.add_column("通俗解释")
    table.add_column("Day24 中的例子")

    table.add_row("镜像 image", "项目打包后的模板", "通过 Dockerfile 构建出来")
    table.add_row("容器 container", "镜像运行后的实例", "day24-deploy-api")
    table.add_row("Dockerfile", "告诉 Docker 如何构建镜像的说明书", "day24/Dockerfile")
    table.add_row("端口映射", "把容器端口暴露到电脑或服务器", "8000:8000")
    table.add_row("环境变量", "部署时传入配置", ".env / docker-compose.yml")

    console.print(table)

    # 练习题答案：
    # 题目：镜像和容器有什么区别？
    # 如何添加：
    # 镜像像“安装包”或“模板”，容器像“真正运行起来的程序”。
    # 一个镜像可以启动多个容器。


if __name__ == "__main__":
    main()
