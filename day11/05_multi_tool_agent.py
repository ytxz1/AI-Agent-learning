"""
Day 11 - 多工具综合 Agent：完整智能助手

整合 LLM + Tools + Memory，构建功能完整的智能助手。
"""

import os, sys, math, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 11 - 多工具综合 Agent", style="bold blue")
console.print("=" * 60, style="bold blue")

# 定义完整工具集
@tool
def calculator(expression: str) -> str:
    """执行数学计算。当需要计算数学表达式时使用此工具。参数: expression - 数学表达式"""
    try:
        safe_dict = {"abs": abs, "round": round, "min": min, "max": max,
                     "sqrt": math.sqrt, "pow": pow, "pi": math.pi, "e": math.e,
                     "sin": math.sin, "cos": math.cos, "tan": math.tan,
                     "log": math.log, "log10": math.log10, "factorial": math.factorial}
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        if isinstance(result, float) and result == int(result):
            return str(int(result))
        return str(round(result, 6))
    except Exception as e:
        return f"计算错误：{e}"

@tool
def get_weather(city: str) -> str:
    """获取城市天气信息。当用户问天气时使用此工具。参数: city - 城市名称"""
    data = {
        "北京": "25°C，晴天，湿度40%，北风2级",
        "上海": "28°C，多云，湿度65%，东南风3级",
        "广州": "32°C，雷阵雨，湿度85%，南风2级",
    }
    return data.get(city, f"未找到 {city} 的天气信息")

@tool
def search_knowledge(query: str) -> str:
    """搜索知识库获取信息。当用户问知识性问题时使用此工具。参数: query - 搜索关键词"""
    knowledge = {
        "python": "Python 是一种高级编程语言，广泛应用于 Web、数据科学、AI 等领域。",
        "机器学习": "机器学习是 AI 的分支，使计算机从数据中学习。",
        "langchain": "LangChain 是构建 LLM 应用的开源框架。",
        "agent": "AI Agent 是能自主决策和执行任务的智能体。",
    }
    results = []
    for key, value in knowledge.items():
        if key in query.lower():
            results.append(f"【{key}】{value}")
    return "\n".join(results) if results else f"未找到与「{query}」相关的信息"

@tool
def get_current_time() -> str:
    """获取当前日期和时间。当用户询问时间时使用此工具。"""
    return datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

@tool
def analyze_text(text: str) -> str:
    """分析文本的基本信息。参数: text - 要分析的文本"""
    char_count = len(text)
    chinese_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    return f"字符数：{char_count}，中文字符：{chinese_count}，词数：{len(text.split())}"

@tool
def unit_convert(value: float, from_unit: str, to_unit: str) -> str:
    """进行单位换算。参数: value - 数值, from_unit - 原单位, to_unit - 目标单位"""
    conversions = {
        ("摄氏度", "华氏度"): lambda v: v * 9 / 5 + 32,
        ("华氏度", "摄氏度"): lambda v: (v - 32) * 5 / 9,
        ("千米", "英里"): lambda v: v * 0.621371,
        ("英里", "千米"): lambda v: v / 0.621371,
        ("千克", "磅"): lambda v: v * 2.20462,
        ("磅", "千克"): lambda v: v / 2.20462,
    }
    key = (from_unit, to_unit)
    if key in conversions:
        result = conversions[key](value)
        return f"{value} {from_unit} = {round(result, 4)} {to_unit}"
    return f"不支持从 {from_unit} 到 {to_unit} 的换算"

all_tools = [calculator, get_weather, search_knowledge, get_current_time, analyze_text, unit_convert]
tool_map = {t.name: t for t in all_tools}

class MultiToolAgent:
    """多工具综合 Agent，整合 LLM + Tools + Memory"""

    def __init__(self, max_history=30, max_rounds=5):
        self.max_history = max_history
        self.max_rounds = max_rounds
        self.system_prompt = SystemMessage(content=(
            "你是一个功能强大的智能助手，拥有计算、天气、搜索、时间、文本分析、单位换算等工具。"
            "根据用户问题选择合适的工具。记住之前的对话内容。"
        ))
        self.messages = [self.system_prompt]
        llm_obj = ChatOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, model=MODEL_NAME, temperature=0.7)
        self.llm = llm_obj.bind_tools(all_tools)

    def chat(self, user_input):
        """与 Agent 对话"""
        self.messages.append(HumanMessage(content=user_input))

        for _ in range(self.max_rounds):
            response = self.llm.invoke(self.messages)
            self.messages.append(response)

            if response.tool_calls:
                for tc in response.tool_calls:
                    console.print(f"  [工具] {tc['name']}({tc['args']})", style="yellow")
                    try:
                        result = tool_map[tc["name"]].invoke(tc["args"]) if tc["name"] in tool_map else "未知工具"
                    except Exception as e:
                        result = f"工具执行错误：{e}"
                    console.print(f"  [结果] {result}", style="green")
                    self.messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
            else:
                self._trim_history()
                return response.content
        return "达到最大推理轮数"

    def _trim_history(self):
        if len(self.messages) > self.max_history:
            self.messages = [self.messages[0]] + self.messages[-(self.max_history - 1):]

    def clear(self):
        self.messages = [self.system_prompt]

# 演示
console.print("\n[bold cyan]多工具 Agent 演示[/bold cyan]")
agent = MultiToolAgent()

tests = [
    "你好，介绍一下你的能力",
    "帮我算一下 (123 + 456) * 789",
    "北京天气怎么样？",
    "把北京的气温转换成华氏度",
    "上海的天气呢？",
    "现在几点了？",
    "什么是 Agent？",
]

for msg in tests:
    console.print(f"\n[bold]你：{msg}[/bold]")
    console.print("-" * 50)
    response = agent.chat(msg)
    console.print(f"Agent：{response}", style="green")

console.print("\n[bold green]多工具综合 Agent 演示完成！[/bold green]")
