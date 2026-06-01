"""文本切分模块。

文档通常很长，不能全部直接放进一次模型请求里。
所以 RAG 会先把长文档切成多个小块，再根据问题检索最相关的小块。
这个模块就是负责完成“长文本 -> 多个 chunk”的步骤。
"""

from __future__ import annotations

from typing import Iterable, List

from .loader import DocumentItem


def split_text(text: str, chunk_size: int = 220, chunk_overlap: int = 50) -> List[str]:
    """把一段长文本切成多个较短文本块。

    参数说明：
    text：原始长文本。
    chunk_size：每个文本块最多保留多少个字符。
    chunk_overlap：相邻文本块之间重叠多少个字符。
    """

    # 先把多余空白压缩成一个空格，避免换行和缩进影响切分效果。
    text = " ".join(text.split())
    if not text:
        return []

    # 如果 chunk_size 设置不合理，就直接返回整段文本，避免死循环。
    if chunk_size <= 0:
        return [text]

    # overlap 不能大于等于 chunk_size，否则切分时 start 可能无法前进。
    if chunk_overlap >= chunk_size:
        chunk_overlap = max(0, chunk_size // 5)

    chunks: List[str] = []
    start = 0
    length = len(text)

    while start < length:
        # end 是当前 chunk 的结束位置，不能超过文本总长度。
        end = min(start + chunk_size, length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # 已经切到最后，就退出循环。
        if end >= length:
            break

        # 下一块不是从 end 开始，而是往前回退 chunk_overlap 个字符。
        # 这样可以让相邻 chunk 保留一点上下文连续性。
        start = end - chunk_overlap
        if start < 0:
            start = 0

        # 兜底保护：确保 start 一定会向前移动。
        if start == end:
            start += 1
    return chunks


def split_documents(documents: Iterable[DocumentItem], chunk_size: int = 220, chunk_overlap: int = 50) -> List[DocumentItem]:
    """把多篇文档批量切分成多个 DocumentItem 文本块。"""

    chunks: List[DocumentItem] = []
    for doc in documents:
        for idx, chunk in enumerate(split_text(doc.page_content, chunk_size, chunk_overlap)):
            # 复制原始文档 metadata，避免修改原文档对象。
            metadata = dict(doc.metadata)

            # chunk_index 用来记录这是某篇文档切出来的第几个文本块。
            metadata["chunk_index"] = idx
            chunks.append(DocumentItem(page_content=chunk, metadata=metadata))
    return chunks

