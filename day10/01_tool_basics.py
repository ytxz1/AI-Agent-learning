"""
Day 10 - Tools 工具：什么是工具

本示例演示工具的基本概念：
1. 工具就是一个普通的 Python 函数
2. 工具需要有清晰的文档字符串（docstring）
3. 工具需要有类型注解

知识点：
1. 工具的定义
2. 工具的三要素：函数名、参数、返回值
3. 工具和普通函数的区别
"""

from tools.calculator import calculator
from tools.weather import get_weather
from tools.translator import translate
from tools.search import search_knowledge
from rich.console import Console

console = Console()

print("=" * 60)
print("Day 10 - 什么是工具（Tool）")
print("=" * 60)

# ==============================
# 1. 工具就是普通的 Python 函数
# ==============================
console.print("\n[bold]1. 工具就是普通的 Python 函数[/bold]", style="cyan")

# 计算器工具
result = calculator("2 + 3 * 4")
console.print(f"calculator('2 + 3 * 4') = {result}", style="green")

result = calculator("sqrt(144) + pow(2, 10)")
console.print(f"calculator('sqrt(144) + pow(2, 10)') = {result}", style="green")

# 天气工具
result = get_weather("北京")
console.print(f"get_weather('北京') = {result}", style="green")

# 翻译工具
result = translate("你好", "英文")
console.print(f"translate('你好', '英文') = {result}", style="green")

# 搜索工具
result = search_knowledge("python")
console.print(f"search_knowledge('python') = {result[:80]}...", style="green")

# ==============================
# 2. 查看工具的文档
# ==============================
console.print("\n[bold]2. 查看工具的文档[/bold]", style="cyan")

print(f"calculator 的文档：\n{calculator.__doc__}")
print(f"\nget_weather 的文档：\n{get_weather.__doc__}")

# ==============================
# 3. 工具的三要素
# ==============================
console.print("\n[bold]3. 工具的三要素[/bold]", style="cyan")

print("""
┌──────────────┬──────────────────────────────────────┐
│     要素     │              说明                     │
├──────────────┼──────────────────────────────────────┤
│  函数名      │ 工具的名称，AI 通过名称来调用         │
│  参数        │ 工具需要的输入，有类型注解             │
│  返回值      │ 工具的输出，通常是字符串               │
│  文档字符串  │ 描述工具的功能，AI 据此决定何时调用    │
└──────────────┴──────────────────────────────────────┘

AI 决定是否调用某个工具的依据：
  1. 看工具的名称是否和用户需求相关
  2. 看工具的文档描述是否匹配用户问题
  3. 看工具的参数是否能从用户问题中提取

所以，好的工具需要：
  - 清晰的函数名（如 get_weather、calculator）
  - 准确的类型注解（如 city: str、expression: str）
  - 详细的文档字符串（描述功能、参数、返回值）
""")

console.print("✅ 工具基础概念演示完成！", style="bold green")
