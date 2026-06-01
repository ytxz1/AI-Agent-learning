"""Day 3 - 练习 4：解析响应。"""

from __future__ import annotations

from rich.console import Console

from modules.mock_api import mock_chat_completion
from modules.response_parser import extract_message_text, summarize_response


console = Console()

mock_response = mock_chat_completion(
    [{"role": "user", "content": "帮我解释 choices 字段是什么"}],
    model="mock-chat",
)

console.print("=" * 60, style="bold blue")
console.print("响应解析演示", style="bold blue")
console.print("=" * 60, style="bold blue")

console.print("[bold cyan]完整响应摘要：[/bold cyan]")
console.print(summarize_response(mock_response), style="yellow")

console.print("\n[bold cyan]提取出来的文本：[/bold cyan]")
console.print(extract_message_text(mock_response), style="green")

