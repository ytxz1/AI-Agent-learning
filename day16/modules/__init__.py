"""modules 包统一导出。

这个文件让 day16/modules 变成一个 Python 包。
同时把常用类和函数集中导出，方便其他文件用更短的导入语句。
"""

from .embeddings import HybridEmbeddingModel, SimpleEmbeddingModel, get_embedding_model
from .loader import DocumentItem, load_documents
from .splitter import split_documents, split_text
from .vector_store import PersistentVectorStore, SearchResult
from .search_demo import SearchDemo
