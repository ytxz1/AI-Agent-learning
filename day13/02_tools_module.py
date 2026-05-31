"""
Day 13 - Tools 模块：综合工具集

整合 Day 10 的所有工具知识，构建完整的工具模块。
"""

import os, sys, math, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_core.tools import tool
from config import OPENAI_API_KEY, OPENAI_BASE_URL
from rich.console import Console

console = Console()

# ============================================================
# 计算器工具
# ============================================================
@tool
def calculator(expression: str) -> str:
    """执行数学计算，支持三角函数、对数、幂运算等。
    当用户需要计算时使用此工具。
    参数: expression - 数学表达式，如 2 + 3 * 4、sqrt(144)"""
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

# ============================================================
# 天气查询工具
# ============================================================
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息。
    当用户询问天气时使用此工具。
    参数: city - 城市名称，如 北京、上海"""
    data = {
        "北京": "25°C，晴天，湿度40%，北风2级",
        "上海": "28°C，多云，湿度65%，东南风3级",
        "广州": "32°C，雷阵雨，湿度85%，南风2级",
        "深圳": "30°C，小雨，湿度75%，东风3级",
        "杭州": "26°C，阴天，湿度55%，西风2级",
        "成都": "24°C，多云转晴，湿度50%，微风",
    }
    return data.get(city, f"未找到 {city} 的天气，支持：{', '.join(data.keys())}")

# ============================================================
# 知识搜索工具
# ============================================================
@tool
def search_knowledge(query: str) -> str:
    """搜索知识库获取信息。
    当用户问知识性问题时使用此工具。
    参数: query - 搜索关键词"""
    kb = {
        "python": "Python 是一种高级编程语言，以简洁易读著称。广泛应用于 Web 开发、数据科学、AI 等。",
        "机器学习": "机器学习是 AI 的分支，从数据中学习。分为监督学习、无监督学习、强化学习。",
        "langchain": "LangChain 是构建 LLM 应用的开源框架，提供 Prompt、Chain、Agent、Memory 等。",
        "agent": "AI Agent 是能自主决策和执行任务的智能体，结合 LLM、工具调用和记忆系统。",
        "rag": "RAG 是 Retrieval Augmented Generation，即检索增强生成，让 LLM 基于外部文档回答。",
        "transformer": "Transformer 是 2017 年 Google 提出的架构，是 GPT、BERT 等模型的基础。",
    }
    results = [f"【{k}】{v}" for k, v in kb.items() if k in query.lower()]
    return "\n".join(results) if results else f"未找到与「{query}」相关的信息"

# ============================================================
# 时间工具
# ============================================================
@tool
def get_current_time() -> str:
    """获取当前日期和时间。当用户询问时间时使用。"""
    now = datetime.datetime.now()
    wd = ["一", "二", "三", "四", "五", "六", "日"]
    return now.strftime(f"%Y年%m月%d日 %H:%M:%S（星期{wd[now.weekday()]}）")

# ============================================================
# 单位换算工具
# ============================================================
@tool
def unit_convert(value: float, from_unit: str, to_unit: str) -> str:
    """进行单位换算（温度、长度、重量）。
    当需要换算单位时使用此工具。
    参数: value - 数值, from_unit - 原单位, to_unit - 目标单位"""
    conv = {
        ("摄氏度", "华氏度"): lambda v: v * 9 / 5 + 32,
        ("华氏度", "摄氏度"): lambda v: (v - 32) * 5 / 9,
        ("千米", "英里"): lambda v: v * 0.621371,
        ("英里", "千米"): lambda v: v / 0.621371,
        ("千克", "磅"): lambda v: v * 2.20462,
        ("磅", "千克"): lambda v: v / 2.20462,
    }
    key = (from_unit, to_unit)
    if key in conv:
        result = conv[key](value)
        return f"{value} {from_unit} = {round(result, 4)} {to_unit}"
    return f"不支持从 {from_unit} 到 {to_unit} 的换算"

# ============================================================
# 所有工具列表
# ============================================================
all_tools = [calculator, get_weather, search_knowledge, get_current_time, unit_convert]
tool_map = {t.name: t for t in all_tools}

if __name__ == "__main__":
    console.print("=" * 60, style="bold blue")
    console.print("Day 13 - Tools 模块测试", style="bold blue")
    console.print("=" * 60, style="bold blue")
    console.print(f"  [{len(all_tools)}] 个工具已注册", style="green")
    for t in all_tools:
        desc = t.description.split("。")[0]
        console.print(f"  - {t.name}: {desc}", style="white")
