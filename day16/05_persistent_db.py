"""练习 5：持久化向量库。

练习目标：
理解“保存到磁盘”和“重新加载”的意义。

参考答案：
调用 store.save() 把向量库保存成 JSON 文件；
再新建一个 PersistentVectorStore，调用 load() 读取回来。
"""

import os
import sys

# 让脚本可以直接导入 day16 内部模块。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE, VECTOR_DB_FILE
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.splitter import split_documents
from modules.vector_store import PersistentVectorStore


if __name__ == "__main__":
    # 1. 构建一个新的向量库。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    store = PersistentVectorStore(get_embedding_model(), VECTOR_DB_FILE)
    store.add_documents(chunks)

    # 2. 保存到 config.py 里配置的 VECTOR_DB_FILE。
    store.save()

    # 3. 重新创建一个空向量库对象，模拟“程序重启后重新加载”。
    reload_store = PersistentVectorStore(get_embedding_model(), VECTOR_DB_FILE)

    # 4. 从磁盘读取刚才保存的数据。
    reload_store.load()

    print("重新加载后的统计：", reload_store.stats())
