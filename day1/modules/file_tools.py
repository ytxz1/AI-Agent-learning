"""文件操作工具模块。

Day 1 需要掌握最基础的文件读写：
- 读取文本文件
- 写入文本文件
- 追加一行内容
- 统计文件信息
"""

from __future__ import annotations

from pathlib import Path


def read_text_file(path: str | Path) -> str:
    """读取文本文件。"""
    return Path(path).read_text(encoding="utf-8")


def write_text_file(path: str | Path, content: str) -> None:
    """写入文本文件，父目录不存在时自动创建。"""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def append_line(path: str | Path, line: str) -> None:
    """向文件末尾追加一行内容。"""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("a", encoding="utf-8") as file:
        file.write(line.rstrip("\n") + "\n")


def summarize_text_file(path: str | Path) -> dict:
    """统计文本文件的基础信息。"""
    text = read_text_file(path)
    lines = text.splitlines()
    words = [word for word in text.replace("\n", " ").split(" ") if word.strip()]
    return {
        "path": str(Path(path)),
        "char_count": len(text),
        "line_count": len(lines),
        "word_count": len(words),
    }

