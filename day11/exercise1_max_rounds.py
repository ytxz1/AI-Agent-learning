"""
Day 11 - 练习 1（基础）：修改 max_rounds 参数观察效果

任务：运行 Agent 基础代码，对比不同 max_rounds 值的行为差异。

新增内容（标注 [新增]）：
  1. [新增] 对比 max_rounds=1 / 3 / 5 三种情况
  2. [新增] 展示推理轮次对复杂问题的影响
  3. [新增] 记录每种情况的工具调用次数
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 11 - 练习 1：max_rounds 参数对比实验", style="bold blue")
console.print("=" * 60, style="bold blue")

llm = ChatOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, model=MODEL_NAME, temperature=0.7)

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

tools = [calculator, get_weather]
tool_map = {t.name: t for t in tools}

# [新增] Agent 函数，返回调用次数
def run_agent(user_input, max_rounds=5, verbose=True):
    """运行 Agent，返回最终答案和工具调用次数"""
    messages = [
        SystemMessage(content="你是一个智能助手，可以使用工具来帮助回答问题。"),
        HumanMessage(content=user_input),
    ]
    llm_with_tools = llm.bind_tools(tools)
    tool_call_count = 0

    for round_num in range(max_rounds):
        if verbose:
            console.print(f"  [轮次 {round_num + 1}]", style="dim cyan")
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            for tc in response.tool_calls:
                tool_name = tc["name"]
                tool_args = tc["args"]
                tool_call_count += 1
                if verbose:
                    console.print(f"    -> 调用 {tool_name}({tool_args})", style="yellow")
                result = tool_map[tool_name].invoke(tool_args) if tool_name in tool_map else "未知工具"
                if verbose:
                    console.print(f"    <- {result}", style="green")
                messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
        else:
            return response.content, tool_call_count
    return "达到最大推理轮数", tool_call_count

# [新增] 测试问题
test_question = "帮我算一下 (123 + 456) * 789，然后再算一下结果除以 3 是多少"

# [新增] 对比不同 max_rounds
console.print("\n[bold cyan]实验：对比不同 max_rounds 的效果[/bold cyan]")
console.print(f"测试问题：{test_question}\n")

# [新增] 结果对比表
result_table = Table(title="max_rounds 对比实验", show_header=True)
result_table.add_column("max_rounds", style="cyan", width=12)
result_table.add_column("工具调用次数", style="yellow", width=14)
result_table.add_column("是否完成", style="green", width=10)
result_table.add_column("最终答案", style="white", width=40)

for max_r in [1, 3, 5]:
    console.print(f"\n[bold]--- max_rounds = {max_r} ---[/bold]")
    answer, calls = run_agent(test_question, max_rounds=max_r, verbose=True)
    completed = "是" if "达到最大" not in answer else "否"
    result_table.add_row(str(max_r), str(calls), completed, answer[:50])
    console.print(f"  最终答案：{answer}", style="bold green")

# [新增] 展示对比结果
console.print("\n")
console.print(result_table)

# [新增] 总结
console.print(Panel(
    "[bold]结论：[/bold]\n"
    "  max_rounds=1：可能无法完成多步任务（只允许 1 轮推理）\n"
    "  max_rounds=3：大多数简单任务可以完成\n"
    "  max_rounds=5：复杂多步任务也能完成\n\n"
    "[bold]建议：[/bold]\n"
    "  简单任务：max_rounds=3\n"
    "  复杂任务：max_rounds=5\n"
    "  防止无限循环：始终设置 max_rounds 上限",
    title="max_rounds 参数总结",
    style="green"
))

console.print("\n练习 1 完成！", style="bold green")
