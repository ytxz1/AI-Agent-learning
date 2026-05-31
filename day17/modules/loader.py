"""文档加载模块。

负责把 documents/ 里的文本、Markdown 等文件加载成 LangChain Document 对象。
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document


def resolve_docs_dir(base_dir: str | Path, docs_dir: str) -> Path:
    """把相对路径转换成绝对路径。"""
    base = Path(base_dir)
    return (base / docs_dir).resolve()


def _load_by_glob(docs_path: Path, glob_pattern: str) -> List[Document]:
    """按文件类型加载文档。"""
    if not docs_path.exists():
        return []

    loader = DirectoryLoader(
        str(docs_path),
        glob=glob_pattern,
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        use_multithreading=False,
        show_progress=False,
    )
    return loader.load()


def normalize_metadata(doc: Document) -> Document:
    """补充统一的 metadata，方便后面展示和调试。"""
    source = doc.metadata.get("source", "")
    file_name = os.path.basename(source) if source else "unknown"
    suffix = Path(file_name).suffix.lower()
    doc.metadata["source"] = source
    doc.metadata["file_name"] = file_name
    doc.metadata["file_type"] = suffix or "unknown"
    doc.metadata["doc_length"] = len(doc.page_content)
    return doc


def load_documents(docs_path: str | Path) -> list[Document]:
    """加载 documents/ 目录中的所有 txt 和 md 文档。"""
    path = Path(docs_path)
    docs: list[Document] = []

    docs.extend(_load_by_glob(path, "*.txt"))
    docs.extend(_load_by_glob(path, "*.md"))

    normalized = [normalize_metadata(doc) for doc in docs]
    return normalized


def summarize_documents(documents: Iterable[Document]) -> dict:
    """统计文档数量、类型和字符数。"""
    docs = list(documents)
    summary = {
        "document_count": len(docs),
        "file_types": {},
        "total_chars": 0,
    }

    for doc in docs:
        file_type = doc.metadata.get("file_type", "unknown")
        summary["file_types"][file_type] = summary["file_types"].get(file_type, 0) + 1
        summary["total_chars"] += len(doc.page_content)

    return summary


def preview_documents(documents: Iterable[Document], limit: int = 3, max_chars: int = 160) -> list[str]:
    """生成文档预览内容。"""
    previews: list[str] = []
    for index, doc in enumerate(documents):
        if index >= limit:
            break
        text = doc.page_content.replace("\n", " ").strip()
        snippet = text[:max_chars] + ("..." if len(text) > max_chars else "")
        source = doc.metadata.get("file_name", "unknown")
        previews.append(f"[{index + 1}] {source}: {snippet}")
    return previews

