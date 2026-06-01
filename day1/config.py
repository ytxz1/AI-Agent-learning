"""Day 1 配置文件。

Day 1 是 Python 基础，所以配置很少。
这里把数据目录、输出目录和示例文件路径统一放在一起，
后面的脚本就不用到处写死路径。
"""

from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
SAMPLE_NOTES_FILE = DATA_DIR / "sample_notes.txt"
OUTPUT_REPORT_FILE = OUTPUT_DIR / "day1_report.txt"

