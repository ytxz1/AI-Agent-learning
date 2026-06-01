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
    """项目内部统一使用的文档对象。

    page_content：保存正文。
    metadata：保存来源文件、路径、块编号等附加信息。
    """

    page_content: str
    metadata: dict


def _read_text_file(path: Path) -> str:
    """尽量用几种常见编码读取文本，减少中文乱码问题。"""
    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except Exception:
            continue
    # 如果常见编码都失败，就忽略错误读取，尽量不中断学习流程。
    return path.read_text(errors="ignore")


def load_documents(docs_dir: str) -> List[DocumentItem]:
    """加载目录中的文本文件。"""
    root = Path(docs_dir)
    if not root.exists():
        return []

    documents: List[DocumentItem] = []
    for file_path in sorted(root.rglob("*")):
        # 只处理文件，跳过文件夹。
        if not file_path.is_file():
            continue

        # Day 16 先支持最容易理解的 .txt 和 .md。
        if file_path.suffix.lower() not in {".txt", ".md"}:
            continue

        content = _read_text_file(file_path).strip()
        if not content:
            continue

        # 把正文和来源信息放在一起，后面检索结果可以追踪来源。
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
