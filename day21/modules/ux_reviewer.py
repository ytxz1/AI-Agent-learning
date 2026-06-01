"""用户体验评审模块。

这个模块从学习项目角度检查 CLI 体验是否友好：
- 有没有统一入口
- 有没有菜单
- 有没有示例
- 有没有错误提示
- 有没有 output 保存能力
"""

from __future__ import annotations

from pathlib import Path

from .project_inspector import ProjectSnapshot


class UXReviewer:
    """CLI 用户体验评审器。"""

    def review(self, snapshot: ProjectSnapshot) -> dict:
        """生成用户体验评审报告。"""
        # UX 评审也读取完整 main.py / README.md，避免只看开头导致误判。
        main_path = Path(snapshot.root) / "main.py"
        readme_path = Path(snapshot.root) / "README.md"
        main_preview = main_path.read_text(encoding="utf-8", errors="ignore") if main_path.exists() else snapshot.key_previews.get("main.py", "")
        readme_preview = readme_path.read_text(encoding="utf-8", errors="ignore") if readme_path.exists() else snapshot.key_previews.get("README.md", "")
        suggestions: list[str] = []
        positives: list[str] = []

        if "命令" in main_preview or "菜单" in main_preview:
            positives.append("主入口包含命令或菜单提示")
        else:
            suggestions.append("在主入口增加命令菜单")

        if "example" in main_preview.lower() or "demo" in main_preview.lower():
            positives.append("包含示例命令")
        else:
            suggestions.append("增加 example/demo 命令，降低上手难度")

        if "output" in main_preview.lower() or "保存" in main_preview:
            positives.append("包含结果保存能力或保存说明")
        else:
            suggestions.append("增加 output 保存功能，方便复盘结果")

        if "如何运行" in readme_preview or "运行方式" in readme_preview:
            positives.append("README 包含运行说明")
        else:
            suggestions.append("README 增加清晰运行方式")

        return {
            "project": snapshot.name,
            "positives": positives,
            "suggestions": suggestions,
        }
