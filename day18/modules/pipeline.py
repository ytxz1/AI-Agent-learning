"""Day 18 文档处理管线。"""

from __future__ import annotations

from pathlib import Path

from .loader import load_documents, preview_documents, resolve_docs_dir, summarize_documents
from .rag_chain import RAGChain
from .splitter import compare_chunk_stats, preview_chunks, split_documents


class RAGPipeline:
    """把文档加载、切分、检索链组装在一起。"""

    def __init__(self, base_dir: str | Path, docs_dir: str, chunk_size: int = 320, chunk_overlap: int = 70, top_k: int = 3, max_context_chars: int = 1600):
        self.base_dir = Path(base_dir)
        self.docs_dir_name = docs_dir
        self.docs_dir = resolve_docs_dir(self.base_dir, docs_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.max_context_chars = max_context_chars
        self.documents = []
        self.chunks = []
        self.chain: RAGChain | None = None

    def load(self):
        """加载原始文档。"""
        self.documents = load_documents(self.docs_dir)
        return self.documents

    def split(self):
        """切分文档。"""
        if not self.documents:
            self.load()
        self.chunks = split_documents(self.documents, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        self.chain = RAGChain(self.chunks, top_k=self.top_k, max_context_chars=self.max_context_chars)
        return self.chunks

    def ensure_ready(self):
        """确保管线已准备好。"""
        if not self.documents:
            self.load()
        if not self.chunks:
            self.split()
        if self.chain is None:
            self.chain = RAGChain(self.chunks, top_k=self.top_k, max_context_chars=self.max_context_chars)

    def document_summary(self):
        return summarize_documents(self.documents)

    def document_previews(self, limit: int = 3, max_chars: int = 180):
        return preview_documents(self.documents, limit=limit, max_chars=max_chars)

    def chunk_summary(self):
        return compare_chunk_stats(self.chunks)

    def chunk_previews(self, limit: int = 5, max_chars: int = 160):
        return preview_chunks(self.chunks, limit=limit, max_chars=max_chars)

    def ask(self, question: str) -> dict:
        """对外统一查询入口。"""
        self.ensure_ready()
        assert self.chain is not None
        return self.chain.query(question)

