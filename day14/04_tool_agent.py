"""Day 14 - 04 工具调用 Agent 测试脚本

这个脚本适合用来快速检查 Agent 是否能工作。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.agent import ToolAgent


def main():
    agent = ToolAgent()

    print("=" * 60)
    print("Day 14 - Tool Agent 测试")
    print("=" * 60)
    print("状态：", agent.get_status())

    examples = [
        "你好，今天适合学习吗？",
        "帮我算一下 2 + 3 * 4",
        "北京今天天气怎么样？",
        "把 25 摄氏度换成华氏度",
        "把“谢谢”翻译成英文",
    ]

    for question in examples:
        print("\n用户：", question)
        answer = agent.auto_mode(question)
        print("助手：", answer)


if __name__ == "__main__":
    main()

