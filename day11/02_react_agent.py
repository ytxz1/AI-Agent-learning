"""
Day 11 - ReAct 推理模式：思考-行动-观察

本示例演示 ReAct（Reasoning + Acting）模式：
1. ReAct 的核心思想：思考 -> 行动 -> 观察
2. 手动实现 ReAct Agent
3. 完整的 ReAct 对话示例
"""

import os, sys
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
console.print("Day 11 - ReAct 推理模式", style="bold blue")
console.print("=" * 60, style="bold blue")

# ReAct 模式解释
console.print("\n[bold cyan]1. ReAct = Reasoning + Acting[/bold cyan]")
console.print(Panel(
    "[bold yellow]Thought（思考）[/bold yellow]：分析当前情况，决定下一步\n"
    "[bold green]Action（行动）[/bold green]：执行具体操作（如调用工具）\n"
    "[bold blue]Observation（观察）[/bold blue]：获取行动的结果\n\n"
    "然后回到 Thought，继续循环，直到得出最终答案。",
    title="ReAct 模式", style="cyan"
))

# 定义工具
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

@tool
def search_knowledge(query: str) -> str:
    """搜索知识库获取信息。当用户问知识性问题时使用此工具。参数: query - 搜索关键词"""
    knowledge = {
        "python": "Python 是一种高级编程语言，广泛应用于 Web 开发、数据科学、AI 等领域。",
        "机器学习": "机器学习是 AI 的分支，使计算机从数据中学习。",
        "langchain": "LangChain 是构建 LLM 应用的开源框架。",
        "agent": "AI Agent 是能自主决策和执行任务的智能体。",
    }
    for key, value in knowledge.items():
        if key in query.lower():
            return f"【{key}】{value}"
    return f"未找到与「{query}」相关的信息"

tools = [calculator, get_weather, search_knowledge]
tool_map = {t.name: t for t in tools}

llm = ChatOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, model=MODEL_NAME, temperature=0.7)

def react_agent(user_input, max_rounds=5, verbose=True):
    """手动实现 ReAct Agent，每一轮都经历 Thought -> Action -> Observation"""
    system_prompt = "你是一个智能助手，使用 ReAct 模式解决问题。如果需要工具就调用，不需要就直接回答。"
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_input)]
    llm_with_tools = llm.bind_tools(tools)

    for round_num in range(max_rounds):
        if verbose:
            console.print(f"\n  [bold dim]--- ReAct 轮次 {round_num + 1} ---[/bold dim]")
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            for tc in response.tool_calls:
                tool_name = tc["name"]
                tool_args = tc["args"]
                if verbose:
                    console.print(f"  [Action] {tool_name}({tool_args})", style="yellow")
                result = tool_map[tool_name].invoke(tool_args) if tool_name in tool_map else f"错误：工具 {tool_name} 不存在"
                if verbose:
                    console.print(f"  [Observation] {result}", style="green")
                messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
        else:
            if verbose:
                console.print(f"  [Answer] {response.content}", style="bold green")
            return response.content
    return "达到最大推理轮数"

# 演示
console.print("\n[bold cyan]2. ReAct Agent 演示[/bold cyan]")

console.print("\n[bold]测试 1：多步推理[/bold]")
react_agent("Python 是什么？然后帮我算一下 2 的 10 次方")

console.print("\n[bold]测试 2：天气 + 计算组合[/bold]")
react_agent("北京天气怎么样？如果气温乘以 2 是多少度？")

console.print("\n[bold green]ReAct 推理模式演示完成！[/bold green]")
