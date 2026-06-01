"""Day 17 程序入口。

运行：
python main.py

这个入口会启动 05_full_pipeline.py 中的完整交互应用。
"""

from __future__ import annotations

import os
import sys

# 把 day17 根目录加入模块搜索路径。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # 复用 05_full_pipeline.py 的完整交互逻辑。
    # 这里使用 exec 是为了保持 main.py 很薄，只作为统一入口。
    exec(open(os.path.join(os.path.dirname(__file__), "05_full_pipeline.py"), encoding="utf-8").read())
