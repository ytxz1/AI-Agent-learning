"""
Day 11 - Agents 代理基础：什么是 Agent

本示例演示 Agent 的基本概念：
1. Agent 的定义和组成
2. Agent 与 Chain 的区别
3. 手动实现一个简单的 Agent
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# ============================================================
# 第一部分：理解 Agent 的基本概念
# ============================================================

console.print("=" * 60, style="bold blue")
console.print("Day 11 - Agents 代理基础", style="bold blue")
console.print("=" * 60, style="bold blue")

# Chain vs Agent 的区别
console.print("\n[bold cyan]1. Chain vs Agent 的区别[/bold cyan]")

table = Table(title="Chain vs Agent", show_header=True, header_style="bold magenta")
table.add_column("对比项", style="cyan", width=20)
table.add_column("Chain（链）", style="green", width=30)
table.add_column("Agent（代理）", style="yellow", width=30)
table.add_row("流程", "固定顺序：A -> B -> C", "动态决策：根据情况选择")
table.add_row("决策", "开发者预先决定", "AI 运行时自主决定")
table.add_row("工具使用", "固定的工具调用", "AI 选择用哪个工具")
table.add_row("循环", "通常无循环", "推理-行动循环")
table.add_row("灵活性", "低（改代码才能变）", "高（AI 自适应）")
table.add_row("适用场景", "明确流程的任务", "开放性、探索性任务")
console.print(table)

# 生活中的类比
console.print("\n[bold cyan]2. 生活中的 Agent 比喻[/bold cyan]")
console.print(Panel(
    "[bold]Chain 就像流水线工人：[/bold]\n"
    "  拿原料 -> 加工 -> 组装 -> 包装（固定步骤）\n\n"
    "[bold]Agent 就像项目经理：[/bold]\n"
    "  分析需求 -> 决定找谁 -> 收集结果 -> 判断是否完成",
    title="类比理解", style="cyan"
))

# ============================================================
# 第二部分：定义工具
# ============================================================

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=MODEL_NAME,
    temperature=0.7,
)

@tool
def calculator(expression: str) -> str:
    """执行数学计算。当需要计算数学表达式时使用此工具。参数: expression - 数学表达式"""
    try:
        import math
        safe_dict = {"abs": abs, "round": round, "min": min, "max": max,
                     "sqrt": math.sqrt, "pow": pow, "pi": math.pi}
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        if isinstance(result, float) and result == int(result):
            return str(int(result))
        return str(result)
    except Exception as e:
        return f"计算错误：{e}"

@tool
def get_weather(city: str) -> str:
    """获取城市天气信息。当用户问天气时使用此工具。参数: city - 城市名称"""
    weather = {"北京": "25°C，晴天", "上海": "28°C，多云", "广州": "32°C，雷阵雨"}
    return weather.get(city, f"未找到 {city} 的天气信息")

tools = [calculator, get_weather]
tool_map = {t.name: t for t in tools}

# ============================================================
# 第三部分：手动实现一个简单 Agent
# ============================================================

console.print("\n[bold cyan]3. 手动实现简单 Agent[/bold cyan]")

def simple_agent(user_input, max_rounds=5):
    """手动实现的简单 Agent，带推理循环"""
    messages = [
        SystemMessage(content="你是一个智能助手，可以使用工具来帮助回答问题。"),
        HumanMessage(content=user_input),
    ]
    llm_with_tools = llm.bind_tools(tools)

    for round_num in range(max_rounds):
        console.print(f"  [推理轮次 {round_num + 1}]", style="dim cyan")
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            for tc in response.tool_calls:
                tool_name = tc["name"]
                tool_args = tc["args"]
                tool_id = tc["id"]
                console.print(f"    -> 调用工具: {tool_name}({tool_args})", style="yellow")
                if tool_name in tool_map:
                    result = tool_map[tool_name].invoke(tool_args)
                    console.print(f"    <- 结果: {result}", style="green")
                    messages.append(ToolMessage(content=result, tool_call_id=tool_id))
        else:
            return response.content
    return "达到最大推理轮数"

# 运行演示
console.print("\n[bold cyan]4. Agent 运行演示[/bold cyan]")

console.print("\n[bold]测试 1：数学计算[/bold]")
result1 = simple_agent("帮我算一下 (123 + 456) * 789 等于多少？")
console.print(f"Agent 回答：{result1}", style="bold green")

console.print("\n[bold]测试 2：天气查询[/bold]")
result2 = simple_agent("北京今天天气怎么样？")
console.print(f"Agent 回答：{result2}", style="bold green")

console.print("\n[bold green]Agent 基础概念演示完成！[/bold green]")
