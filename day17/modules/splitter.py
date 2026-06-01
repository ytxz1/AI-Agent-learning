"""文档切分模块。

负责把长文档切成更适合后续检索和分析的小块。
"""

from __future__ import annotations

from typing import Iterable, List

from langchain_core.documents import Document
from langchain_text_splitters import (
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


def split_recursive(
    documents: Iterable[Document],
    chunk_size: int = 300,
    chunk_overlap: int = 60,
    separators: list[str] | None = None,
) -> list[Document]:
    """使用递归切分器切文档。"""
    # RecursiveCharacterTextSplitter 会按 separators 的优先级尝试切分。
    # 它会优先按段落、换行、中文标点等更自然的位置切。
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators or ["\n\n", "\n", "。", "！", "？", "；", ";", " "],
    )

    # split_documents 会保留原文档 metadata，并生成新的 Document chunk。
    return splitter.split_documents(list(documents))


def split_character(
    documents: Iterable[Document],
    chunk_size: int = 300,
    chunk_overlap: int = 60,
) -> list[Document]:
    """使用最简单的字符切分器切文档。"""
    # CharacterTextSplitter 更简单，主要按指定 separator 切。
    # 它适合做基础对比，但通常不如递归切分器灵活。
    splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separator="\n",
    )
    return splitter.split_documents(list(documents))


def split_markdown_headers(document: Document) -> list[Document]:
    """按 Markdown 标题结构切分文档。"""
    # MarkdownHeaderTextSplitter 会根据 #、##、### 这样的标题结构切分。
    # 这种方式能更好保留 Markdown 的章节语义。
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "一级标题"),
            ("##", "二级标题"),
            ("###", "三级标题"),
        ]
    )
    chunks = splitter.split_text(document.page_content)

    # 补充原始文件信息，方便后续追踪来源。
    for chunk in chunks:
        chunk.metadata.update(document.metadata)
        chunk.metadata["splitter"] = "markdown_headers"
    return chunks


def split_by_type(documents: Iterable[Document], chunk_size: int = 300, chunk_overlap: int = 60) -> list[Document]:
    """根据文件类型选择不同切分方式。"""
    result: list[Document] = []
    for doc in documents:
        file_type = doc.metadata.get("file_type")

        # Markdown 文档优先按标题切分。
        if file_type == ".md":
            result.extend(split_markdown_headers(doc))
        else:
            # 普通 txt 文档使用递归切分器。
            result.extend(split_recursive([doc], chunk_size=chunk_size, chunk_overlap=chunk_overlap))
    return result


def compare_splitters(documents: Iterable[Document], chunk_size: int = 300, chunk_overlap: int = 60) -> dict[str, list[Document]]:
    """对比不同切分器的结果。"""
    # 先转 list，避免 Iterable 被某个切分器消耗后，后面切分器拿不到数据。
    docs = list(documents)
    return {
        "recursive": split_recursive(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap),
        "character": split_character(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap),
        "by_type": split_by_type(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap),
    }


def chunk_summary(chunks: Iterable[Document]) -> dict:
    """统计 chunk 数量和平均长度。"""
    chunk_list = list(chunks)
    if not chunk_list:
        return {"chunk_count": 0, "total_chars": 0, "avg_chars": 0}

    # total_chars 和 avg_chars 可以帮助判断切分是否过碎或过大。
    total_chars = sum(len(chunk.page_content) for chunk in chunk_list)
    return {
        "chunk_count": len(chunk_list),
        "total_chars": total_chars,
        "avg_chars": round(total_chars / len(chunk_list), 2),
    }


def preview_chunks(chunks: Iterable[Document], limit: int = 5, max_chars: int = 140) -> list[str]:
    """生成 chunk 的预览。"""
    previews: list[str] = []
    for index, chunk in enumerate(chunks):
        # 只展示前 limit 个 chunk。
        if index >= limit:
            break

        text = chunk.page_content.replace("\n", " ").strip()
        snippet = text[:max_chars] + ("..." if len(text) > max_chars else "")

        # 展示来源文件和切分器名称，方便比较不同策略。
        source = chunk.metadata.get("file_name", chunk.metadata.get("source", "unknown"))
        splitter_name = chunk.metadata.get("splitter", "recursive")
        previews.append(f"[{index + 1}] {source} | {splitter_name} | {snippet}")
    return previews
