"""Day 3 - 练习 1：什么是 API。"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table


console = Console()

table = Table(title="API 基础概念", show_header=True)
table.add_column("概念", style="cyan")
table.add_column("解释", style="green")

table.add_row("API", "程序之间互相调用的接口")
table.add_row("Endpoint", "具体请求地址，例如 /chat/completions")
table.add_row("Method", "请求方法，例如 GET、POST")
table.add_row("Header", "请求头，通常放 Authorization 和 Content-Type")
table.add_row("Payload", "请求体，通常是 JSON")
table.add_row("Response", "响应结果，通常也是 JSON")

console.print(table)
console.print("\n一句话理解：API 就像餐厅点餐窗口，你按格式提交请求，对方按格式返回结果。", style="yellow")

