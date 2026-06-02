"""GitHub 展示优化建议生成器。

Day26 的重点不是“代码能跑”，而是“别人看到你的仓库时觉得它完整、清楚、可信”。
这个模块会根据扫描结果和 README 检查结果生成仓库优化报告。
"""

from __future__ import annotations

import sys
from pathlib import Path


DAY26_DIR = Path(__file__).resolve().parents[1]
if str(DAY26_DIR) not in sys.path:
    sys.path.insert(0, str(DAY26_DIR))

from config import PROJECT_NAME

try:
    from .project_scanner import ProjectScanner
    from .readme_reviewer import ReadmeReviewer
    from .schemas import CheckItem, GitHubReport
except ImportError:
    from project_scanner import ProjectScanner
    from readme_reviewer import ReadmeReviewer
    from schemas import CheckItem, GitHubReport


class GitHubAdvisor:
    """生成 GitHub 仓库优化报告。"""

    def __init__(self, project_dir: Path) -> None:
        self.project_dir = project_dir
        self.scanner = ProjectScanner(project_dir)
        self.readme_reviewer = ReadmeReviewer(project_dir)

    def build_report(self) -> GitHubReport:
        """生成完整优化报告。"""

        checks = self.scanner.check_structure() + self.readme_reviewer.review()
        score = self._calculate_score(checks)
        return GitHubReport(
            project_name=PROJECT_NAME,
            target_path=str(self.project_dir),
            score=score,
            checks=checks,
            highlights=self._build_highlights(),
            next_actions=self._build_next_actions(checks),
        )

    def _calculate_score(self, checks: list[CheckItem]) -> int:
        """根据检查通过率计算分数。"""

        if not checks:
            return 0
        passed_count = sum(1 for check in checks if check.passed)
        return round(passed_count / len(checks) * 100)

    def _build_highlights(self) -> list[str]:
        """生成项目亮点。"""

        return [
            "项目按 day 组织，学习路径清楚。",
            "包含 FastAPI、Agent API、Docker、Streamlit 前端等完整链路。",
            "README 和代码注释适合初学者复盘。",
            "本地 fallback 设计降低了 API Key 和网络依赖。",
        ]

    def _build_next_actions(self, checks: list[CheckItem]) -> list[str]:
        """根据未通过检查生成下一步行动。"""

        actions = [check.suggestion for check in checks if not check.passed]
        actions.extend(
            [
                "给 README 添加项目运行截图。",
                "在 GitHub 仓库首页添加 Topics：python、fastapi、agent、rag、streamlit。",
                "补充一段 30 秒演示 GIF，展示从提问到回答的流程。",
            ]
        )
        return list(dict.fromkeys(actions))


if __name__ == "__main__":
    # 练习题答案 4：
    # 如何生成 GitHub 优化报告？
    # 如何添加：创建 GitHubAdvisor，调用 build_report()。
    from config import get_target_project_dir

    report = GitHubAdvisor(get_target_project_dir()).build_report()
    print("练习题答案 4：GitHub 优化分数", report.score)
    print(report.model_dump())
