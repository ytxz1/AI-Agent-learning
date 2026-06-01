"""练习 2：相似度搜索。

练习目标：
理解用户问题如何被转换成向量，并与向量库里的文档块计算相似度。

参考答案：
构建向量库后，调用 SearchDemo.search(question) 即可返回 Top-K 相关结果。
"""

import os
import sys

# 让脚本可以直接导入 config 和 modules。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHUNK_OVERLAP, CHUNK_SIZE, TOP_K, VECTOR_DB_FILE
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.search_demo import SearchDemo
from modules.splitter import split_documents
from modules.vector_store import PersistentVectorStore


if __name__ == "__main__":
    # 1. 加载 documents/ 下的示例文档。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    documents = load_documents(docs_dir)

    # 2. 切分文档，得到适合检索的小文本块。
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)

    # 3. 构建向量库并写入文本块。
    store = PersistentVectorStore(get_embedding_model(), VECTOR_DB_FILE)
    store.add_documents(chunks)

    # 4. SearchDemo 负责把检索结果格式化成更容易看的文本。
    demo = SearchDemo(store, TOP_K)

    # 5. 用一个固定问题测试语义搜索效果。
    question = "什么是向量数据库？"
    results = demo.search(question)

    print(demo.format_results(results))
