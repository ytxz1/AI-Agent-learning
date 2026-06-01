"""JSON 文件工具。

Day 2 会用到 json、os/pathlib、异常处理。
这里把 JSON 读写单独封装，方便其他脚本调用。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    """读取 JSON 文件。"""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")

    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON 格式错误：{exc}") from exc


def save_json(path: str | Path, data: Any) -> None:
    """保存 JSON 文件。"""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def safe_load_json(path: str | Path, default: Any = None) -> Any:
    """安全读取 JSON，失败时返回默认值。"""
    try:
        return load_json(path)
    except (FileNotFoundError, ValueError):
        return default

