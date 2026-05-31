"""Day 13 程序入口。

这个文件只负责启动交互界面，不放业务逻辑。
真正的聊天、工具调用、输出解析和模式切换逻辑，都在 `06_chat_interface.py` 里。
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    exec(open(os.path.join(os.path.dirname(__file__), "06_chat_interface.py"), encoding="utf-8").read())
