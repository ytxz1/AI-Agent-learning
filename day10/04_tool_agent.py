"""
Day 10 - Tools 工具：工具代理（Tool Agent）

本示例演示如何构建一个完整的工具代理：
1. 定义多个工具
2. LLM 自动选择工具
3. 循环调用直到得到最终答案

知识点：
1. 多工具协作
2. 工具调用循环
3. Agent 的基本原理
"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=MODEL_NAME,
    temperature=0.7,
)

console = Console()

print("=" * 60)
print("Day 10 - 工具代理（Tool Agent）")
print("=" * 60)

# ==============================
# 1. 定义工具
# ==============================

@tool
def calculator(expression: str) -> str:
    """执行数学计算。当需要计算数学表达式时使用。

    参数:
        expression: 数学表达式，如 "2 + 3 * 4"
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误：{e}"

@tool
def get_weather(city: str) -> str:
    """获取城市天气。当用户问天气时使用。

    参数:
        city: 城市名称
    """
    weather = {
        "北京": "25°C，晴天",
        "上海": "28°C，多云",
        "广州": "32°C，雷阵雨",
        "深圳": "30°C，小雨",
    }
    return weather.get(city, f"未找到{city}的天气")

@tool
def translate_text(text: str, target_language: str) -> str:
    """翻译文本。当用户需要翻译时使用。

    参数:
        text: 待翻译的文本
        target_language: 目标语言
    """
    translations = {
        ("你好", "英文"): "Hello",
        ("谢谢", "英文"): "Thank you",
        ("python", "中文"): "Python是一种编程语言",
    }
    key = (text.lower(), target_language)
    return translations.get(key, f"暂时无法翻译「{text}」为{target_language}")

tools = [calculator, get_weather, translate_text]

# ==============================
# 2. 构建 Agent 循环
# ==============================

def run_agent(user_input: str, max_rounds: int = 5):
    """
    运行工具代理

    参数:
        user_input: 用户输入
        max_rounds: 最大工具调用轮数（防止无限循环）
    """
    console.print(f"\n[bold]用户: {user_input}[/bold]")

    # 绑定工具
    llm_with_tools = llm.bind_tools(tools)

    # 初始化消息
    messages = [HumanMessage(content=user_input)]

    # Agent 循环
    for round_num in range(max_rounds):
        console.print(f"\n[dim]--- 第 {round_num + 1} 轮 ---[/dim]")

        # 调用 LLM
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # 检查是否有工具调用
        if response.tool_calls:
            console.print(f"[yellow]LLM 决定调用工具: {len(response.tool_calls)} 个[/yellow]")

            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                console.print(f"  调用: {tool_name}({tool_args})", style="cyan")

                # 执行工具
                tool_func = next((t for t in tools if t.name == tool_name), None)
                if tool_func:
                    result = tool_func.invoke(tool_args)
                else:
                    result = "未知工具"

                console.print(f"  结果: {result}", style="green")

                # 将工具结果添加到消息
                messages.append(ToolMessage(
                    content=result,
                    tool_call_id=tool_call["id"],
                ))
        else:
            # 没有工具调用，LLM 给出了最终答案
            console.print(f"\n[bold green]AI: {response.content}[/bold green]")
            return response.content

    console.print("[red]达到最大调用轮数[/red]")
    return "达到最大调用轮数"

# ==============================
# 3. 测试 Agent
# ==============================

console.print(Panel.fit("Day 10 - 工具代理测试", style="bold green"))

# 测试1：需要调用天气工具
run_agent("北京天气怎么样？")

# 测试2：需要调用计算器
run_agent("计算 123 * 456")

# 测试3：不需要工具
run_agent("你好，你是谁？")

console.print("\n✅ 工具代理演示完成！", style="bold green")
