"""Day 17 - 完整演示：文档加载与切分管线。

这个文件是 Day 17 的完整交互应用。
你可以通过命令体验：加载文档、预览文档、切分文档、对比切分器和查看 chunk。
"""

from __future__ import annotations

import os
import sys

# 让当前脚本可以直接导入 day17 内部模块。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR, MAX_PREVIEW_CHARS, PREVIEW_LIMIT
from modules.pipeline import DocumentPipeline

console = Console()


class DocumentApp:
    """一个命令行版文档加载与切分小应用。"""

    def __init__(self):
        # DocumentPipeline 是真正负责加载和切分的核心对象。
        self.pipeline = DocumentPipeline(
            base_dir=os.path.dirname(os.path.abspath(__file__)),
            docs_dir=DOCS_DIR,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

        # loaded 用来记录是否已经加载过文档，避免重复加载。
        self.loaded = False

    def show_welcome(self):
        """显示欢迎信息。"""
        console.print(
            Panel.fit(
                "[bold]Day 17 - 文档加载与切分[/bold]\n"
                "本日重点：把文件读进来，再把长文档切成适合后续处理的小块。",
                style="bold green",
            )
        )

    def show_menu(self):
        """显示可用命令。"""
        console.print("\n可用命令：")
        console.print("  load    - 加载文档")
        console.print("  preview - 预览文档内容")
        console.print("  split   - 使用递归切分器切分")
        console.print("  compare - 对比不同切分策略")
        console.print("  stats   - 查看统计信息")
        console.print("  chunks  - 预览切分结果")
        console.print("  q       - 退出")

    def load(self):
        """加载 documents/ 目录下的文档。"""
        docs = self.pipeline.load()
        self.loaded = True
        console.print(f"已加载 {len(docs)} 份文档。", style="green")

    def preview(self):
        """预览文档统计信息和前几份文档内容。"""
        if not self.loaded:
            self.load()
        summary = self.pipeline.document_summary()
        console.print(f"\n文档总数：{summary['document_count']}", style="green")
        console.print(f"总字符数：{summary['total_chars']}", style="green")
        console.print(f"文件类型：{summary['file_types']}", style="green")
        console.print("\n[bold cyan]文档预览：[/bold cyan]")
        for line in self.pipeline.document_previews(limit=PREVIEW_LIMIT, max_chars=MAX_PREVIEW_CHARS):
            console.print(line, style="yellow")

    def split(self):
        """使用递归切分器切分文档。"""
        if not self.loaded:
            self.load()
        chunks = self.pipeline.split()
        report = self.pipeline.chunk_report()
        console.print(f"切分完成：{report['chunk_count']} 个 chunk", style="green")
        console.print(f"平均长度：{report['avg_chars']} 字符", style="green")

    def compare(self):
        """对比多种切分策略。"""
        if not self.loaded:
            self.load()
        comparisons = self.pipeline.compare()
        console.print("\n[bold cyan]切分策略对比：[/bold cyan]")
        for name, chunks in comparisons.items():
            total_chars = sum(len(chunk.page_content) for chunk in chunks)
            avg_chars = round(total_chars / len(chunks), 2) if chunks else 0
            console.print(f"  - {name}: chunk 数量 = {len(chunks)}，平均长度 = {avg_chars}", style="yellow")

    def show_chunks(self):
        """预览已经切分好的 chunk。"""
        if not self.pipeline.chunks:
            console.print("请先执行 split。", style="red")
            return
        console.print("\n[bold cyan]chunk 预览：[/bold cyan]")
        for line in self.pipeline.chunk_previews():
            console.print(line, style="yellow")

    def run(self):
        """运行命令行主循环。"""
        self.show_welcome()
        self.show_menu()
        while True:
            try:
                cmd = Prompt.ask("\n请输入命令").strip().lower()
            except (EOFError, KeyboardInterrupt):
                console.print("\n再见！", style="bold red")
                break
            if cmd == "q":
                console.print("再见！", style="bold red")
                break
            if cmd == "load":
                self.load()
            elif cmd == "preview":
                self.preview()
            elif cmd == "split":
                self.split()
            elif cmd == "compare":
                self.compare()
            elif cmd == "stats":
                if not self.loaded:
                    self.load()
                console.print(self.pipeline.document_summary(), style="green")
            elif cmd == "chunks":
                self.show_chunks()
            else:
                console.print("未知命令，请重新输入。", style="red")


def main():
    """程序入口函数。"""
    app = DocumentApp()
    app.run()


if __name__ == "__main__":
    main()
