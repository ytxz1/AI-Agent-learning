"""工具模块。

这里保存 Agent 能调用的几个基础工具：
- 数学计算
- 天气查询
- 知识检索
- 当前时间
- 单位转换

这一版把原先的文档问答知识说明，改成了“输出解析 / 结构化输出”的知识说明。
"""

from __future__ import annotations

import math
from datetime import datetime

from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """执行安全的数学计算。"""
    try:
        safe_dict = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sqrt": math.sqrt,
            "pow": pow,
            "pi": math.pi,
            "e": math.e,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "factorial": math.factorial,
        }
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        if isinstance(result, float) and result == int(result):
            return str(int(result))
        return str(round(result, 6))
    except Exception as exc:
        return f"计算错误：{exc}"


@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息。"""
    data = {
        "北京": "25°C，晴天",
        "上海": "28°C，多云",
        "广州": "32°C，雷阵雨",
        "深圳": "30°C，小雨",
        "杭州": "26°C，阴天",
        "成都": "24°C，多云",
    }
    return data.get(city, f"未找到 {city} 的天气信息")


@tool
def search_knowledge(query: str) -> str:
    """从一个简易知识库里检索信息。"""
    kb = {
        "python": "Python 是一种高级编程语言。",
        "机器学习": "机器学习是人工智能的重要分支。",
        "langchain": "LangChain 是构建 LLM 应用的开源框架。",
        "agent": "AI Agent 是能够自主决策并调用工具的智能体。",
        "输出解析": "输出解析是把自然语言整理成结构化结果的过程。",
        "结构化输出": "结构化输出通常会把内容整理成 JSON、表格或固定字段。",
        "json": "JSON 是一种轻量级的数据交换格式。",
    }
    results = [f"【{k}】{v}" for k, v in kb.items() if k in query.lower() or k in query]
    return "\n".join(results) if results else f"未找到与「{query}」相关的信息"


@tool
def get_current_time() -> str:
    """获取当前日期和时间。"""
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")


@tool
def unit_convert(value: float, from_unit: str, to_unit: str) -> str:
    """进行单位换算。"""
    conv = {
        ("摄氏度", "华氏度"): lambda v: v * 9 / 5 + 32,
        ("华氏度", "摄氏度"): lambda v: (v - 32) * 5 / 9,
        ("千米", "英里"): lambda v: v * 0.621371,
        ("英里", "千米"): lambda v: v / 0.621371,
    }
    key = (from_unit, to_unit)
    if key in conv:
        return f"{value} {from_unit} = {round(conv[key](value), 4)} {to_unit}"
    return f"不支持从 {from_unit} 到 {to_unit} 的换算"


all_tools = [calculator, get_weather, search_knowledge, get_current_time, unit_convert]
tool_map = {t.name: t for t in all_tools}
