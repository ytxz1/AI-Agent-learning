"""Day 18 - 完整演示：RAG 检索链。"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from config import ANSWER_STYLE, CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR, MAX_CONTEXT_CHARS, TOP_K
from modules.pipeline import RAGPipeline

console = Console()


class RAGApp:
    """命令行版 RAG 检索链应用。"""

    def __init__(self):
        self.pipeline = RAGPipeline(
            base_dir=os.path.dirname(os.path.abspath(__file__)),
            docs_dir=DOCS_DIR,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            top_k=TOP_K,
            max_context_chars=MAX_CONTEXT_CHARS,
        )
        self.loaded = False

    def show_welcome(self):
        console.print(
            Panel.fit(
                "[bold]Day 18 - RAG 检索链[/bold]\n"
                "本日重点：检索器、Top-K、上下文拼接、检索结果组织。",
                style="bold green",
            )
        )

    def show_menu(self):
        console.print("\n可用命令：")
        console.print("  load    - 加载并切分文档")
        console.print("  docs    - 查看文档预览")
        console.print("  chunks  - 查看 chunk 预览")
        console.print("  stats   - 查看统计信息")
        console.print("  ask     - 提问一次")
        console.print("  demo    - 运行示例问题")
        console.print("  q       - 退出")

    def load(self):
        self.pipeline.load()
        self.pipeline.split()
        self.loaded = True
        console.print("文档加载与切分完成。", style="green")

    def show_docs(self):
        if not self.loaded:
            self.load()
        summary = self.pipeline.document_summary()
        console.print(f"\n文档总数：{summary['document_count']}", style="green")
        console.print(f"总字符数：{summary['total_chars']}", style="green")
        console.print(f"文件类型：{summary['file_types']}", style="green")
        console.print("\n[bold cyan]文档预览：[/bold cyan]")
        for line in self.pipeline.document_previews():
            console.print(line, style="yellow")

    def show_chunks(self):
        if not self.loaded:
            self.load()
        summary = self.pipeline.chunk_summary()
        console.print(f"\nchunk 数量：{summary['chunk_count']}", style="green")
        console.print(f"平均长度：{summary['avg_chars']}", style="green")
        console.print("\n[bold cyan]chunk 预览：[/bold cyan]")
        for line in self.pipeline.chunk_previews():
            console.print(line, style="yellow")

    def show_stats(self):
        if not self.loaded:
            self.load()
        console.print("\n[bold cyan]系统状态：[/bold cyan]")
        console.print(f"  文档数量：{self.pipeline.document_summary()['document_count']}", style="green")
        console.print(f"  chunk 数量：{self.pipeline.chunk_summary()['chunk_count']}", style="green")
        console.print(f"  top_k：{TOP_K}", style="green")
        console.print(f"  max_context_chars：{MAX_CONTEXT_CHARS}", style="green")
        api_status = "可用" if self.pipeline.chain and self.pipeline.chain.llm is not None else "不可用"
        console.print(f"  在线模型：{api_status}", style="green")

    def ask_once(self):
        if not self.loaded:
            self.load()
        question = Prompt.ask("\n请输入你的问题")
        result = self.pipeline.ask(question)
        console.print("\n[bold cyan]检索结果摘要：[/bold cyan]")
        console.print(result["retrieval_summary"], style="yellow")
        console.print("\n[bold cyan]拼接上下文：[/bold cyan]")
        console.print(result["context"], style="green")
        console.print("\n[bold cyan]最终回答：[/bold cyan]")
        console.print(result["answer"], style="magenta")
        console.print(f"\n[dim]回答模式：{'API 在线生成' if result.get('api_enabled') else '本地兜底'}[/dim]")

    def demo(self):
        if not self.loaded:
            self.load()
        demo_questions = [
            "什么是 RAG？",
            "Retriever 的核心作用是什么？",
            "为什么上下文拼接会影响答案质量？",
        ]
        for question in demo_questions:
            console.print(f"\n[bold cyan]问题：{question}[/bold cyan]")
            result = self.pipeline.ask(question)
            console.print(result["answer"], style="magenta")

    def run(self):
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
            elif cmd == "docs":
                self.show_docs()
            elif cmd == "chunks":
                self.show_chunks()
            elif cmd == "stats":
                self.show_stats()
            elif cmd == "ask":
                self.ask_once()
            elif cmd == "demo":
                self.demo()
            else:
                console.print("未知命令，请重新输入。", style="red")


def main():
    app = RAGApp()
    app.run()


if __name__ == "__main__":
    main()
