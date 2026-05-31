"""工作区操作模块。

这个模块负责：
- 安全地定位工作区文件
- 扫描文件树
- 读取文件内容
- 生成文件预览
"""

from __future__ import annotations

import fnmatch
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass
class WorkspaceFile:
    """工作区中的一个文件快照。"""

    path: str
    size: int
    preview: str


def _is_within_root(root: Path, candidate: Path) -> bool:
    """判断路径是否在工作区根目录内。"""
    try:
        root_resolved = root.resolve()
        candidate_resolved = candidate.resolve()
        return os.path.commonpath([str(root_resolved), str(candidate_resolved)]) == str(root_resolved)
    except Exception:
        return False


class WorkspaceInspector:
    """负责扫描和读取工作区。"""

    def __init__(self, workspace_dir: str | Path):
        self.root = Path(workspace_dir).resolve()

    def resolve_path(self, relative_path: str | Path) -> Path:
        """把相对路径转换为工作区内的绝对路径。"""
        candidate = (self.root / Path(relative_path)).resolve()
        if not _is_within_root(self.root, candidate):
            raise ValueError(f"路径超出工作区范围：{relative_path}")
        return candidate

    def list_files(
        self,
        patterns: Optional[list[str]] = None,
        max_depth: int = 3,
        max_files: int = 200,
    ) -> list[Path]:
        """列出工作区中的文件。"""
        patterns = patterns or ["*.py", "*.md", "*.txt", "*.json", "*.yml", "*.yaml"]
        results: list[Path] = []

        for path in self.root.rglob("*"):
            if len(results) >= max_files:
                break
            if not path.is_file():
                continue

            rel = path.relative_to(self.root)
            if len(rel.parts) - 1 > max_depth:
                continue

            if any(fnmatch.fnmatch(path.name.lower(), pattern.lower()) for pattern in patterns):
                results.append(path)

        return sorted(results)

    def tree_lines(self, max_depth: int = 2, max_entries: int = 60) -> list[str]:
        """生成简化版目录树。"""
        lines: list[str] = []
        entries = 0
        for path in sorted(self.root.rglob("*")):
            if entries >= max_entries:
                lines.append("... (more)")
                break
            rel = path.relative_to(self.root)
            depth = len(rel.parts)
            if depth > max_depth + 1:
                continue
            indent = "  " * (depth - 1)
            suffix = "/" if path.is_dir() else ""
            lines.append(f"{indent}- {rel.name}{suffix}")
            entries += 1
        return lines

    def read_text(self, relative_path: str | Path, max_chars: Optional[int] = None) -> str:
        """读取文件文本。"""
        path = self.resolve_path(relative_path)
        text = path.read_text(encoding="utf-8", errors="ignore")
        if max_chars is not None:
            return text[:max_chars]
        return text

    def file_preview(self, relative_path: str | Path, max_chars: int = 220) -> WorkspaceFile:
        """生成单个文件的预览。"""
        path = self.resolve_path(relative_path)
        text = self.read_text(path, max_chars=max_chars)
        return WorkspaceFile(path=str(path), size=path.stat().st_size, preview=text)

    def stats(self) -> dict:
        """统计工作区文件信息。"""
        files = [p for p in self.root.rglob("*") if p.is_file()]
        total_size = sum(p.stat().st_size for p in files)
        return {
            "workspace_root": str(self.root),
            "file_count": len(files),
            "total_size": total_size,
        }

    def summarize_files(self, max_files: int = 5, max_chars: int = 220) -> list[WorkspaceFile]:
        """返回一组常见文件的预览。"""
        previews: list[WorkspaceFile] = []
        for path in self.list_files(max_files=max_files):
            previews.append(self.file_preview(path, max_chars=max_chars))
        return previews

