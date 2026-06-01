"""Day 2 配置文件。

Day 2 是 Python 进阶练习，会用到 JSON 文件和输出报告。
把路径集中在这里，后面的代码更容易维护。
"""

from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
STUDENTS_JSON = DATA_DIR / "students.json"
OUTPUT_REPORT = OUTPUT_DIR / "students_report.json"
TEXT_REPORT = OUTPUT_DIR / "students_report.txt"

