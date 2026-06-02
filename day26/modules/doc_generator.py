"""项目展示文档生成器。

这个模块用于生成：
- 截图计划；
- GitHub README 亮点段落；
- 项目展示清单。

这些内容会被练习脚本写入 output 文件夹。
"""

from __future__ import annotations

import sys
from pathlib import Path


DAY26_DIR = Path(__file__).resolve().parents[1]
if str(DAY26_DIR) not in sys.path:
    sys.path.insert(0, str(DAY26_DIR))

from config import GITHUB_REPO_URL, PROJECT_NAME

try:
    from .schemas import ScreenshotPlan
except ImportError:
    from schemas import ScreenshotPlan


def build_screenshot_plan() -> list[ScreenshotPlan]:
    """生成截图计划。"""

    return [
        ScreenshotPlan(
            title="FastAPI 自动文档截图",
            target_page="http://127.0.0.1:8000/docs",
            purpose="展示后端 API 已经接口化，支持自动文档。",
            file_name="fastapi-docs.png",
        ),
        ScreenshotPlan(
            title="Agent 问答接口截图",
            target_page="http://127.0.0.1:8000/docs#/Agent%20API",
            purpose="展示 Agent 可以通过 POST 接口调用。",
            file_name="agent-chat-api.png",
        ),
        ScreenshotPlan(
            title="Streamlit 前端页面截图",
            target_page="http://localhost:8501",
            purpose="展示用户可以通过 Web 页面和 Agent 对话。",
            file_name="streamlit-ui.png",
        ),
    ]


def build_readme_highlight_block() -> str:
    """生成可复制到 GitHub README 的亮点段落。"""

    return f"""## 项目亮点

- 完整覆盖 AI Agent 学习链路：Python、API、LangChain、RAG、FastAPI、Docker、Streamlit。
- 后端使用 FastAPI 封装 Agent API，支持自动文档和健康检查。
- 前端使用 Streamlit 构建聊天界面，支持本地模拟和后端 API 两种模式。
- 项目包含详细中文注释、练习题、答案和运行说明，适合复盘和面试展示。
- 仓库地址：{GITHUB_REPO_URL}
"""


def build_project_showcase_checklist() -> str:
    """生成 GitHub 展示检查清单。"""

    return f"""# {PROJECT_NAME} GitHub 展示检查清单

- [ ] README 开头是否说明项目是什么
- [ ] 是否添加项目运行截图
- [ ] 是否写清楚安装依赖命令
- [ ] 是否写清楚运行命令
- [ ] 是否展示项目结构
- [ ] 是否说明核心功能
- [ ] 是否说明技术栈
- [ ] 是否写常见错误
- [ ] 是否添加 GitHub Topics
- [ ] 是否准备演示 GIF 或短视频
"""


if __name__ == "__main__":
    # 练习题答案 5：
    # 如何生成截图计划？
    # 如何添加：调用 build_screenshot_plan()。
    print("练习题答案 5：截图计划")
    for plan in build_screenshot_plan():
        print(plan.model_dump())
