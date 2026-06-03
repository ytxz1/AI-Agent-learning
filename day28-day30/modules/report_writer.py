"""Day28-Day30 报告写入工具。"""

from __future__ import annotations

import json
import sys
from pathlib import Path


DAY_DIR = Path(__file__).resolve().parents[1]
if str(DAY_DIR) not in sys.path:
    sys.path.insert(0, str(DAY_DIR))

from config import OUTPUT_DIR


def write_markdown(file_name: str, content: str) -> Path:
    """写入 Markdown 文件。"""

    path = OUTPUT_DIR / file_name
    path.write_text(content, encoding="utf-8")
    return path


def write_json(file_name: str, data: object) -> Path:
    """写入 JSON 文件。"""

    path = OUTPUT_DIR / file_name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    # 练习题答案 7：
    # 如何写入一份跟进记录？
    # 如何添加：调用 write_markdown()。
    path = write_markdown("demo_follow_up.md", "# 练习题答案 7\n\n跟进记录写入成功。")
    print("练习题答案 7：文件已写入", path)
