"""README 完整度检查器。

GitHub 项目最先被别人看到的通常是 README。
一个好的 README 应该至少包含：
- 项目介绍；
- 功能亮点；
- 项目结构；
- 安装依赖；
- 运行命令；
- 示例截图；
- 常见问题；
- 后续计划。
"""

from __future__ import annotations

import sys
from pathlib import Path


DAY26_DIR = Path(__file__).resolve().parents[1]
if str(DAY26_DIR) not in sys.path:
    sys.path.insert(0, str(DAY26_DIR))

try:
    from .schemas import CheckItem
except ImportError:
    from schemas import CheckItem


class ReadmeReviewer:
    """检查 README 是否足够适合 GitHub 展示。"""

    required_sections = {
        "项目": "建议 README 说明项目是什么。",
        "安装": "建议说明如何安装依赖。",
        "运行": "建议说明如何启动项目。",
        "结构": "建议展示项目目录结构。",
        "练习": "学习型项目建议保留练习题和答案说明。",
        "常见错误": "建议列出初学者容易遇到的问题。",
    }

    def __init__(self, project_dir: Path) -> None:
        self.project_dir = project_dir
        self.readme_path = project_dir / "README.md"

    def review(self) -> list[CheckItem]:
        """检查 README 内容。"""

        if not self.readme_path.exists():
            return [
                CheckItem(
                    title="README 是否存在",
                    passed=False,
                    detail="没有找到 README.md。",
                    suggestion="请先创建 README.md，说明项目功能、运行方式和亮点。",
                )
            ]

        content = self.readme_path.read_text(encoding="utf-8")
        checks = [
            CheckItem(
                title="README 长度是否足够",
                passed=len(content) >= 1500,
                detail=f"README 当前长度约 {len(content)} 个字符。",
                suggestion="GitHub 展示型 README 建议写详细一些，至少包含项目介绍、运行方式、截图和亮点。",
            )
        ]

        for keyword, suggestion in self.required_sections.items():
            checks.append(
                CheckItem(
                    title=f"README 是否包含：{keyword}",
                    passed=keyword in content,
                    detail=f"已找到关键词：{keyword}" if keyword in content else f"未找到关键词：{keyword}",
                    suggestion=suggestion,
                )
            )
        return checks

    def generate_improvement_tips(self) -> list[str]:
        """生成 README 优化建议。"""

        return [
            "在开头用 3-5 句话说明项目解决什么问题。",
            "添加一张运行截图或 GIF，让别人一眼看到效果。",
            "把安装命令、运行命令、访问地址写成可复制的代码块。",
            "用表格列出核心功能，显得更清楚。",
            "补充项目亮点，例如 API、前端界面、Docker 部署、本地 fallback。",
            "增加常见错误，展示你对项目运行问题的理解。",
        ]


if __name__ == "__main__":
    # 练习题答案 3：
    # 如何检查 README？
    # 如何添加：创建 ReadmeReviewer，调用 review()。
    from config import get_target_project_dir

    reviewer = ReadmeReviewer(get_target_project_dir())
    print("练习题答案 3：README 检查结果")
    for check in reviewer.review():
        print(check.model_dump())
