"""Day 3 主入口：API 调用入门。"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from modules.chat_client import ChatAPIClient
from modules.response_parser import extract_message_text, summarize_response


console = Console()


def show_menu() -> None:
    table = Table(title="Day 3 功能菜单", show_header=True, header_style="bold magenta")
    table.add_column("命令", style="cyan", width=14)
    table.add_column("说明", style="white", width=50)
    table.add_row("chat", "发送一次 Chat Completions 请求")
    table.add_row("summary", "查看最近一次响应摘要")
    table.add_row("q", "退出")
    console.print(table)


def main() -> None:
    client = ChatAPIClient()
    last_response = None

    console.print(
        Panel.fit(
            "[bold]Day 3 - API 调用入门[/bold]\n什么是 API、如何发送请求、如何解析响应",
            style="bold green",
        )
    )
    console.print(f"[dim]当前模式：{'在线 API' if client.api_available else '本地模拟'}[/dim]")
    show_menu()

    while True:
        try:
            command = Prompt.ask("\n请输入命令").strip().lower()
        except (EOFError, KeyboardInterrupt):
            console.print("\n再见！", style="bold red")
            break

        if command == "q":
            console.print("再见！", style="bold red")
            break
        if command == "chat":
            question = Prompt.ask("请输入你的问题", default="什么是 API？")
            last_response = client.chat(
                question,
                system_prompt="你是一个耐心的 Python API 入门老师。",
            )
            console.print(extract_message_text(last_response), style="green")
        elif command == "summary":
            if last_response is None:
                console.print("还没有响应，请先执行 chat。", style="yellow")
            else:
                console.print(summarize_response(last_response), style="green")
        else:
            console.print("未知命令，请输入 chat / summary / q", style="yellow")


if __name__ == "__main__":
    main()

