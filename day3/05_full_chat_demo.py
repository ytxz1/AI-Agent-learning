"""Day 3 - 综合小项目：API 对话助手。"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from modules.chat_client import ChatAPIClient
from modules.response_parser import extract_message_text, summarize_response


console = Console()


def main() -> None:
    client = ChatAPIClient()
    console.print(
        Panel.fit(
            "[bold]Day 3 - API 对话助手[/bold]\n"
            "输入问题后，程序会优先调用在线 Chat Completions；没有 key 或请求失败时会使用本地模拟响应。",
            style="bold green",
        )
    )
    console.print(f"[dim]API Key 状态：{'已配置' if client.api_available else '未配置，使用本地模拟'}[/dim]")

    while True:
        try:
            user_input = Prompt.ask("\n你")
        except (EOFError, KeyboardInterrupt):
            console.print("\n再见！", style="bold red")
            break

        if user_input.strip().lower() in {"q", "quit", "exit"}:
            console.print("再见！", style="bold red")
            break
        if not user_input.strip():
            continue

        response = client.chat(
            user_input,
            system_prompt="你是一个适合初学者的 API 调用老师，回答要清楚、简洁。",
        )
        console.print("\n[bold cyan]响应摘要：[/bold cyan]")
        console.print(summarize_response(response), style="yellow")
        console.print("\n[bold green]助手：[/bold green]")
        console.print(extract_message_text(response), style="green")


if __name__ == "__main__":
    main()

