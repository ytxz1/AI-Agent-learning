"""
Day 10 - Tools 综合实践：智能工具助手

整合所有工具知识，构建一个支持多种工具的交互式助手。
功能：
1. 自动选择合适的工具
2. 支持多种工具切换
3. 显示工具调用过程
4. 支持连续对话

运行方式：
    python main.py
"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
import os
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=MODEL_NAME,
    temperature=0.7,
)

console = Console()

# ==============================
# 定义工具
# ==============================

@tool
def calculator(expression: str) -> str:
    """执行数学计算。当需要计算数学表达式时使用此工具。
    参数:
        expression: 数学表达式，如 "2 + 3 * 4"、"sqrt(144)"
    """
    try:
        import math
        safe_dict = {"abs": abs, "round": round, "min": min, "max": max,
                     "sqrt": math.sqrt, "pow": pow, "pi": math.pi}
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return str(int(result)) if isinstance(result, float) and result == int(result) else str(result)
    except Exception as e:
        return f"计算错误：{e}"

@tool
def get_weather(city: str) -> str:
    """获取城市天气信息。当用户问天气时使用此工具。
    参数:
        city: 城市名称，如 "北京"、"上海"
    """
    weather = {
        "北京": "25°C，晴天，微风",
        "上海": "28°C，多云，东南风3级",
        "广州": "32°C，雷阵雨，湿度85%",
        "深圳": "30°C，小雨，阵风5级",
        "杭州": "26°C，阴天，西风2级",
        "成都": "24°C，多云转晴",
    }
    return weather.get(city, f"未找到 {city} 的天气，目前支持：{', '.join(weather.keys())}")

@tool
def translate_text(text: str, target_language: str) -> str:
    """翻译文本。当用户需要翻译时使用此工具。
    参数:
        text: 待翻译的文本
        target_language: 目标语言，如 "英文"、"中文"
    """
    translations = {
        ("你好", "英文"): "Hello", ("谢谢", "英文"): "Thank you",
        ("再见", "英文"): "Goodbye", ("hello", "中文"): "你好",
        ("thank you", "中文"): "谢谢", ("goodbye", "中文"): "再见",
    }
    key = (text.strip().lower(), target_language)
    return translations.get(key, f"暂时无法翻译「{text}」为{target_language}")

@tool
def search_knowledge(query: str) -> str:
    """搜索知识库获取信息。当用户问知识性问题时使用此工具。
    参数:
        query: 搜索关键词
    """
    knowledge = {
        "python": "Python 是一种高级编程语言，以简洁易读著称，广泛应用于 Web 开发、数据科学、AI 等领域。",
        "机器学习": "机器学习是 AI 的分支，使计算机从数据中学习。分为监督学习、无监督学习、强化学习。",
        "langchain": "LangChain 是构建 LLM 应用的开源框架，提供 Prompt、Chain、Agent、Memory 等组件。",
        "transformer": "Transformer 是 2017 年 Google 提出的神经网络架构，是 GPT、BERT 等模型的基础。",
        "agent": "AI Agent 是能自主决策和执行任务的智能体，结合 LLM、工具调用和记忆系统。",
    }
    for key, value in knowledge.items():
        if key in query.lower():
            return f"【{key}】{value}"
    return f"未找到与「{query}」相关的信息"

tools = [calculator, get_weather, translate_text, search_knowledge]

# ==============================
# 工具调用循环
# ==============================

def chat(user_input: str, max_rounds: int = 5):
    """与 AI 对话，自动调用工具"""
    llm_with_tools = llm.bind_tools(tools)
    messages = [HumanMessage(content=user_input)]

    for _ in range(max_rounds):
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            for tc in response.tool_calls:
                tool_func = next((t for t in tools if t.name == tc["name"]), None)
                if tool_func:
                    result = tool_func.invoke(tc["args"])
                    console.print(f"  [工具] {tc['name']}({tc['args']}) -> {result}", style="yellow")
                    messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
        else:
            return response.content

    return "达到最大调用轮数"

# ==============================
# 菜单
# ==============================

def show_menu():
    table = Table(title="Day 10 智能工具助手", show_header=True)
    table.add_column("功能", style="green", width=14)
    table.add_column("说明", style="white")

    table.add_row("直接输入", "和 AI 聊天，自动调用工具")
    table.add_row("tools", "查看所有可用工具")
    table.add_row("q", "退出程序")

    console.print(table)

# ==============================
# 主程序
# ==============================

def main():
    console.print(
        Panel.fit(
            "Day 10 - 智能工具助手\n"
            "AI 会自动选择合适的工具来回答你的问题",
            style="bold green"
        )
    )

    show_menu()

    while True:
        user_input = input("\n你：").strip()
        if not user_input:
            continue

        if user_input.lower() == "q":
            console.print("\n再见！", style="bold red")
            break

        if user_input.lower() == "tools":
            console.print("\n可用工具：", style="cyan")
            for t in tools:
                console.print(f"  - {t.name}: {t.description.split('。')[0]}", style="green")
            continue

        with console.status("[bold green]思考中..."):
            result = chat(user_input)

        console.print(f"AI: {result}", style="green")

if __name__ == "__main__":
    main()
