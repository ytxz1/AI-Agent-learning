"""Day 15 - 01 文档加载演示。

这个脚本对应 RAG 流程的第一步：读取知识库文档。
运行后可以看到 documents/ 目录下加载到了哪些文件。
"""

import os
import sys

# 把当前 day15 目录加入模块搜索路径。
# 这样无论你从 VS Code 直接运行，还是在终端运行，都能正确导入 modules。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.loader import load_documents


def main():
    # 拼出 documents 文件夹的绝对路径。
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")

    # 调用封装好的文档加载函数。
    documents = load_documents(docs_dir)

    print("=" * 60)
    print("文档加载演示")
    print("=" * 60)
    print(f"加载到 {len(documents)} 份文档")

    # 打印每份文档的文件名和前 80 个字符，方便快速确认加载是否成功。
    for doc in documents:
        print(f"- {doc.metadata['source']}: {doc.page_content[:80]}...")


if __name__ == "__main__":
    main()

