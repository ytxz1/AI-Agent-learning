"""
Day 11 - 练习 2（中等）：给 Agent 添加新工具（获取随机数）

任务：在 03_tool_agent.py 基础上添加一个随机数工具。

新增内容（标注 [新增]）：
  1. [新增] random_number 工具定义（支持范围、个数、种子）
  2. [新增] random_choice 工具定义（从列表中随机选择）
  3. [新增] 测试随机数相关的 Agent 对话
"""

import os, sys, random, math, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 11 - 练习 2：添加随机数工具", style="bold blue")
console.print("=" * 60, style="bold blue")

# --- 原有工具 ---
@tool
def calculator(expression: str) -> str:
    """执行高级数学计算。参数: expression - 数学表达式"""
    try:
        safe_dict = {"abs": abs, "round": round, "min": min, "max": max,
                     "sqrt": math.sqrt, "pow": pow, "pi": math.pi,
                     "sin": math.sin, "cos": math.cos, "tan": math.tan}
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        if isinstance(result, float) and result == int(result):
            return str(int(result))
        return str(round(result, 6))
    except Exception as e:
        return f"计算错误：{e}"

@tool
def get_weather(city: str) -> str:
    """获取城市天气信息。参数: city - 城市名称"""
    data = {"北京": "25°C，晴天", "上海": "28°C，多云", "广州": "32°C，雷阵雨"}
    return data.get(city, f"未找到 {city} 的天气")

@tool
def get_current_time() -> str:
    """获取当前日期和时间。"""
    return datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

# [新增] 随机数工具
@tool
def random_number(min_value: int = 1, max_value: int = 100, count: int = 1) -> str:
    """生成随机数。当用户需要随机数、掷骰子、抽奖时使用此工具。
    参数:
        min_value - 最小值（默认 1）
        max_value - 最大值（默认 100）
        count - 生成个数（默认 1，最多 10）"""
    if count > 10:
        count = 10
    if min_value > max_value:
        min_value, max_value = max_value, min_value
    numbers = [random.randint(min_value, max_value) for _ in range(count)]
    if count == 1:
        return f"随机数：{numbers[0]}（范围 {min_value}-{max_value}）"
    return f"随机数：{numbers}（范围 {min_value}-{max_value}，共 {count} 个）"

# [新增] 随机选择工具
@tool
def random_choice(options: str) -> str:
    """从给定选项中随机选择一个。当用户需要做选择、抽奖时使用此工具。
    参数: options - 选项列表，用逗号分隔，如 "苹果,香蕉,橘子" """
    items = [opt.strip() for opt in options.split(",") if opt.strip()]
    if not items:
        return "错误：没有提供有效选项"
    chosen = random.choice(items)
    return f"从 {items} 中随机选择了：{chosen}"

all_tools = [calculator, get_weather, get_current_time, random_number, random_choice]
tool_map = {t.name: t for t in all_tools}

# 展示新增工具
console.print("\n[bold cyan][新增] 已添加工具：[/bold cyan]")
console.print("  random_number - 生成随机数（支持范围、个数）", style="green")
console.print("  random_choice - 从列表中随机选择", style="green")

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
                console.print(f"  [工具] {tc['name']}({tc['args']})", style="yellow")
                result = tool_map[tc["name"]].invoke(tc["args"]) if tc["name"] in tool_map else "未知工具"
                console.print(f"  [结果] {result}", style="green")
                messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
        else:
            return response.content
    return "达到最大推理轮数"

# [新增] 测试随机数功能
console.print("\n[bold cyan]测试随机数工具[/bold cyan]")

console.print("\n[bold]测试 1：生成随机数[/bold]")
r = tool_agent("帮我生成 5 个 1 到 50 之间的随机数")
console.print(f"Agent：{r}", style="bold green")

console.print("\n[bold]测试 2：掷骰子[/bold]")
r = tool_agent("帮我掷 3 个骰子")
console.print(f"Agent：{r}", style="bold green")

console.print("\n[bold]测试 3：随机选择[/bold]")
r = tool_agent("今天中午吃什么？选项有：麻辣烫、黄焖鸡、沙县小吃、兰州拉面、肯德基")
console.print(f"Agent：{r}", style="bold green")

console.print("\n[bold]测试 4：组合使用[/bold]")
r = tool_agent("帮我生成一个 1-100 的随机数，然后告诉我它是奇数还是偶数")
console.print(f"Agent：{r}", style="bold green")

console.print("\n练习 2 完成！", style="bold green")
