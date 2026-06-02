"""项目结构扫描器。

Day26 要优化 GitHub 仓库，第一步就是知道项目里有什么：
- 有没有 README；
- 有没有 requirements.txt；
- 有没有主入口；
- 有没有模块目录；
- 有没有文档目录；
- 有没有截图或 assets。
"""

from __future__ import annotations

import sys
from pathlib import Path


DAY26_DIR = Path(__file__).resolve().parents[1]
if str(DAY26_DIR) not in sys.path:
    sys.path.insert(0, str(DAY26_DIR))

from config import IGNORE_OUTPUT

try:
    from .schemas import CheckItem, ProjectFile
except ImportError:
    from schemas import CheckItem, ProjectFile


class ProjectScanner:
    """扫描目标项目结构。"""

    def __init__(self, project_dir: Path) -> None:
        self.project_dir = project_dir

    def list_files(self) -> list[ProjectFile]:
        """列出项目中的文件。"""

        files: list[ProjectFile] = []
        if not self.project_dir.exists():
            return files

        for file_path in self.project_dir.rglob("*"):
            if not file_path.is_file():
                continue
            if IGNORE_OUTPUT and "output" in file_path.parts:
                continue

            relative_path = file_path.relative_to(self.project_dir).as_posix()
            files.append(
                ProjectFile(
                    path=relative_path,
                    suffix=file_path.suffix or "[无后缀]",
                    size=file_path.stat().st_size,
                    description=self._describe_file(file_path),
                )
            )
        return files

    def check_structure(self) -> list[CheckItem]:
        """检查 GitHub 项目常见结构是否完整。"""

        checks = [
            self._check_exists("README.md", "README 是 GitHub 项目的门面。"),
            self._check_exists("requirements.txt", "requirements.txt 说明项目依赖。"),
            self._check_any(["main.py", "app.py"], "项目应该有清晰的主入口。"),
            self._check_exists("modules", "modules 文件夹能让代码结构更清楚。"),
        ]

        assets_dir = self.project_dir / "assets"
        docs_dir = self.project_dir / "docs"
        checks.append(
            CheckItem(
                title="是否准备截图或资源目录",
                passed=assets_dir.exists(),
                detail="已找到 assets 目录。" if assets_dir.exists() else "还没有 assets 目录。",
                suggestion="建议准备 screenshots 或 assets 目录，用来存放运行截图、架构图或 GIF。",
            )
        )
        checks.append(
            CheckItem(
                title="是否准备项目文档目录",
                passed=docs_dir.exists(),
                detail="已找到 docs 目录。" if docs_dir.exists() else "还没有 docs 目录。",
                suggestion="建议准备 docs 目录，放接口说明、部署说明、学习总结等文档。",
            )
        )
        return checks

    def _check_exists(self, relative_path: str, suggestion: str) -> CheckItem:
        """检查单个路径是否存在。"""

        target = self.project_dir / relative_path
        return CheckItem(
            title=f"检查 {relative_path}",
            passed=target.exists(),
            detail=f"{relative_path} 存在。" if target.exists() else f"{relative_path} 不存在。",
            suggestion=suggestion,
        )

    def _check_any(self, relative_paths: list[str], suggestion: str) -> CheckItem:
        """检查多个路径中是否至少存在一个。"""

        existing = [path for path in relative_paths if (self.project_dir / path).exists()]
        return CheckItem(
            title=f"检查主入口 {' / '.join(relative_paths)}",
            passed=bool(existing),
            detail=f"已找到：{', '.join(existing)}" if existing else "没有找到主入口文件。",
            suggestion=suggestion,
        )

    def _describe_file(self, file_path: Path) -> str:
        """根据文件类型生成简单说明。"""

        suffix = file_path.suffix.lower()
        if file_path.name == "README.md":
            return "项目说明文档"
        if file_path.name == "requirements.txt":
            return "Python 依赖文件"
        if file_path.name in {"main.py", "app.py"}:
            return "项目主入口"
        if suffix == ".py":
            return "Python 源代码"
        if suffix == ".md":
            return "Markdown 文档"
        if suffix in {".png", ".jpg", ".jpeg", ".gif"}:
            return "图片或演示资源"
        return "项目文件"


if __name__ == "__main__":
    # 练习题答案 2：
    # 如何扫描一个项目目录？
    # 如何添加：创建 ProjectScanner，调用 list_files() 和 check_structure()。
    from config import get_target_project_dir

    scanner = ProjectScanner(get_target_project_dir())
    print("练习题答案 2：文件数量", len(scanner.list_files()))
    for check in scanner.check_structure():
        print(check.model_dump())
