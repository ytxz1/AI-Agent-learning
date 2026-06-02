"""练习 03：容器运行配置检查。

这个脚本检查 docker-compose.yml 是否存在，并打印关键运行命令。
它不会真的启动 Docker，所以没有安装 Docker 也能学习。
"""

from __future__ import annotations

from pathlib import Path

from rich.console import Console


console = Console()
DAY24_DIR = Path(__file__).resolve().parent
COMPOSE_FILE = DAY24_DIR / "docker-compose.yml"


def main() -> None:
    """检查容器运行配置。"""

    console.rule("[bold green]练习 03：容器运行配置检查")
    console.print("docker-compose.yml 是否存在：", COMPOSE_FILE.exists())
    console.print()
    console.print("常用命令：")
    console.print("  docker compose up --build       构建并启动容器")
    console.print("  docker compose up -d --build    后台构建并启动容器")
    console.print("  docker compose ps               查看容器状态")
    console.print("  docker compose logs -f          查看实时日志")
    console.print("  docker compose down             停止并删除容器")

    # 练习题答案：
    # 题目：为什么 Docker 中 FastAPI 要监听 0.0.0.0？
    # 如何添加：
    # 127.0.0.1 只允许容器内部访问；
    # 0.0.0.0 才能让容器外部通过端口映射访问服务。


if __name__ == "__main__":
    main()
