"""练习 04：自我介绍准备。

目标：
生成 1 分钟自我介绍模板。
"""

from __future__ import annotations

from rich.console import Console

from config import CANDIDATE_NAME, TARGET_ROLE
from modules.profile_loader import load_project_profile
from modules.report_writer import write_markdown


console = Console()


def build_self_intro() -> str:
    """生成自我介绍。"""

    profile = load_project_profile()
    return f"""# 1 分钟自我介绍

面试官您好，我叫 {CANDIDATE_NAME}，目前正在准备 {TARGET_ROLE} 方向的实习。

我最近系统完成了一个「{profile.project_name}」，这个项目按照 1 个月学习计划推进，覆盖了 Python 基础、FastAPI 接口化、RAG、Agent 工具调用、Docker 部署和 Streamlit 前端展示。

在这个项目里，我重点练习了把 AI 能力从脚本变成可调用 API 的过程。例如，我使用 FastAPI 封装 Agent 问答接口，使用 Streamlit 做前端页面，并通过 Dockerfile 和 docker-compose 准备部署配置。

项目中我也特别注意工程稳定性，比如在没有 API Key 或在线模型异常时，设计了本地 fallback，让项目仍然可以完整演示。

我希望通过这个实习继续深入 AI Agent 工程化，把模型能力真正做成稳定、可用、易展示的产品功能。
"""


def main() -> None:
    """生成自我介绍文件。"""

    console.rule("[bold green]练习 04：自我介绍准备")
    intro = build_self_intro()
    output_path = write_markdown("self_intro.md", intro)
    console.print(intro)
    console.print("已写入：", output_path)

    # 练习题答案：
    # 题目：自我介绍应该控制在多久？
    # 如何添加：
    # 通常控制在 1 分钟左右，重点说方向、项目、技术栈和求职目标。


if __name__ == "__main__":
    main()
