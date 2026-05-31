"""Day 17 文档处理流水线。

把“加载 -> 预览 -> 切分 -> 统计”串成一个完整流程。
"""

from __future__ import annotations

from pathlib import Path

from .loader import load_documents, preview_documents, resolve_docs_dir, summarize_documents
from .splitter import chunk_summary, compare_splitters, preview_chunks, split_by_type, split_recursive


class DocumentPipeline:
    """一个很轻量的文档处理管线。"""

    def __init__(self, base_dir: str | Path, docs_dir: str, chunk_size: int = 300, chunk_overlap: int = 60):
        self.base_dir = Path(base_dir)
        self.docs_dir_name = docs_dir
        self.docs_dir = resolve_docs_dir(self.base_dir, docs_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.documents = []
        self.chunks = []
        self.comparisons = {}

    def load(self):
        """加载所有文档。"""
        self.documents = load_documents(self.docs_dir)
        return self.documents

    def document_summary(self):
        """输出文档统计信息。"""
        return summarize_documents(self.documents)

    def document_previews(self, limit: int = 3, max_chars: int = 160):
        """预览文档内容。"""
        return preview_documents(self.documents, limit=limit, max_chars=max_chars)

    def split(self):
        """使用递归切分器进行切分。"""
        self.chunks = split_recursive(self.documents, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        return self.chunks

    def split_by_type(self):
        """按照文件类型选择切分方式。"""
        self.chunks = split_by_type(self.documents, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        return self.chunks

    def compare(self):
        """对比不同切分器的结果。"""
        self.comparisons = compare_splitters(
            self.documents,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        return self.comparisons

    def chunk_report(self):
        """返回当前 chunk 的统计结果。"""
        return chunk_summary(self.chunks)

    def chunk_previews(self, limit: int = 5, max_chars: int = 140):
        """预览 chunk。"""
        return preview_chunks(self.chunks, limit=limit, max_chars=max_chars)

