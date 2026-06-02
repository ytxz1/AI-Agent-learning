"""简历项目经历生成器。

简历 bullet 的重点不是“我做了什么流水账”，而是：
- 使用了什么技术；
- 解决了什么问题；
- 产出了什么结果；
- 能体现什么能力。
"""

from __future__ import annotations

import sys
from pathlib import Path


DAY27_DIR = Path(__file__).resolve().parents[1]
if str(DAY27_DIR) not in sys.path:
    sys.path.insert(0, str(DAY27_DIR))

try:
    from .schemas import ProjectProfile, ResumeBullet
except ImportError:
    from schemas import ProjectProfile, ResumeBullet


class ResumeBuilder:
    """根据项目素材生成简历项目经历。"""

    def __init__(self, profile: ProjectProfile) -> None:
        self.profile = profile

    def build_bullets(self) -> list[ResumeBullet]:
        """生成简历 bullet。"""

        return [
            ResumeBullet(
                content=(
                    f"基于 {self.profile.duration} 学习计划独立完成 {self.profile.project_name}，"
                    "覆盖 Agent API、RAG、部署和前端展示等完整链路。"
                ),
                focus="项目完整度",
            ),
            ResumeBullet(
                content=(
                    "使用 FastAPI 将 Agent 能力封装为 REST API，支持普通问答、"
                    "流式响应、健康检查和统一错误处理。"
                ),
                focus="后端接口化能力",
            ),
            ResumeBullet(
                content=(
                    "设计本地 fallback 方案，在未配置 API Key 或在线模型异常时仍可完整演示项目。"
                ),
                focus="工程稳定性",
            ),
            ResumeBullet(
                content=(
                    "使用 Dockerfile 和 docker-compose 编写部署配置，并通过健康检查接口验证服务状态。"
                ),
                focus="部署能力",
            ),
            ResumeBullet(
                content=(
                    "使用 Streamlit 构建聊天前端，支持本地模拟和后端 API 两种模式，提升项目展示效果。"
                ),
                focus="前端展示能力",
            ),
        ]

    def build_resume_section(self) -> str:
        """生成可复制到简历里的 Markdown 文本。"""

        lines = [
            f"**{self.profile.project_name}｜Python / FastAPI / Streamlit / Docker**",
            "",
        ]
        lines.extend([f"- {bullet.content}" for bullet in self.build_bullets()])
        return "\n".join(lines)


if __name__ == "__main__":
    # 练习题答案 3：
    # 如何生成简历项目经历？
    # 如何添加：加载 profile，创建 ResumeBuilder，调用 build_resume_section()。
    from profile_loader import load_project_profile

    builder = ResumeBuilder(load_project_profile())
    print("练习题答案 3：简历项目经历")
    print(builder.build_resume_section())
