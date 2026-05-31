"""Day 14 - 01 工具基础演示

运行：
    python 01_tool_basics.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.tools import calculator, get_current_time, get_weather, translate, unit_convert


def main():
    print("=" * 60)
    print("Day 14 - 工具基础演示")
    print("=" * 60)

    print("\n1) 计算器")
    print("2 + 3 * 4 =", calculator.invoke({"expression": "2 + 3 * 4"}))
    print("(10 - 2) / 4 =", calculator.invoke({"expression": "(10 - 2) / 4"}))

    print("\n2) 天气工具")
    print("北京天气：", get_weather.invoke({"city": "北京"}))

    print("\n3) 翻译工具")
    print('翻译 "你好" -> English：', translate.invoke({"text": "你好", "target_language": "English"}))

    print("\n4) 时间工具")
    print("当前时间：", get_current_time.invoke({"timezone_name": "local"}))

    print("\n5) 单位换算")
    print("25 摄氏度 =", unit_convert.invoke({"value": 25, "from_unit": "celsius", "to_unit": "fahrenheit"}))


if __name__ == "__main__":
    main()

