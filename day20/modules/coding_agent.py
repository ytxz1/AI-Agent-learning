"""Coding Agent 主模块。

这个文件把工作区扫描、计划生成、代码草案生成串成完整流程。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Optional

from .coder import ChangeSetBuilder
from .planner import CodingPlanner
from .workspace import WorkspaceInspector


class CodingAgent:
    """一个教学版 Coding Agent。"""

    def __init__(self, workspace_dir: str | Path):
        self.workspace = WorkspaceInspector(workspace_dir)
        self.planner = CodingPlanner()
        self.coder = ChangeSetBuilder()
        self.last_plan: Optional[dict] = None
        self.last_change_set: Optional[dict] = None

    def workspace_summary(self) -> dict:
        """返回工作区摘要。"""
        stats = self.workspace.stats()
        files = self.workspace.summarize_files(max_files=5)
        return {
            "stats": stats,
            "preview_files": [
                {
                    "path": item.path,
                    "size": item.size,
                    "preview": item.preview,
                }
                for item in files
            ],
        }

    def inspect(self, relative_path: str, max_chars: int = 220) -> dict:
        """查看单个文件。"""
        preview = self.workspace.file_preview(relative_path, max_chars=max_chars)
        return {
            "path": preview.path,
            "size": preview.size,
            "preview": preview.preview,
        }

    def scan_tree(self, max_depth: int = 2) -> list[str]:
        """扫描目录树。"""
        return self.workspace.tree_lines(max_depth=max_depth)

    def generate_plan(self, request: str, focus_files: Iterable[str] | None = None) -> dict:
        """生成修改计划。"""
        summary = self.workspace_summary()
        plan = self.planner.generate_plan(request, summary["stats"], focus_files=focus_files)
        self.last_plan = plan
        return plan

    def generate_change_set(self, request: str, focus_files: Iterable[str] | None = None) -> dict:
        """生成代码草案。"""
        if self.last_plan is None:
            self.generate_plan(request, focus_files=focus_files)

        workspace_excerpt = "\n\n".join(
            f"FILE: {item['path']}\n{item['preview']}"
            for item in self.workspace_summary()["preview_files"]
        )
        change_set = self.coder.generate_change_set(
            request,
            self.last_plan or {},
            workspace_excerpt,
            focus_files=focus_files,
        )
        self.last_change_set = change_set
        return change_set

    def pretty_json(self, data: dict) -> str:
        """把结构化数据格式化成 JSON。"""
        return json.dumps(data, ensure_ascii=False, indent=2)

