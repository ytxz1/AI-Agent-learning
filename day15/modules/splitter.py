"""文本切分模块"""

from __future__ import annotations

from dataclasses import replace
from typing import Iterable, List

from .loader import DocumentItem


def split_text(text: str, chunk_size: int = 220, chunk_overlap: int = 50) -> List[str]:
    text = " ".join(text.split())
    if not text:
        return []
    if chunk_size <= 0:
        return [text]
    if chunk_overlap >= chunk_size:
        chunk_overlap = max(0, chunk_size // 5)

    chunks: List[str] = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + chunk_size, length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= length:
            break
        start = end - chunk_overlap
        if start < 0:
            start = 0
        if start == end:
            start += 1
    return chunks


def split_documents(documents: Iterable[DocumentItem], chunk_size: int = 220, chunk_overlap: int = 50) -> List[DocumentItem]:
    chunks: List[DocumentItem] = []
    for doc in documents:
        for idx, chunk in enumerate(split_text(doc.page_content, chunk_size, chunk_overlap)):
            metadata = dict(doc.metadata)
            metadata["chunk_index"] = idx
            chunks.append(DocumentItem(page_content=chunk, metadata=metadata))
    return chunks

