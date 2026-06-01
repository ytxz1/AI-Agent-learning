"""Day 21 优化应用模块。

这个模块把项目扫描、质量评估、提示词优化、功能规划和 UX 评审串起来。
"""

from __future__ import annotations

import json
from pathlib import Path

from .feature_planner import FeaturePlanner
from .project_inspector import ProjectInspector
from .prompt_optimizer import PromptOptimizer
from .quality_evaluator import QualityEvaluator
from .ux_reviewer import UXReviewer


class OptimizationApp:
    """项目优化与调试应用。"""

    def __init__(self, base_dir: str | Path, target_projects: list[str], report_dir: str):
        self.base_dir = Path(base_dir).resolve()
        self.target_projects = target_projects
        self.report_dir = self.base_dir / report_dir
        self.inspector = ProjectInspector(self.base_dir)
        self.evaluator = QualityEvaluator()
        self.prompt_optimizer = PromptOptimizer()
        self.feature_planner = FeaturePlanner()
        self.ux_reviewer = UXReviewer()

    def scan(self, max_preview_chars: int = 500) -> list[dict]:
        """扫描所有目标项目。"""
        snapshots = self.inspector.scan_many(self.target_projects, max_preview_chars=max_preview_chars)
        return [snapshot.__dict__ for snapshot in snapshots]

    def evaluate(self, max_preview_chars: int = 500) -> list[dict]:
        """评估所有目标项目。"""
        snapshots = self.inspector.scan_many(self.target_projects, max_preview_chars=max_preview_chars)
        return self.evaluator.compare(snapshots)

    def feature_plan(self) -> list[dict]:
        """为目标项目生成优化功能清单。"""
        plans = []
        for project in self.target_projects:
            project_name = self.inspector.resolve_project(project).name
            plans.append(self.feature_planner.suggest_features(project_name))
        return plans

    def ux_review(self, max_preview_chars: int = 500) -> list[dict]:
        """生成用户体验评审。"""
        snapshots = self.inspector.scan_many(self.target_projects, max_preview_chars=max_preview_chars)
        return [self.ux_reviewer.review(snapshot) for snapshot in snapshots]

    def prompt_review(self, prompt: str, task_name: str = "项目优化") -> dict:
        """评估一个提示词并返回优化建议。"""
        review = self.prompt_optimizer.review(prompt, task_name=task_name)
        return review.__dict__

    def full_report(self, max_preview_chars: int = 500) -> dict:
        """生成完整优化报告。"""
        return {
            "scan": self.scan(max_preview_chars=max_preview_chars),
            "quality": self.evaluate(max_preview_chars=max_preview_chars),
            "features": self.feature_plan(),
            "ux": self.ux_review(max_preview_chars=max_preview_chars),
        }

    def save_report(self, data: dict, file_name: str = "day21_optimization_report.json") -> str:
        """把报告保存到 output/。"""
        self.report_dir.mkdir(parents=True, exist_ok=True)
        path = self.report_dir / file_name
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(path)
