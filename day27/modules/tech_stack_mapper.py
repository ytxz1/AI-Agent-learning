"""技术栈梳理器。

面试时只说“我用过 FastAPI”是不够的。
更好的表达是：
- 我用它做了什么；
- 为什么使用它；
- 遇到了什么问题；
- 我掌握到了什么程度。
"""

from __future__ import annotations

import sys
from pathlib import Path


DAY27_DIR = Path(__file__).resolve().parents[1]
if str(DAY27_DIR) not in sys.path:
    sys.path.insert(0, str(DAY27_DIR))

try:
    from .schemas import ProjectProfile
except ImportError:
    from schemas import ProjectProfile


class TechStackMapper:
    """把技术栈转化为面试可讲内容。"""

    explanations = {
        "Python": "用于编写核心脚本、API 服务、数据处理和工具函数。",
        "FastAPI": "用于将 Agent 能力封装成 REST API，并生成自动接口文档。",
        "Pydantic": "用于请求参数和响应结构校验，让接口数据更稳定。",
        "Streamlit": "用于快速构建聊天前端，让项目可交互、可展示。",
        "Docker": "用于容器化部署，保证项目在不同环境中更稳定运行。",
        "LangChain": "用于理解 Agent、Chain、Tools、Memory 等 AI 应用组件。",
        "RAG": "用于学习文档加载、向量化、检索和增强生成流程。",
        "OpenAI API": "用于调用大模型，同时通过 fallback 降低在线依赖。",
        "GitHub": "用于项目展示、文档整理和求职作品集沉淀。",
    }

    def __init__(self, profile: ProjectProfile) -> None:
        self.profile = profile

    def build_stack_table(self) -> list[dict[str, str]]:
        """生成技术栈解释表。"""

        rows = []
        for tech in self.profile.tech_stack:
            rows.append(
                {
                    "tech": tech,
                    "usage": self.explanations.get(tech, "用于项目功能实现。"),
                    "interview_tip": f"面试时不要只说用过 {tech}，要结合项目说明具体场景。",
                }
            )
        return rows


if __name__ == "__main__":
    # 练习题答案 4：
    # 如何梳理技术栈？
    # 如何添加：创建 TechStackMapper，调用 build_stack_table()。
    from profile_loader import load_project_profile

    mapper = TechStackMapper(load_project_profile())
    print("练习题答案 4：技术栈梳理")
    for row in mapper.build_stack_table():
        print(row)
