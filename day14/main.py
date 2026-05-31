"""
Day 14 - 工具调用 Agent

运行方式：
    python main.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    exec(open(os.path.join(os.path.dirname(__file__), "05_chat_interface.py"), encoding="utf-8").read())

