"""
Day 10 - Tools 工具：LLM 工具调用

本示例演示如何让 LLM 自动决定调用哪个工具：
1. 定义工具 schema
2. 将工具绑定到 LLM
3. LLM 自动选择和调用工具

知识点：
1. bind_tools() 方法
2. tool_calls 的解析
3. 工具调用的完整流程
"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=MODEL_NAME,
    temperature=0.7,
)

console = Console()

print("=" * 60)
print("Day 10 - LLM 工具调用")
print("=" * 60)

# ==============================
# 1. 定义工具
# ==============================
console.print("\n[bold]1. 定义工具[/bold]", style="cyan")

@tool
def calculator(expression: str) -> str:
    """执行数学计算。当用户问数学问题时使用此工具。

    参数:
        expression: 数学表达式，如 "2 + 3 * 4"
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误：{e}"

@tool
def get_weather(city: str) -> str:
    """获取城市天气信息。当用户问天气相关问题时使用此工具。

    参数:
        city: 城市名称
    """
    weather = {
        "北京": "25°C，晴天",
        "上海": "28°C，多云",
        "广州": "32°C，雷阵雨",
    }
    return weather.get(city, f"未找到{city}的天气信息")

# 工具列表
tools = [calculator, get_weather]

# ==============================
# 2. 将工具绑定到 LLM
# ==============================
# bind_tools() 会把工具的 schema 告诉 LLM
# LLM 就知道有哪些工具可用，以及如何调用
console.print("\n[bold]2. 绑定工具到 LLM[/bold]", style="cyan")

llm_with_tools = llm.bind_tools(tools)
console.print("工具已绑定到 LLM", style="green")

# ==============================
# 3. LLM 自动选择工具
# ==============================
console.print("\n[bold]3. LLM 自动选择工具[/bold]", style="cyan")

# 测试1：数学问题
console.print("\n[bold]问题1: 北京天气怎么样？[/bold]")
response = llm_with_tools.invoke("北京天气怎么样？")

print(f"AI 决定调用工具: {response.tool_calls}")
# 输出类似: [{'name': 'get_weather', 'args': {'city': '北京'}, 'id': '...'}]

# 执行工具调用
if response.tool_calls:
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        console.print(f"调用工具: {tool_name}({tool_args})", style="yellow")

        # 根据工具名找到对应的工具并执行
        if tool_name == "get_weather":
            result = get_weather.invoke(tool_args)
        elif tool_name == "calculator":
            result = calculator.invoke(tool_args)
        else:
            result = "未知工具"

        console.print(f"工具结果: {result}", style="green")

# 测试2：数学问题
console.print("\n[bold]问题2: 计算 (15 + 27) * 3[/bold]")
response = llm_with_tools.invoke("计算 (15 + 27) * 3")

if response.tool_calls:
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        console.print(f"调用工具: {tool_name}({tool_args})", style="yellow")

        if tool_name == "calculator":
            result = calculator.invoke(tool_args)
        elif tool_name == "get_weather":
            result = get_weather.invoke(tool_args)
        else:
            result = "未知工具"

        console.print(f"工具结果: {result}", style="green")

# ==============================
# 4. 完整的工具调用流程
# ==============================
console.print("\n[bold]4. 完整流程图[/bold]", style="cyan")

print("""
用户问题: "北京天气怎么样？"
    │
    ▼
LLM 分析问题 → 判断需要调用工具
    │
    ▼
LLM 返回 tool_calls:
  [{name: "get_weather", args: {city: "北京"}}]
    │
    ▼
程序执行工具:
  result = get_weather("北京") → "25°C，晴天"
    │
    ▼
将工具结果发回给 LLM:
  ToolMessage(content="25°C，晴天", tool_call_id="...")
    │
    ▼
LLM 生成最终回复:
  "北京今天25°C，晴天，适合出门。"
""")

console.print("✅ LLM 工具调用演示完成！", style="bold green")
