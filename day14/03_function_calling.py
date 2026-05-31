"""Day 14 - 03 Function Calling 演示

重点：
1. 告诉模型有哪些工具
2. 让模型决定是否要调用工具
3. 让程序执行工具并回传结果
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from config import MODEL_NAME, OPENAI_API_KEY, OPENAI_BASE_URL, TEMPERATURE
from modules.tools import all_tools


def main():
    print("=" * 60)
    print("Day 14 - Function Calling 演示")
    print("=" * 60)

    if not OPENAI_API_KEY:
        print("\n未检测到 OPENAI_API_KEY，跳过在线 Function Calling 演示。")
        print("你可以先补上 .env 再运行这个文件。")
        return

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    )

    llm_with_tools = llm.bind_tools(all_tools)
    prompt = "帮我计算 2 + 3 * 4，然后告诉我北京天气。"
    response = llm_with_tools.invoke([HumanMessage(content=prompt)])

    print("\n原始模型输出：")
    print("content =", response.content)
    print("tool_calls =", response.tool_calls)


if __name__ == "__main__":
    main()

