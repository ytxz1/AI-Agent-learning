"""项目质量评估模块。

这个模块用本地规则给项目打分。
它不是替代人工 review，而是帮你快速发现“README、配置、练习、入口、注释”这些基础项是否齐全。
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from .project_inspector import ProjectSnapshot


class QualityEvaluator:
    """项目质量评估器。"""

    def evaluate(self, snapshot: ProjectSnapshot) -> dict:
        """对项目快照进行评分。"""
        score = 0
        findings: list[str] = []
        suggestions: list[str] = []

        if "README.md" in snapshot.config_files:
            score += 20
            findings.append("包含 README.md")
        else:
            suggestions.append("补充详细 README.md")

        if "config.py" in snapshot.config_files:
            score += 15
            findings.append("包含 config.py")
        else:
            suggestions.append("补充统一配置文件 config.py")

        if "main.py" in snapshot.python_files:
            score += 15
            findings.append("包含 main.py 统一入口")
        else:
            suggestions.append("补充 main.py 统一入口")

        exercise_count = sum(1 for item in snapshot.python_files if item.startswith("0") or item.startswith("exercise"))
        if exercise_count >= 5:
            score += 20
            findings.append("练习脚本数量充足")
        else:
            suggestions.append("至少准备 5 个练习脚本")

        # README 的练习题专区通常不在开头，所以这里读取完整 README，避免误判。
        readme_path = Path(snapshot.root) / "README.md"
        if readme_path.exists():
            readme_preview = readme_path.read_text(encoding="utf-8", errors="ignore")
        else:
            readme_preview = snapshot.key_previews.get("README.md", "")
        if "练习题专区" in readme_preview or "练习题" in readme_preview:
            score += 15
            findings.append("README 包含练习题说明")
        else:
            suggestions.append("README 增加练习题专区")

        if "API" in readme_preview or "本地" in readme_preview:
            score += 15
            findings.append("README 说明了运行模式")
        else:
            suggestions.append("README 增加 API Key / 本地模式说明")

        return {
            "project": snapshot.name,
            "score": min(score, 100),
            "snapshot": asdict(snapshot),
            "findings": findings,
            "suggestions": suggestions,
        }

    def compare(self, snapshots: list[ProjectSnapshot]) -> list[dict]:
        """批量评估多个项目。"""
        return [self.evaluate(snapshot) for snapshot in snapshots]
