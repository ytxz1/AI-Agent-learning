"""Day 17 - 练习 1：文档加载基础。

练习目标：
先确认 documents/ 里的文件可以被正确读取成 Document 对象。

参考答案：
使用 DocumentPipeline.load() 加载文档，再调用 document_summary() 和 document_previews()
查看文档数量、总字符数、文件类型和内容预览。
"""

from __future__ import annotations

import os
import sys

# 把当前 day17 目录加入模块搜索路径，避免直接运行时报导入错误。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console

from config import DOCS_DIR
from modules.pipeline import DocumentPipeline

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 17 - 练习 1：文档加载基础", style="bold blue")
console.print("=" * 60, style="bold blue")

# 创建文档处理管线。
# base_dir 表示 day17 根目录，docs_dir 表示文档目录名。
pipeline = DocumentPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR)

# 加载 documents/ 下的 .txt 和 .md 文件。
pipeline.load()

# 统计加载结果，确认文档真的进入程序。
summary = pipeline.document_summary()
console.print(f"文档数量：{summary['document_count']}", style="green")
console.print(f"总字符数：{summary['total_chars']}", style="green")
console.print(f"文件类型：{summary['file_types']}", style="green")

console.print("\n[bold cyan]文档预览：[/bold cyan]")

# 打印前几份文档的预览内容，避免整篇文档刷屏。
for line in pipeline.document_previews():
    console.print(line, style="yellow")
