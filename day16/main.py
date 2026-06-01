"""Day 16 - 向量数据库演示入口。

直接运行：
python main.py

这个入口提供一个命令行小工具，可以构建索引、搜索、查看统计、保存和加载向量库。
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# 让当前脚本无论从哪里运行，都能导入 day16 内部模块。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from config import CHUNK_OVERLAP, CHUNK_SIZE, TOP_K, VECTOR_DB_FILE
from modules.embeddings import get_embedding_model
from modules.loader import load_documents
from modules.search_demo import SearchDemo
from modules.splitter import split_documents
from modules.vector_store import PersistentVectorStore


console = Console()


class VectorDBApp:
    """Day 16 的命令行演示程序。"""

    def __init__(self):
        # documents 文件夹是知识库来源。
        self.docs_dir = Path(__file__).parent / "documents"

        # Embedding 模型：有 API 用在线，没有 API 用本地。
        self.embedding_model = get_embedding_model()

        # 可持久化向量库，保存路径来自 config.py。
        self.vector_store = PersistentVectorStore(self.embedding_model, VECTOR_DB_FILE)

        # SearchDemo 负责把检索结果格式化输出。
        self.search_demo = SearchDemo(self.vector_store, top_k=TOP_K)
        self.running = True

    def build_index(self):
        """重新构建索引。"""
        # 1. 加载文档。
        documents = load_documents(str(self.docs_dir))

        # 2. 切分文本。
        chunks = split_documents(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

        # 3. 清空旧记录，避免重复添加。
        self.vector_store.records = []

        # 4. 写入新文本块。
        self.vector_store.add_documents(chunks)

        return len(documents), len(chunks)

    def show_banner(self):
        """显示欢迎横幅。"""
        console.print(
            Panel.fit(
                "[bold]Day 16 - 向量数据库[/bold]\n"
                "命令：build / search / stats / save / load / demo / q\n"
                "示例：\n"
                "  search 什么是 RAG？\n"
                "  search 向量数据库有什么作用？\n"
                "  search:source=rag_notes.txt 什么是检索增强生成？",
                style="bold green",
            )
        )
        console.print(f"[dim]Embedding 模式：{getattr(self.embedding_model, 'mode', '未知')}[/dim]")

    def show_menu(self):
        """显示命令菜单。"""
        table = Table(title="命令菜单", show_header=True, header_style="bold magenta")
        table.add_column("命令", width=16)
        table.add_column("说明", width=60)
        table.add_row("build", "重新加载文档并构建向量索引")
        table.add_row("search", "执行一次语义搜索，例如：search 什么是 RAG？")
        table.add_row("stats", "查看向量库统计信息")
        table.add_row("save", "把向量库保存到磁盘")
        table.add_row("load", "从磁盘加载向量库")
        table.add_row("demo", "运行内置演示")
        table.add_row("q", "退出程序")
        console.print(table)

    def show_stats(self):
        """显示向量库统计信息。"""
        stats = self.vector_store.stats()
        console.print("\n[bold cyan]向量库统计[/bold cyan]")
        console.print(f"记录数量：{stats['record_count']}")
        console.print(f"保存路径：{stats['db_path']}")
        console.print(f"来源分布：{stats['source_counts']}")
        console.print(f"Embedding 模式：{getattr(self.embedding_model, 'mode', '未知')}")

    def run_demo(self):
        """运行几条示例问题。"""
        examples = [
            "什么是 RAG？",
            "向量数据库有什么作用？",
            "AI Agent 为什么要结合检索？",
        ]
        for question in examples:
            console.print(f"\n[bold cyan]问题：{question}[/bold cyan]")
            results = self.search_demo.search(question)
            console.print(self.search_demo.format_results(results))

    def parse_search_command(self, command: str):
        """解析 search 命令中的简单过滤条件。"""
        metadata_filter = None
        question = command

        if command.startswith("search:"):
            # 支持这种写法：
            # search:source=rag_notes.txt 什么是 RAG？
            prefix, rest = command.split(" ", 1) if " " in command else (command, "")
            filter_part = prefix[len("search:"):]
            if "=" in filter_part:
                key, value = filter_part.split("=", 1)
                metadata_filter = {key.strip(): value.strip()}
            question = rest.strip()
        else:
            question = command[len("search"):].strip()

        return question, metadata_filter

    def run(self):
        """主循环。"""
        self.show_banner()
        self.show_menu()

        self.vector_store.load()
        if not self.vector_store.records:
            # 如果磁盘上没有保存过向量库，就自动构建一次索引。
            count_docs, count_chunks = self.build_index()
            console.print(f"[dim]已自动构建索引：{count_docs} 份文档，{count_chunks} 个文本块[/dim]")

        while self.running:
            try:
                user_input = Prompt.ask("\n请输入命令或问题")
            except (EOFError, KeyboardInterrupt):
                console.print("\n再见！", style="bold red")
                break

            if not user_input:
                continue

            command = user_input.strip().lower()

            if command == "q":
                console.print("再见！", style="bold red")
                break
            if command == "build":
                count_docs, count_chunks = self.build_index()
                console.print(f"索引已重建：{count_docs} 份文档，{count_chunks} 个文本块")
                continue
            if command == "stats":
                self.show_stats()
                continue
            if command == "save":
                self.vector_store.save()
                console.print("向量库已保存到磁盘。")
                continue
            if command == "load":
                self.vector_store.load()
                console.print("向量库已从磁盘加载。")
                continue
            if command == "demo":
                self.run_demo()
                continue

            if command.startswith("search"):
                question, metadata_filter = self.parse_search_command(user_input)
                if not question:
                    console.print("请输入搜索问题，例如：search 什么是 RAG？", style="yellow")
                    continue

                # 执行语义搜索，并打印格式化结果。
                results = self.search_demo.search(question, metadata_filter=metadata_filter)
                console.print(self.search_demo.format_results(results))
                continue

            console.print("无法识别的命令。请输入 build / search / stats / save / load / demo / q", style="yellow")


if __name__ == "__main__":
    VectorDBApp().run()
