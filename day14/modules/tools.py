"""Day 14 - 工具模块

这里放项目里会被 Agent 调用的所有工具。
每个工具都尽量做到：
1. 输入简单
2. 输出清晰
3. 便于模型理解参数
"""

from __future__ import annotations

import ast
import datetime as _dt
import math
import operator as _op
from zoneinfo import ZoneInfo

from langchain_core.tools import tool


_ALLOWED_OPERATORS = {
    ast.Add: _op.add,
    ast.Sub: _op.sub,
    ast.Mult: _op.mul,
    ast.Div: _op.truediv,
    ast.FloorDiv: _op.floordiv,
    ast.Mod: _op.mod,
    ast.Pow: _op.pow,
    ast.UAdd: _op.pos,
    ast.USub: _op.neg,
}

_ALLOWED_FUNCTIONS = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sqrt": math.sqrt,
    "pow": pow,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "factorial": math.factorial,
}

_ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}

_WEATHER_DATA = {
    "北京": {"weather": "晴", "temperature": 25, "humidity": 45, "wind": "微风"},
    "上海": {"weather": "多云", "temperature": 28, "humidity": 60, "wind": "东南风 2 级"},
    "广州": {"weather": "雷阵雨", "temperature": 32, "humidity": 78, "wind": "南风 3 级"},
    "深圳": {"weather": "小雨", "temperature": 30, "humidity": 72, "wind": "东风 2 级"},
    "杭州": {"weather": "阴", "temperature": 26, "humidity": 58, "wind": "微风"},
    "成都": {"weather": "多云", "temperature": 24, "humidity": 65, "wind": "微风"},
}

_CITY_ALIASES = {
    "beijing": "北京",
    "bj": "北京",
    "shanghai": "上海",
    "sh": "上海",
    "guangzhou": "广州",
    "gz": "广州",
    "shenzhen": "深圳",
    "sz": "深圳",
    "hangzhou": "杭州",
    "hz": "杭州",
    "chengdu": "成都",
    "cd": "成都",
}

_ZH_TO_EN = {
    "你好": "hello",
    "谢谢": "thank you",
    "我很好": "I am fine",
    "我很开心": "I am very happy",
    "今天天气不错": "The weather is nice today",
    "请帮我": "please help me",
    "早上好": "good morning",
    "晚上好": "good evening",
}

_EN_TO_ZH = {v.lower(): k for k, v in _ZH_TO_EN.items()}


def _safe_eval(node: ast.AST):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_CONSTANTS:
            return _ALLOWED_CONSTANTS[node.id]
        raise ValueError(f"不支持的变量: {node.id}")
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        value = _safe_eval(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](value)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNCTIONS:
            raise ValueError(f"不支持的函数: {func_name}")
        args = [_safe_eval(arg) for arg in node.args]
        return _ALLOWED_FUNCTIONS[func_name](*args)
    raise ValueError("表达式包含不安全或不支持的内容")


def _format_number(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def _normalize_city(city: str) -> str:
    city = city.strip()
    if city in _WEATHER_DATA:
        return city
    return _CITY_ALIASES.get(city.lower(), city)


def _normalize_language(target_language: str) -> str:
    return target_language.strip().lower()


@tool
def calculator(expression: str) -> str:
    """执行安全数学计算，支持四则运算、括号和部分数学函数。"""
    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_eval(tree)
        return _format_number(result)
    except Exception as exc:
        return f"计算失败：{exc}"


@tool
def get_weather(city: str) -> str:
    """查询模拟天气数据，参数 city 为城市名。"""
    normalized_city = _normalize_city(city)
    info = _WEATHER_DATA.get(normalized_city)
    if not info:
        return f"未找到 {city} 的天气数据。支持城市：{', '.join(_WEATHER_DATA.keys())}"
    return (
        f"{normalized_city}：{info['weather']}，{info['temperature']}°C，"
        f"湿度 {info['humidity']}%，{info['wind']}"
    )


@tool
def translate(text: str, target_language: str) -> str:
    """翻译文本到目标语言，目前主要演示中英互译。"""
    lang = _normalize_language(target_language)

    if lang in {"en", "eng", "english", "英文", "英语"}:
        translated = _ZH_TO_EN.get(text.strip())
        if translated:
            return translated
        return f"{text} (English demo translation)"

    if lang in {"zh", "zhs", "chinese", "中文", "汉语"}:
        translated = _EN_TO_ZH.get(text.strip().lower())
        if translated:
            return translated
        return f"{text}（中文示例翻译）"

    return f"暂不支持目标语言：{target_language}"


@tool
def get_current_time(timezone_name: str = "local") -> str:
    """获取当前时间，timezone_name 可填 local 或时区名。"""
    now = _dt.datetime.now()
    if timezone_name and timezone_name != "local":
        try:
            now = _dt.datetime.now(ZoneInfo(timezone_name))
        except Exception:
            return f"无法识别时区：{timezone_name}，请使用如 Asia/Shanghai 这样的时区名"
    return now.strftime("%Y-%m-%d %H:%M:%S")


@tool
def unit_convert(value: float, from_unit: str, to_unit: str) -> str:
    """进行常见单位换算，支持温度、长度、重量。"""
    from_unit = from_unit.strip().lower()
    to_unit = to_unit.strip().lower()

    converters = {
        ("c", "f"): lambda v: v * 9 / 5 + 32,
        ("celsius", "fahrenheit"): lambda v: v * 9 / 5 + 32,
        ("摄氏度", "华氏度"): lambda v: v * 9 / 5 + 32,
        ("f", "c"): lambda v: (v - 32) * 5 / 9,
        ("fahrenheit", "celsius"): lambda v: (v - 32) * 5 / 9,
        ("华氏度", "摄氏度"): lambda v: (v - 32) * 5 / 9,
        ("km", "mile"): lambda v: v * 0.621371,
        ("kilometer", "mile"): lambda v: v * 0.621371,
        ("公里", "英里"): lambda v: v * 0.621371,
        ("mile", "km"): lambda v: v / 0.621371,
        ("英里", "公里"): lambda v: v / 0.621371,
        ("kg", "lb"): lambda v: v * 2.20462,
        ("kilogram", "pound"): lambda v: v * 2.20462,
        ("公斤", "磅"): lambda v: v * 2.20462,
        ("lb", "kg"): lambda v: v / 2.20462,
        ("pound", "kilogram"): lambda v: v / 2.20462,
        ("磅", "公斤"): lambda v: v / 2.20462,
        ("m", "ft"): lambda v: v * 3.28084,
        ("meter", "foot"): lambda v: v * 3.28084,
        ("米", "英尺"): lambda v: v * 3.28084,
        ("ft", "m"): lambda v: v / 3.28084,
        ("foot", "meter"): lambda v: v / 3.28084,
        ("英尺", "米"): lambda v: v / 3.28084,
    }

    key = (from_unit, to_unit)
    if key not in converters:
        return f"不支持从 {from_unit} 到 {to_unit} 的换算"
    result = converters[key](value)
    return f"{_format_number(value)} {from_unit} = {_format_number(round(result, 6))} {to_unit}"


all_tools = [calculator, get_weather, translate, get_current_time, unit_convert]
tool_map = {tool_item.name: tool_item for tool_item in all_tools}

