"""Day 2 - 练习 3：异常处理。"""

from __future__ import annotations

from rich.console import Console

from modules.json_tools import load_json, safe_load_json


console = Console()

console.print("=" * 60, style="bold blue")
console.print("异常处理演示", style="bold blue")
console.print("=" * 60, style="bold blue")

missing_file = "data/not_exists.json"

try:
    load_json(missing_file)
except FileNotFoundError as exc:
    console.print(f"捕获到文件不存在错误：{exc}", style="yellow")
except ValueError as exc:
    console.print(f"捕获到 JSON 格式错误：{exc}", style="red")
finally:
    console.print("finally：不管是否出错，这里都会执行。", style="green")

fallback = safe_load_json(missing_file, default=[])
console.print(f"\nsafe_load_json 返回默认值：{fallback}", style="cyan")

