"""Day 3 - 练习 3：发送 Chat Completions 请求。"""

from __future__ import annotations

from rich.console import Console

from modules.chat_client import ChatAPIClient
from modules.response_parser import extract_message_text, summarize_response


console = Console()
client = ChatAPIClient()

response = client.chat(
    "请用三句话解释什么是 API。",
    system_prompt="你是一个耐心的 Python 和 API 入门老师。",
)

console.print("=" * 60, style="bold blue")
console.print("Chat Completions 响应摘要", style="bold blue")
console.print("=" * 60, style="bold blue")
console.print(summarize_response(response), style="yellow")

console.print("\n[bold cyan]助手回复：[/bold cyan]")
console.print(extract_message_text(response), style="green")

