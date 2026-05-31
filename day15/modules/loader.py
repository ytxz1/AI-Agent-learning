"""文档加载模块"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class DocumentItem:
    page_content: str
    metadata: dict


def _read_text_file(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except Exception:
            continue
    return path.read_text(errors="ignore")


def load_documents(docs_dir: str) -> List[DocumentItem]:
    docs_path = Path(docs_dir)
    if not docs_path.exists():
        return []

    documents: List[DocumentItem] = []
    for file_path in sorted(docs_path.rglob("*")):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in {".txt", ".md"}:
            continue
        text = _read_text_file(file_path).strip()
        if not text:
            continue
        documents.append(
            DocumentItem(
                page_content=text,
                metadata={
                    "source": file_path.name,
                    "path": str(file_path),
                },
            )
        )
    return documents

