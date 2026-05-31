"""文档加载模块。

这个模块负责把 documents/ 目录中的 txt 或 md 文本读出来，
并包装成统一的数据结构，方便后续切分和向量化。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class DocumentItem:
    """表示一份文档。"""

    page_content: str
    metadata: dict


def _read_text_file(path: Path) -> str:
    """尽量用几种常见编码读取文本，减少中文乱码问题。"""
    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except Exception:
            continue
    return path.read_text(errors="ignore")


def load_documents(docs_dir: str) -> List[DocumentItem]:
    """加载目录中的文本文件。"""
    root = Path(docs_dir)
    if not root.exists():
        return []

    documents: List[DocumentItem] = []
    for file_path in sorted(root.rglob("*")):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in {".txt", ".md"}:
            continue

        content = _read_text_file(file_path).strip()
        if not content:
            continue

        documents.append(
            DocumentItem(
                page_content=content,
                metadata={
                    "source": file_path.name,
                    "path": str(file_path),
                },
            )
        )

    return documents

