"""
Day 11 - 工具增强 Agent：让 Agent 拥有超能力

本示例演示如何给 Agent 配备丰富的工具集：
1. 定义多种实用工具
2. Agent 如何选择合适的工具
3. 多工具组合使用
"""

import os, sys, math, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 11 - 工具增强 Agent", style="bold blue")
console.print("=" * 60, style="bold blue")

# --- 定义 6 种工具 ---
@tool
def advanced_calculator(expression: str) -> str:
    """执行高级数学计算，支持三角函数、对数、幂运算等。参数: expression - 数学表达式"""
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
    """获取指定城市的天气信息。当用户询问天气时使用此工具。参数: city - 城市名称"""
    data = {
        "北京": "25°C，晴天，湿度40%，北风2级",
        "上海": "28°C，多云，湿度65%，东南风3级",
        "广州": "32°C，雷阵雨，湿度85%，南风2级",
        "深圳": "30°C，小雨，湿度75%，东风3级",
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
    """获取当前日期和时间。当用户询问当前时间或日期时使用此工具。"""
    now = datetime.datetime.now()
    return now.strftime("%Y年%m月%d日 %H:%M:%S")

@tool
def analyze_text(text: str) -> str:
    """分析文本的基本信息。当需要统计文本字数、词数等信息时使用此工具。参数: text - 要分析的文本"""
    char_count = len(text)
    chinese_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    word_count = len(text.split())
    return f"字符数：{char_count}，中文：{chinese_count}，词数：{word_count}"

@tool
def unit_convert(value: float, from_unit: str, to_unit: str) -> str:
    """进行单位换算（温度、长度、重量）。参数: value - 数值, from_unit - 原单位, to_unit - 目标单位"""
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

all_tools = [advanced_calculator, get_weather, search_knowledge, get_current_time, analyze_text, unit_convert]
tool_map = {t.name: t for t in all_tools}

# 展示工具列表
table = Table(title="可用工具集", show_header=True)
table.add_column("工具名", style="green", width=22)
table.add_column("功能", style="white", width=35)
table.add_row("advanced_calculator", "高级数学计算")
table.add_row("get_weather", "天气查询")
table.add_row("search_knowledge", "知识搜索")
table.add_row("get_current_time", "获取当前时间")
table.add_row("analyze_text", "文本分析")
table.add_row("unit_convert", "单位换算")
console.print(table)

llm = ChatOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, model=MODEL_NAME, temperature=0.7)

def tool_agent(user_input, max_rounds=5):
    """工具增强 Agent"""
    messages = [SystemMessage(content="你是一个多功能智能助手，根据问题选择合适的工具。"),
                HumanMessage(content=user_input)]
    llm_with_tools = llm.bind_tools(all_tools)

    for _ in range(max_rounds):
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        if response.tool_calls:
            for tc in response.tool_calls:
                console.print(f"  [工具调用] {tc['name']}({tc['args']})", style="yellow")
                result = tool_map[tc["name"]].invoke(tc["args"]) if tc["name"] in tool_map else "未知工具"
                console.print(f"  [结果] {result}", style="green")
                messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
        else:
            return response.content
    return "达到最大推理轮数"

# 演示
console.print("\n[bold cyan]工具增强 Agent 演示[/bold cyan]")

console.print("\n[bold]测试 1：高级数学计算[/bold]")
r = tool_agent("sin(3.14159/2) 等于多少？再算一下 2 的 20 次方")
console.print(f"Agent：{r}", style="bold green")

console.print("\n[bold]测试 2：天气 + 单位换算[/bold]")
r = tool_agent("上海天气怎么样？把气温转换成华氏度")
console.print(f"Agent：{r}", style="bold green")

console.print("\n[bold green]工具增强 Agent 演示完成！[/bold green]")
