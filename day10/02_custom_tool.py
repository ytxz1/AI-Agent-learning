"""
Day 10 - Tools 工具：自定义工具

本示例演示如何创建自定义工具：
1. 使用 @tool 装饰器
2. 使用 BaseTool 类
3. 工具的输入输出定义

知识点：
1. @tool 装饰器的使用
2. BaseTool 类的继承
3. 工具的 schema 定义
"""

from langchain_core.tools import tool
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from rich.console import Console

console = Console()

print("=" * 60)
print("Day 10 - 自定义工具")
print("=" * 60)

# ==============================
# 1. 使用 @tool 装饰器创建工具
# ==============================
# 最简单的方式：给函数加上 @tool 装饰器
# LangChain 会自动从函数名、类型注解、docstring 生成工具 schema
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
    word_count = len(text.split())
    return f"字数：{char_count}，词数：{word_count}"

# 测试工具
result = multiply.invoke({"a": 6, "b": 7})
console.print(f"multiply(6, 7) = {result}", style="green")

result = word_count.invoke({"text": "Hello World 你好世界"})
console.print(f"word_count('Hello World 你好世界') = {result}", style="green")

# 查看工具的 schema
console.print("\n工具 schema：", style="yellow")
print(f"multiply.name: {multiply.name}")
print(f"multiply.description: {multiply.description}")
print(f"multiply.args_schema: {multiply.args_schema}")

# ==============================
# 2. 使用 Pydantic 模型定义工具输入
# ==============================
# 更精确地定义输入参数
console.print("\n[bold]2. 使用 Pydantic 模型定义输入[/bold]", style="cyan")

class WeatherInput(BaseModel):
    """天气查询的输入参数"""
    city: str = Field(description="城市名称，如：北京、上海")
    unit: str = Field(default="celsius", description="温度单位：celsius（摄氏度）或 fahrenheit（华氏度）")

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
        temp = temp * 9/5 + 32
        unit_str = "°F"
    else:
        unit_str = "°C"

    return f"{city}：{data['condition']}，{temp}{unit_str}"

result = get_weather_detailed.invoke({"city": "北京", "unit": "celsius"})
console.print(f"get_weather_detailed(北京, celsius) = {result}", style="green")

result = get_weather_detailed.invoke({"city": "上海", "unit": "fahrenheit"})
console.print(f"get_weather_detailed(上海, fahrenheit) = {result}", style="green")

# ==============================
# 3. 使用 StructuredTool 创建工具
# ==============================
# 可以用函数 + schema 的方式创建
console.print("\n[bold]3. 使用 StructuredTool[/bold]", style="cyan")

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
# 4. 工具的三种创建方式对比
# ==============================
console.print("\n[bold]4. 三种创建方式对比[/bold]", style="cyan")

print("""
┌──────────────────┬──────────────┬──────────────┬──────────────┐
│                  │  @tool       │  BaseTool    │ StructuredTool│
├──────────────────┼──────────────┼──────────────┼──────────────┤
│  复杂度          │  最简单      │  中等        │  中等        │
│  输入定义        │  自动推断    │  手动定义    │  Pydantic    │
│  适合场景        │  简单工具    │  复杂逻辑    │  精确控制    │
│  类型安全        │  基础        │  完整        │  完整        │
│  推荐程度        │  ⭐⭐⭐       │  ⭐⭐         │  ⭐⭐⭐       │
└──────────────────┴──────────────┴──────────────┴──────────────┘

推荐：大多数场景用 @tool 装饰器即可！
""")

console.print("✅ 自定义工具演示完成！", style="bold green")
