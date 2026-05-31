"""文本切分模块。

长文档通常不能直接一次性拿去做检索，所以需要切成多个小块。
切块时保留一点 overlap，可以避免上下文被切断。
"""

from __future__ import annotations

from typing import Iterable, List

from .loader import DocumentItem


def split_text(text: str, chunk_size: int = 240, chunk_overlap: int = 60) -> List[str]:
    """按字符切分文本。

    这里做一个简单、容易理解的切分器，方便学习向量库基础逻辑。
    """
    text = " ".join(text.split())
    if not text:
        return []

    if chunk_size <= 0:
        return [text]

    if chunk_overlap >= chunk_size:
        chunk_overlap = max(0, chunk_size // 5)

    chunks: List[str] = []
    start = 0
    total = len(text)

    while start < total:
        end = min(start + chunk_size, total)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= total:
            break

        # 下一段从 overlap 位置重新开始，保留一点上下文。
        start = max(0, end - chunk_overlap)
        if start == end:
            start += 1

    return chunks


def split_documents(
    documents: Iterable[DocumentItem],
    chunk_size: int = 240,
    chunk_overlap: int = 60,
) -> List[DocumentItem]:
    """把多份文档切成多个文档块。"""
    chunks: List[DocumentItem] = []

    for doc in documents:
        parts = split_text(doc.page_content, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for idx, part in enumerate(parts):
            metadata = dict(doc.metadata)
            metadata["chunk_index"] = idx
            chunks.append(DocumentItem(page_content=part, metadata=metadata))

    return chunks

