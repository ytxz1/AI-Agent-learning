"""
Day 10 - 练习 1（基础）：添加一个新工具

任务：运行 02_custom_tool.py，添加一个新的工具（获取当前时间）

新增内容（标注 [新增]）：
  1. [新增] get_current_time 工具定义
  2. [新增] 测试 get_current_time 工具
  3. [新增] 查看新工具的 schema
"""

from langchain_core.tools import tool
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from datetime import datetime
from rich.console import Console

console = Console()

print("=" * 60)
print("Day 10 - 练习 1：添加一个新工具（获取当前时间）")
print("=" * 60)

# ==============================
# 1. 使用 @tool 装饰器创建工具
# ==============================
console.print("\n[bold]1. 使用 @tool 装饰器[/bold]", style="cyan")

@tool
def multiply(a: int, b: int) -> int:
    """将两个整数相乘。

    参数:
        a: 第一个整数
        b: 第二个整数
    """
    return a * b

@tool
def word_count(text: str) -> str:
    """统计文本的字数和词数。

    参数:
        text: 待统计的文本
    """
    char_count = len(text)
    word_count_val = len(text.split())
    return f"字数：{char_count}，词数：{word_count_val}"

# 测试工具
result = multiply.invoke({"a": 6, "b": 7})
console.print(f"multiply(6, 7) = {result}", style="green")

result = word_count.invoke({"text": "Hello World 你好世界"})
console.print(f"word_count('Hello World 你好世界') = {result}", style="green")

# ==============================
# [新增] 2. 添加 get_current_time 工具
# ==============================
console.print("\n[bold]2. [新增] 获取当前时间工具[/bold]", style="cyan")

@tool
def get_current_time(format: str = "full") -> str:
    """获取当前日期和时间。当用户问现在几点、今天几号时使用此工具。

    参数:
        format: 输出格式，可选值：
            - "full": 完整日期时间（默认），如 "2026-05-30 14:30:00"
            - "date": 仅日期，如 "2026-05-30"
            - "time": 仅时间，如 "14:30:00"
            - "chinese": 中文格式，如 "2026年05月30日 14时30分00秒"
    """
    now = datetime.now()

    if format == "date":
        return now.strftime("%Y-%m-%d")
    elif format == "time":
        return now.strftime("%H:%M:%S")
    elif format == "chinese":
        return now.strftime("%Y年%m月%d日 %H时%M分%S秒")
    else:
        return now.strftime("%Y-%m-%d %H:%M:%S")

# 测试新工具
console.print("\n[bold]测试 get_current_time 工具：[/bold]", style="yellow")

result = get_current_time.invoke({"format": "full"})
console.print(f"  get_current_time(full)    = {result}", style="green")

result = get_current_time.invoke({"format": "date"})
console.print(f"  get_current_time(date)    = {result}", style="green")

result = get_current_time.invoke({"format": "time"})
console.print(f"  get_current_time(time)    = {result}", style="green")

result = get_current_time.invoke({"format": "chinese"})
console.print(f"  get_current_time(chinese) = {result}", style="green")

# 不传参数，使用默认值
result = get_current_time.invoke({})
console.print(f"  get_current_time()        = {result}", style="green")

# ==============================
# 3. 使用 Pydantic 模型定义工具输入
# ==============================
console.print("\n[bold]3. 使用 Pydantic 模型定义输入[/bold]", style="cyan")

class WeatherInput(BaseModel):
    """天气查询的输入参数"""
    city: str = Field(description="城市名称，如：北京、上海")
    unit: str = Field(default="celsius", description="温度单位：celsius 或 fahrenheit")

@tool(args_schema=WeatherInput)
def get_weather_detailed(city: str, unit: str = "celsius") -> str:
    """查询指定城市的天气信息。

    参数:
        city: 城市名称
        unit: 温度单位
    """
    weather_data = {
        "北京": {"temp": 25, "condition": "晴天"},
        "上海": {"temp": 28, "condition": "多云"},
        "广州": {"temp": 32, "condition": "雷阵雨"},
    }
    data = weather_data.get(city)
    if not data:
        return f"未找到 {city} 的天气信息"

    temp = data["temp"]
    if unit == "fahrenheit":
        temp = temp * 9 / 5 + 32
        unit_str = "°F"
    else:
        unit_str = "°C"
    return f"{city}：{data['condition']}，{temp}{unit_str}"

result = get_weather_detailed.invoke({"city": "北京", "unit": "celsius"})
console.print(f"get_weather_detailed(北京, celsius) = {result}", style="green")

result = get_weather_detailed.invoke({"city": "上海", "unit": "fahrenheit"})
console.print(f"get_weather_detailed(上海, fahrenheit) = {result}", style="green")

# ==============================
# 4. 使用 StructuredTool 创建工具
# ==============================
console.print("\n[bold]4. 使用 StructuredTool[/bold]", style="cyan")

class MathInput(BaseModel):
    """数学运算的输入"""
    expression: str = Field(description="数学表达式，如 '2+3*4'")

def _calculate(expression: str) -> str:
    """执行数学计算"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误：{e}"

math_tool = StructuredTool.from_function(
    func=_calculate,
    name="calculator",
    description="执行数学计算，支持加减乘除、幂运算等",
    args_schema=MathInput,
)

result = math_tool.invoke({"expression": "2**10"})
console.print(f"calculator('2**10') = {result}", style="green")

# ==============================
# [新增] 5. 查看新工具的 schema
# ==============================
console.print("\n[bold]5. [新增] 查看所有工具的 schema[/bold]", style="cyan")

all_tools = [multiply, word_count, get_current_time]
for t in all_tools:
    console.print(f"\n  工具名: {t.name}", style="yellow")
    console.print(f"  描述: {t.description.split(chr(10))[0]}", style="white")
    console.print(f"  参数: {t.args_schema}", style="dim")

console.print("\n" + "=" * 60, style="bold green")
console.print("✅ 练习 1 完成：成功添加了 get_current_time 工具！", style="bold green")
console.print("=" * 60, style="bold green")
