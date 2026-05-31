"""Day 14 - 03 Function Calling 演示。

这个脚本演示三件事：
1. 告诉模型有哪些工具
2. 让模型决定要不要调用工具
3. 把工具执行结果再整理回自然语言

如果没有配置 `OPENAI_API_KEY`，脚本不会直接退出，而是切换到“本地模拟演示”模式，
这样你依然能看到完整的 Function Calling 流程。
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from config import MODEL_NAME, OPENAI_API_KEY, OPENAI_BASE_URL, TEMPERATURE
from modules.tools import calculator, get_current_time, get_weather, translate, unit_convert


def _print_header():
    """打印标题。"""
    print("=" * 60)
    print("Day 14 - Function Calling 演示")
    print("=" * 60)


def _run_online_demo():
    """有 API Key 时，运行真实的在线 Function Calling 演示。"""
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    )

    # 把工具交给模型，模型会决定是否调用它们。
    llm_with_tools = llm.bind_tools([calculator, get_weather, translate, get_current_time, unit_convert])
    prompt = "帮我计算 2 + 3 * 4，然后告诉我北京天气，最后把“你好”翻译成英文。"
    response = llm_with_tools.invoke([HumanMessage(content=prompt)])

    print("\n[在线模式] 原始模型输出：")
    print("content =", response.content)
    print("tool_calls =", response.tool_calls)


def _run_offline_demo():
    """没有 API Key 时，运行本地模拟演示。"""
    print("\n切换到本地模拟演示。")
    print("这个模式不会调用在线模型，但会完整展示“选择工具 -> 执行工具 -> 汇总结果”的流程。")

    prompt = "帮我计算 2 + 3 * 4，然后告诉我北京天气，最后把“你好”翻译成英文。"
    print("\n用户输入：")
    print(prompt)

    # 这里模拟“模型已经想好了要调用哪些工具”
    fake_tool_calls = [
        {
            "name": "calculator",
            "args": {"expression": "2 + 3 * 4"},
        },
        {
            "name": "get_weather",
            "args": {"city": "北京"},
        },
        {
            "name": "translate",
            "args": {"text": "你好", "target_language": "English"},
        },
    ]

    print("\n模拟模型决定调用的工具：")
    for index, call in enumerate(fake_tool_calls, 1):
        print(f"  {index}. {call['name']}({call['args']})")

    print("\n开始执行工具：")
    results = []
    for call in fake_tool_calls:
        if call["name"] == "calculator":
            result = calculator.invoke(call["args"])
        elif call["name"] == "get_weather":
            result = get_weather.invoke(call["args"])
        elif call["name"] == "translate":
            result = translate.invoke(call["args"])
        else:
            result = "未知工具"
        results.append((call["name"], result))
        print(f"  - {call['name']} -> {result}")

    final_answer = (
        f"计算结果是 {results[0][1]}，"
        f"北京天气是 {results[1][1]}，"
        f"“你好”翻译成英文是 {results[2][1]}。"
    )

    print("\n整理后的最终回答：")
    print(final_answer)


def main():
    """主函数。"""
    _print_header()

    if OPENAI_API_KEY:
        print("\n检测到 OPENAI_API_KEY，优先运行在线 Function Calling 演示。")
        try:
            _run_online_demo()
            return
        except Exception as exc:
            print("\n在线演示失败，自动切换到本地模拟模式。")
            print(f"失败原因：{exc}")
            _run_offline_demo()
    else:
        _run_offline_demo()


if __name__ == "__main__":
    main()
