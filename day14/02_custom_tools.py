"""Day 14 - 02 自定义工具与分发器演示

这个文件演示：
1. 如何拿到所有工具
2. 如何按名字调用工具
3. 如何把自然语言请求转成工具参数
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.tools import all_tools, tool_map


def dispatch_tool(tool_name: str, arguments: dict):
    tool = tool_map.get(tool_name)
    if not tool:
        return f"未找到工具：{tool_name}"
    return tool.invoke(arguments)


def main():
    print("=" * 60)
    print("Day 14 - 自定义工具演示")
    print("=" * 60)

    print("\n可用工具：")
    for item in all_tools:
        print(f"- {item.name}: {item.description.splitlines()[0]}")

    print("\n工具分发测试：")
    print(dispatch_tool("get_weather", {"city": "上海"}))
    print(dispatch_tool("calculator", {"expression": "sqrt(16) + 2"}))
    print(dispatch_tool("translate", {"text": "谢谢", "target_language": "English"}))


if __name__ == "__main__":
    main()

