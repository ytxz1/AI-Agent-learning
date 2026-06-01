"""文档切分模块。

这一层负责把长文档切成更短的 chunk。
"""

from __future__ import annotations

import re
from typing import Iterable

from .loader import DocumentItem


def _normalize_text(text: str) -> str:
    """清理多余空白，方便切分。"""
    # 把三个及以上连续换行压缩成两个换行，保留段落感。
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _split_by_separator(text: str, chunk_size: int, chunk_overlap: int, separators: list[str]) -> list[str]:
    """递归切分长文本。"""
    text = _normalize_text(text)
    if len(text) <= chunk_size:
        return [text] if text else []

    # 依次尝试更自然的分隔符，例如段落、换行、中文句号。
    for separator in separators:
        if separator and separator in text:
            parts = text.split(separator)
            chunks: list[str] = []
            current = ""
            for part in parts:
                # 尝试把当前片段拼进当前 chunk。
                candidate = (current + separator + part).strip() if current else part.strip()
                if len(candidate) <= chunk_size:
                    current = candidate
                else:
                    if current:
                        # 如果当前 chunk 仍然太长，就换下一层分隔符继续递归切。
                        chunks.extend(_split_by_separator(current, chunk_size, chunk_overlap, separators[1:]))
                    current = part.strip()
            if current:
                chunks.extend(_split_by_separator(current, chunk_size, chunk_overlap, separators[1:]))
            return _merge_with_overlap(chunks, chunk_overlap)

    # 如果找不到合适分隔符，就直接滑窗切分
    return _sliding_window(text, chunk_size, chunk_overlap)


def _sliding_window(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """最基础的滑窗切分。"""
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        # 下一块从 end - overlap 开始，保留一点上下文。
        start = max(0, end - chunk_overlap)
    return chunks


def _merge_with_overlap(chunks: list[str], chunk_overlap: int) -> list[str]:
    """把过碎的 chunk 做一次轻微合并。"""
    if not chunks:
        return []
    merged: list[str] = []
    for chunk in chunks:
        if not merged:
            merged.append(chunk)
            continue
        # 太短的 chunk 单独存在意义不大，这里合并到上一块。
        if len(chunk) < max(40, chunk_overlap // 2):
            merged[-1] = (merged[-1] + "\n" + chunk).strip()
        else:
            merged.append(chunk)
    return merged


def split_documents(
    documents: Iterable[DocumentItem],
    chunk_size: int = 320,
    chunk_overlap: int = 70,
) -> list[DocumentItem]:
    """把多个文档切成 chunk。"""
    result: list[DocumentItem] = []
    separators = ["\n\n", "\n", "。", "！", "？", "；", ";", "，", " ", ""]

    for doc in documents:
        chunks = _split_by_separator(doc.page_content, chunk_size, chunk_overlap, separators)
        for index, chunk in enumerate(chunks):
            # 复制原文档 metadata，并追加 chunk 相关信息。
            metadata = dict(doc.metadata)
            metadata["chunk_index"] = index
            metadata["chunk_count"] = len(chunks)
            metadata["chunk_size"] = len(chunk)
            metadata["splitter"] = "recursive"
            result.append(DocumentItem(page_content=chunk, metadata=metadata))
    return result


def compare_chunk_stats(chunks: Iterable[DocumentItem]) -> dict:
    """统计 chunk 数量和平均长度。"""
    items = list(chunks)
    if not items:
        return {"chunk_count": 0, "total_chars": 0, "avg_chars": 0}
    # 平均长度可以帮助判断 chunk 是否过碎或过大。
    total_chars = sum(len(chunk.page_content) for chunk in items)
    return {
        "chunk_count": len(items),
        "total_chars": total_chars,
        "avg_chars": round(total_chars / len(items), 2),
    }


def preview_chunks(chunks: Iterable[DocumentItem], limit: int = 5, max_chars: int = 160) -> list[str]:
    """生成 chunk 预览。"""
    previews: list[str] = []
    for index, chunk in enumerate(chunks):
        if index >= limit:
            break
        # 压缩空白后截断显示。
        text = " ".join(chunk.page_content.split())
        snippet = text[:max_chars] + ("..." if len(text) > max_chars else "")
        previews.append(
            f"[{index + 1}] {chunk.metadata.get('file_name', 'unknown')} | chunk {chunk.metadata.get('chunk_index', 0)+1}/{chunk.metadata.get('chunk_count', 1)}: {snippet}"
        )
    return previews
