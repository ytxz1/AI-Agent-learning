"""Day 2 - 练习 4：常用库 requests、json、os/pathlib、typing。"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from rich.console import Console

from modules.api_tools import fetch_python_repo_info


console = Console()


def show_env_info() -> dict[str, Any]:
    """展示一小部分环境信息。"""
    return {
        "cwd": os.getcwd(),
        "home": str(Path.home()),
        "python_path_exists": Path("main.py").exists(),
    }


console.print("=" * 60, style="bold blue")
console.print("常用库演示", style="bold blue")
console.print("=" * 60, style="bold blue")

console.print("\n[bold cyan]os/pathlib 信息：[/bold cyan]")
console.print(show_env_info(), style="green")

console.print("\n[bold cyan]requests 示例：[/bold cyan]")
console.print(fetch_python_repo_info(), style="yellow")

