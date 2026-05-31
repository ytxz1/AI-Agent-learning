"""工具模块"""

import math, datetime
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """执行数学计算，支持三角函数、对数、幂运算等。参数: expression - 数学表达式"""
    try:
        safe_dict = {"abs": abs, "round": round, "min": min, "max": max,
                     "sqrt": math.sqrt, "pow": pow, "pi": math.pi, "e": math.e,
                     "sin": math.sin, "cos": math.cos, "tan": math.tan,
                     "log": math.log, "log10": math.log10, "factorial": math.factorial}
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return str(int(result)) if isinstance(result, float) and result == int(result) else str(round(result, 6))
    except Exception as e:
        return f"计算错误：{e}"

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息。参数: city - 城市名称"""
    data = {"北京": "25°C，晴天", "上海": "28°C，多云", "广州": "32°C，雷阵雨",
            "深圳": "30°C，小雨", "杭州": "26°C，阴天", "成都": "24°C，多云"}
    return data.get(city, f"未找到 {city} 的天气")

@tool
def search_knowledge(query: str) -> str:
    """搜索知识库获取信息。参数: query - 搜索关键词"""
    kb = {"python": "Python 是一种高级编程语言。", "机器学习": "机器学习是 AI 的分支。",
          "langchain": "LangChain 是构建 LLM 应用的开源框架。",
          "agent": "AI Agent 是能自主决策的智能体。",
          "rag": "RAG 是检索增强生成技术。"}
    results = [f"【{k}】{v}" for k, v in kb.items() if k in query.lower()]
    return "\n".join(results) if results else f"未找到与「{query}」相关的信息"

@tool
def get_current_time() -> str:
    """获取当前日期和时间。"""
    from datetime import datetime
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

@tool
def unit_convert(value: float, from_unit: str, to_unit: str) -> str:
    """进行单位换算。参数: value - 数值, from_unit - 原单位, to_unit - 目标单位"""
    conv = {("摄氏度", "华氏度"): lambda v: v * 9 / 5 + 32,
            ("华氏度", "摄氏度"): lambda v: (v - 32) * 5 / 9,
            ("千米", "英里"): lambda v: v * 0.621371,
            ("英里", "千米"): lambda v: v / 0.621371}
    key = (from_unit, to_unit)
    if key in conv:
        return f"{value} {from_unit} = {round(conv[key](value), 4)} {to_unit}"
    return f"不支持从 {from_unit} 到 {to_unit} 的换算"

all_tools = [calculator, get_weather, search_knowledge, get_current_time, unit_convert]
tool_map = {t.name: t for t in all_tools}
