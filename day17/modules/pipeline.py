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
        # base_dir 是 day17 根目录。
        self.base_dir = Path(base_dir)

        # docs_dir_name 保存原始配置名，方便调试。
        self.docs_dir_name = docs_dir

        # docs_dir 是解析后的绝对路径。
        self.docs_dir = resolve_docs_dir(self.base_dir, docs_dir)

        # 切分参数。
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # documents 保存加载后的原始文档。
        self.documents = []

        # chunks 保存切分后的文档块。
        self.chunks = []

        # comparisons 保存不同切分器的对比结果。
        self.comparisons = {}

    def load(self):
        """加载所有文档。"""
        self.documents = load_documents(self.docs_dir)
        return self.documents

    def document_summary(self):
        """输出文档统计信息。"""
        # 统计文档数量、类型分布、总字符数。
        return summarize_documents(self.documents)

    def document_previews(self, limit: int = 3, max_chars: int = 160):
        """预览文档内容。"""
        # 返回字符串列表，由调用方决定如何打印。
        return preview_documents(self.documents, limit=limit, max_chars=max_chars)

    def split(self):
        """使用递归切分器进行切分。"""
        # 默认切分方式：递归切分，比较适合普通文本。
        self.chunks = split_recursive(self.documents, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        return self.chunks

    def split_by_type(self):
        """按照文件类型选择切分方式。"""
        # Markdown 用标题切分，普通 txt 用递归切分。
        self.chunks = split_by_type(self.documents, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        return self.chunks

    def compare(self):
        """对比不同切分器的结果。"""
        # 同一批文档用多种策略切分，方便观察差异。
        self.comparisons = compare_splitters(
            self.documents,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        return self.comparisons

    def chunk_report(self):
        """返回当前 chunk 的统计结果。"""
        # 统计 chunk 数量、总字符数和平均长度。
        return chunk_summary(self.chunks)

    def chunk_previews(self, limit: int = 5, max_chars: int = 140):
        """预览 chunk。"""
        # 预览前几个 chunk，帮助判断切分是否合理。
        return preview_chunks(self.chunks, limit=limit, max_chars=max_chars)
