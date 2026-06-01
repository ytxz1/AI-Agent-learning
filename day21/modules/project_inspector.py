"""项目扫描模块。

这个模块负责读取目标项目的文件结构和关键文件内容。
Day 21 的优化不是凭空想象，而是先看 Day 19 / Day 20 当前有什么。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class ProjectSnapshot:
    """一个项目的扫描快照。"""

    name: str
    root: str
    file_count: int
    python_files: list[str]
    markdown_files: list[str]
    config_files: list[str]
    key_previews: dict[str, str]


class ProjectInspector:
    """扫描和读取项目文件。"""

    def __init__(self, base_dir: str | Path):
        # base_dir 通常是 day21 目录。
        self.base_dir = Path(base_dir).resolve()

    def resolve_project(self, project_path: str | Path) -> Path:
        """把目标项目路径解析成绝对路径。"""
        path = Path(project_path)
        if not path.is_absolute():
            path = (self.base_dir / path).resolve()
        return path

    def _safe_read(self, path: Path, max_chars: int = 500) -> str:
        """安全读取文本文件预览。"""
        try:
            return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]
        except Exception as exc:
            return f"读取失败：{exc}"

    def scan(self, project_path: str | Path, max_preview_chars: int = 500) -> ProjectSnapshot:
        """扫描单个项目，返回结构化快照。"""
        root = self.resolve_project(project_path)
        files = [item for item in root.rglob("*") if item.is_file()]
        python_files = [str(item.relative_to(root)) for item in files if item.suffix == ".py"]
        markdown_files = [str(item.relative_to(root)) for item in files if item.suffix.lower() == ".md"]
        config_files = [
            str(item.relative_to(root))
            for item in files
            if item.name in {"config.py", ".env.example", "requirements.txt", "README.md"}
        ]

        # 重点预览 README、main.py、config.py，优化项目时最常看这些文件。
        key_previews: dict[str, str] = {}
        for name in ["README.md", "main.py", "config.py"]:
            target = root / name
            if target.exists():
                key_previews[name] = self._safe_read(target, max_preview_chars)

        return ProjectSnapshot(
            name=root.name,
            root=str(root),
            file_count=len(files),
            python_files=python_files,
            markdown_files=markdown_files,
            config_files=config_files,
            key_previews=key_previews,
        )

    def scan_many(self, project_paths: Iterable[str | Path], max_preview_chars: int = 500) -> list[ProjectSnapshot]:
        """批量扫描多个项目。"""
        return [self.scan(path, max_preview_chars=max_preview_chars) for path in project_paths]
