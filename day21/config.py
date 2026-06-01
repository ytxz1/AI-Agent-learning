"""Day 21 配置文件。

Day 21 的主题是“项目优化与调试”。
这里不强制调用 API，而是用本地规则评估 Day 19 和 Day 20 项目：
- 提示词是否清晰
- 检索/回答链路是否可调试
- 用户体验是否友好
- 是否还有可以增加的功能
"""

from __future__ import annotations

from pathlib import Path
import os

from dotenv import load_dotenv


# 当前 day21 目录。
CURRENT_DIR = Path(__file__).parent
ENV_PATH = CURRENT_DIR / ".env"
EXAMPLE_ENV_PATH = CURRENT_DIR / ".env.example"

# 先读取真实 .env，再读取 .env.example 兜底。
load_dotenv(ENV_PATH)
if EXAMPLE_ENV_PATH.exists():
    load_dotenv(EXAMPLE_ENV_PATH, override=False)

# 要优化的目标项目。默认优化 Day 19 和 Day 20。
TARGET_PROJECTS = [
    item.strip()
    for item in os.getenv("TARGET_PROJECTS", "../day19,../day20").split(",")
    if item.strip()
]

# 报告输出目录。
REPORT_DIR = os.getenv("REPORT_DIR", "output")

# 读取文件预览时最多截取多少字符。
MAX_PREVIEW_CHARS = int(os.getenv("MAX_PREVIEW_CHARS", "500"))

# 项目评分达到多少算通过。
MIN_SCORE_PASS = int(os.getenv("MIN_SCORE_PASS", "70"))
