"""Day 17 - 练习 2：切分器对比。

练习目标：
对比 recursive、character、by_type 三种切分策略的 chunk 数量和平均长度。

参考答案：
使用 pipeline.compare() 同时运行多种切分器，再用表格展示每种策略的结果。
"""

from __future__ import annotations

import os
import sys

# 保证当前脚本可以导入 day17 内部模块。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.table import Table

from config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR
from modules.pipeline import DocumentPipeline

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 17 - 练习 2：切分器对比", style="bold blue")
console.print("=" * 60, style="bold blue")

# 创建管线时传入 chunk_size 和 chunk_overlap，方便切分器统一使用同一组参数。
pipeline = DocumentPipeline(base_dir=os.path.dirname(os.path.abspath(__file__)), docs_dir=DOCS_DIR, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

# 先加载文档，再比较切分器。
pipeline.load()
comparisons = pipeline.compare()

# 用表格展示结果，比直接 print 字典更清楚。
table = Table(title="切分器对比", show_header=True)
table.add_column("策略", style="cyan", width=16)
table.add_column("chunk 数量", style="yellow", width=12)
table.add_column("平均长度", style="green", width=12)

for name, chunks in comparisons.items():
    # 计算每种切分策略的平均 chunk 长度。
    total_chars = sum(len(chunk.page_content) for chunk in chunks)
    avg_chars = round(total_chars / len(chunks), 2) if chunks else 0
    table.add_row(name, str(len(chunks)), str(avg_chars))

console.print(table)
