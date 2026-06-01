"""练习 1：把切块存入向量库。

练习目标：
理解“文档 -> 文本块 -> 向量库记录”的完整过程。

参考答案已经直接写在下面的代码里：
先加载 documents/ 里的文档，再切分成 chunk，最后调用 add_documents 存入向量库。
"""

import os
import sys

# 把当前 day16 目录加入 Python 搜索路径，避免直接运行时报模块找不到。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE, VECTOR_DB_FILE
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.splitter import split_documents
from modules.vector_store import PersistentVectorStore


if __name__ == "__main__":
    # 1. 找到 documents 文件夹。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")

    # 2. 加载本地文档，每份文档会被包装成 DocumentItem。
    documents = load_documents(docs_dir)

    # 3. 把长文档切成多个小文本块，方便后续检索。
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)

    # 4. 创建可持久化向量库。
    # get_embedding_model() 会优先使用在线 Embedding，没有 API 时使用本地兜底。
    store = PersistentVectorStore(get_embedding_model(), VECTOR_DB_FILE)

    # 5. 把文本块写入向量库。
    # 这里内部会自动把每个 chunk 转成向量，并和原文、metadata 一起保存。
    store.add_documents(chunks)

    print("文档数量：", len(documents))
    print("文本块数量：", len(chunks))
    print("向量库统计：", store.stats())
