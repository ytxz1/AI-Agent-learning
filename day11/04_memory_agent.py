"""
Day 11 - 带记忆的 Agent：让 Agent 记住对话历史

本示例演示如何给 Agent 添加记忆能力：
1. 为什么 Agent 需要记忆
2. 手动管理对话历史
3. 记忆 + 工具 + Agent 的整合
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 11 - 带记忆的 Agent", style="bold blue")
console.print("=" * 60, style="bold blue")

console.print("\n[bold cyan]为什么 Agent 需要记忆？[/bold cyan]")
console.print(Panel(
    "[bold]没有记忆：[/bold]\n"
    "  你：北京天气怎么样？ -> Agent：北京 25°C\n"
    "  你：那上海呢？ -> Agent：??? 你在说什么？\n\n"
    "[bold]有记忆：[/bold]\n"
    "  你：北京天气怎么样？ -> Agent：北京 25°C\n"
    "  你：那上海呢？ -> Agent：上海 28°C（理解你在问天气）",
    title="记忆的重要性", style="cyan"
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

tools = [calculator, get_weather]
tool_map = {t.name: t for t in tools}

llm = ChatOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, model=MODEL_NAME, temperature=0.7)

class MemoryAgent:
    """带记忆的 Agent 类，会记住所有对话历史"""

    def __init__(self, max_history=20):
        """初始化，max_history 限制历史消息数量"""
        self.max_history = max_history
        self.system_prompt = SystemMessage(content="你是一个有记忆的智能助手，能记住之前的对话内容。")
        self.messages = [self.system_prompt]
        self.llm = llm.bind_tools(tools)

    def chat(self, user_input, max_rounds=5):
        """与 Agent 对话，自动管理记忆"""
        self.messages.append(HumanMessage(content=user_input))

        for _ in range(max_rounds):
            response = self.llm.invoke(self.messages)
            self.messages.append(response)

            if response.tool_calls:
                for tc in response.tool_calls:
                    tool_name = tc["name"]
                    result = tool_map[tool_name].invoke(tc["args"]) if tool_name in tool_map else f"错误：工具 {tool_name} 不存在"
                    self.messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
            else:
                self._trim_history()
                return response.content
        return "达到最大推理轮数"

    def _trim_history(self):
        """裁剪对话历史，防止 Token 超限"""
        if len(self.messages) > self.max_history:
            self.messages = [self.messages[0]] + self.messages[-(self.max_history - 1):]

    def clear_history(self):
        """清空对话历史"""
        self.messages = [self.system_prompt]

# 演示多轮对话
console.print("\n[bold cyan]带记忆的 Agent 演示[/bold cyan]")

agent = MemoryAgent(max_history=20)

test_messages = [
    "你好，我叫小明",
    "北京天气怎么样？",
    "上海呢？",
    "帮我算一下 2 的 10 次方",
    "再加上刚才的计算结果，乘以 2",
]

for msg in test_messages:
    console.print(f"\n[bold]你：{msg}[/bold]")
    console.print("-" * 40)
    response = agent.chat(msg)
    console.print(f"Agent：{response}", style="green")

# 显示历史
console.print("\n[bold cyan]对话历史记录[/bold cyan]")
history = agent.messages
console.print(f"历史消息数：{len(history)}")
for i, msg in enumerate(history):
    if isinstance(msg, SystemMessage):
        console.print(f"  [{i}] System: {msg.content[:50]}...", style="dim")
    elif isinstance(msg, HumanMessage):
        console.print(f"  [{i}] Human: {msg.content}", style="cyan")
    elif isinstance(msg, AIMessage):
        content = msg.content if msg.content else "[工具调用]"
        console.print(f"  [{i}] AI: {content[:80]}", style="green")

console.print("\n[bold green]带记忆的 Agent 演示完成！[/bold green]")
