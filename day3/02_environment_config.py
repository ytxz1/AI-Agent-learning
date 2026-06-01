"""Day 3 - 练习 2：环境变量和配置。"""

from __future__ import annotations

from rich.console import Console

from config import CHAT_COMPLETIONS_URL, OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, TIMEOUT_SECONDS


console = Console()

console.print("=" * 60, style="bold blue")
console.print("环境变量和配置演示", style="bold blue")
console.print("=" * 60, style="bold blue")

console.print(f"Base URL：{OPENAI_BASE_URL}", style="green")
console.print(f"Chat Completions URL：{CHAT_COMPLETIONS_URL}", style="green")
console.print(f"模型名：{OPENAI_MODEL}", style="green")
console.print(f"超时时间：{TIMEOUT_SECONDS} 秒", style="green")
console.print(f"是否检测到 API Key：{bool(OPENAI_API_KEY)}", style="yellow")

console.print("\n真实项目里不要把 API Key 写进代码，要放在 .env 里。", style="cyan")

