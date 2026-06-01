"""Day 20 程序入口。

运行：
python main.py

这个入口会启动 05_full_coding_agent.py 中的完整 Coding Agent 应用。
"""

from __future__ import annotations

import os
import sys

# 把 day20 根目录加入模块搜索路径。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # 复用完整应用文件，main.py 只作为统一入口。
    exec(open(os.path.join(os.path.dirname(__file__), "05_full_coding_agent.py"), encoding="utf-8").read())
