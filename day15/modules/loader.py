"""文档加载模块。

RAG 的第一步是“把知识库资料读进程序”。
这个模块负责读取 day15/documents/ 下面的 .txt 和 .md 文件，
并统一包装成 DocumentItem 对象，方便后续切分、向量化和检索。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class DocumentItem:
    """项目内部统一使用的文档对象。

    page_content 保存正文内容。
    metadata 保存来源文件名、路径、chunk_index 等附加信息。
    """

    page_content: str
    metadata: dict


def _read_text_file(path: Path) -> str:
    """读取文本文件，并尽量兼容常见中文编码。

    有些中文文件是 UTF-8，有些可能是 GBK。
    这里按顺序尝试不同编码，避免读取中文文档时出现乱码或报错。
    """

    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except Exception:
            continue
    # 如果上面的编码都失败，就忽略错误强行读取，保证流程不中断。
    return path.read_text(errors="ignore")


def load_documents(docs_dir: str) -> List[DocumentItem]:
    """加载指定目录下的所有 .txt 和 .md 文档。"""

    docs_path = Path(docs_dir)
    if not docs_path.exists():
        return []

    documents: List[DocumentItem] = []
    for file_path in sorted(docs_path.rglob("*")):
        # 跳过文件夹，只处理真正的文件。
        if not file_path.is_file():
            continue

        # Day 15 先只支持最容易理解的纯文本格式。
        if file_path.suffix.lower() not in {".txt", ".md"}:
            continue

        text = _read_text_file(file_path).strip()
        if not text:
            continue

        # 把正文和来源信息一起保存，后面检索结果就能显示“来自哪个文件”。
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

