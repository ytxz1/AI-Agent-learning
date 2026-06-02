"""练习 02：理解镜像构建流程。

这个脚本会读取 Dockerfile，并解释每一类指令的作用。
不需要真的执行 docker build，也可以先理解构建步骤。
"""

from __future__ import annotations

from pathlib import Path

from rich.console import Console


console = Console()
DAY24_DIR = Path(__file__).resolve().parent
DOCKERFILE = DAY24_DIR / "Dockerfile"


def explain_instruction(line: str) -> str:
    """解释 Dockerfile 中的一行指令。"""

    if line.startswith("FROM"):
        return "选择基础镜像。"
    if line.startswith("ENV"):
        return "设置容器环境变量。"
    if line.startswith("WORKDIR"):
        return "设置容器工作目录。"
    if line.startswith("COPY"):
        return "复制文件到镜像。"
    if line.startswith("RUN"):
        return "构建镜像时执行命令。"
    if line.startswith("EXPOSE"):
        return "声明容器会使用的端口。"
    if line.startswith("CMD"):
        return "容器启动时执行的命令。"
    return "注释或其他说明。"


def main() -> None:
    """打印 Dockerfile 构建流程解释。"""

    console.rule("[bold green]练习 02：镜像构建流程")
    for line in DOCKERFILE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        console.print(f"{stripped}")
        console.print(f"  解释：{explain_instruction(stripped)}")

    console.print("\n推荐构建命令：docker build -t day24-deploy-api .")

    # 练习题答案：
    # 题目：为什么先 COPY requirements.txt，再 COPY 全部代码？
    # 如何添加：
    # 因为 Docker 有缓存机制。依赖不变时，可以复用 pip install 这一层，
    # 代码修改后不必每次重新安装依赖，构建更快。


if __name__ == "__main__":
    main()
