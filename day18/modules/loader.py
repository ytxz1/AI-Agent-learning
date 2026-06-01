"""文档加载模块。

负责把 documents/ 目录里的文本文件加载成可处理的文档对象。
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class DocumentItem:
    """项目内部使用的文档结构。

    page_content 保存正文内容。
    metadata 保存来源、文件名、文件类型、文档长度等信息。
    """

    page_content: str
    metadata: dict = field(default_factory=dict)


def resolve_docs_dir(base_dir: str | Path, docs_dir: str) -> Path:
    """把相对文档目录转换成绝对路径。"""
    # base_dir 通常是 day18 根目录，docs_dir 通常是 documents。
    return (Path(base_dir) / docs_dir).resolve()


def load_text_file(file_path: Path) -> DocumentItem:
    """读取一个文本文件。"""
    # Day 18 的示例文档统一使用 UTF-8。
    content = file_path.read_text(encoding="utf-8")

    # metadata 后续会跟着 chunk 一起进入检索链。
    metadata = {
        "source": str(file_path),
        "file_name": file_path.name,
        "file_type": file_path.suffix.lower(),
        "doc_length": len(content),
    }
    return DocumentItem(page_content=content, metadata=metadata)


def load_documents(docs_path: str | Path) -> list[DocumentItem]:
    """加载目录下的 txt 和 md 文件。"""
    path = Path(docs_path)
    if not path.exists():
        return []

    documents: list[DocumentItem] = []
    for file_path in sorted(path.iterdir()):
        # 只加载 .txt 和 .md，跳过其他文件。
        if file_path.is_file() and file_path.suffix.lower() in {".txt", ".md"}:
            documents.append(load_text_file(file_path))
    return documents


def summarize_documents(documents: Iterable[DocumentItem]) -> dict:
    """统计文档数量和类型分布。"""
    # Iterable 转 list，方便多次统计。
    docs = list(documents)
    summary = {
        "document_count": len(docs),
        "total_chars": 0,
        "file_types": {},
    }
    for doc in docs:
        file_type = doc.metadata.get("file_type", "unknown")
        # 累加总字符数。
        summary["total_chars"] += len(doc.page_content)
        # 统计不同文件类型数量。
        summary["file_types"][file_type] = summary["file_types"].get(file_type, 0) + 1
    return summary


def preview_documents(documents: Iterable[DocumentItem], limit: int = 3, max_chars: int = 180) -> list[str]:
    """生成文档预览。"""
    previews: list[str] = []
    for index, doc in enumerate(documents):
        # 只展示前 limit 份文档，避免输出过长。
        if index >= limit:
            break
        # 压缩空白，让预览在一行里更容易看。
        text = " ".join(doc.page_content.split())
        snippet = text[:max_chars] + ("..." if len(text) > max_chars else "")
        previews.append(f"[{index + 1}] {doc.metadata.get('file_name', 'unknown')}: {snippet}")
    return previews
