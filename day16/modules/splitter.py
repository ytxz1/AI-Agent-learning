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
    # 压缩多余空白，避免换行和多个空格影响切分。
    text = " ".join(text.split())
    if not text:
        return []

    # 如果 chunk_size 不合理，就直接返回整段文本，避免死循环。
    if chunk_size <= 0:
        return [text]

    # overlap 不能大于等于 chunk_size，否则下一段起点无法前进。
    if chunk_overlap >= chunk_size:
        chunk_overlap = max(0, chunk_size // 5)

    chunks: List[str] = []
    start = 0
    total = len(text)

    while start < total:
        # 当前块的结束位置不能超过文本总长度。
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
        # 每份文档都单独切分，避免不同文档内容混在同一个 chunk 里。
        parts = split_text(doc.page_content, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for idx, part in enumerate(parts):
            # 复制 metadata，保留 source/path，同时增加 chunk_index。
            metadata = dict(doc.metadata)
            metadata["chunk_index"] = idx
            chunks.append(DocumentItem(page_content=part, metadata=metadata))

    return chunks
