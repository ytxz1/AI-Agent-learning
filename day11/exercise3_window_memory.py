"""
Day 11 - 练习 3（进阶）：带窗口记忆的 Agent

任务：实现一个只保留最近 K 轮对话的 Agent（滑动窗口记忆）。

新增内容（标注 [新增]）：
  1. [新增] WindowMemoryAgent 类（只保留最近 K 轮）
  2. [新增] 对比无记忆 / 全记忆 / 窗口记忆三种模式
  3. [新增] 展示窗口记忆的裁剪过程
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 11 - 练习 3：带窗口记忆的 Agent", style="bold blue")
console.print("=" * 60, style="bold blue")

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

# [新增] 窗口记忆 Agent 类
class WindowMemoryAgent:
    """带滑动窗口记忆的 Agent，只保留最近 K 轮对话。

    与全记忆 Agent 的区别：
    - 全记忆：保存所有对话历史，Token 会越来越多
    - 窗口记忆：只保留最近 K 轮，Token 稳定可控
    """

    def __init__(self, window_size=5):
        """
        初始化窗口记忆 Agent。

        参数:
            window_size: 窗口大小，保留最近几轮对话（1 轮 = 1 个 HumanMessage + 1 个 AIMessage）
        """
        self.window_size = window_size
        self.system_prompt = SystemMessage(content="你是一个智能助手，可以使用工具回答问题。")
        # 完整的历史（用于展示）
        self.full_history = [self.system_prompt]
        # 发送给 LLM 的消息（受窗口限制）
        self.messages = [self.system_prompt]
        self.llm = llm.bind_tools(tools)

    def chat(self, user_input):
        """与 Agent 对话"""
        # 添加用户消息
        user_msg = HumanMessage(content=user_input)
        self.full_history.append(user_msg)
        self.messages.append(user_msg)

        # 推理循环
        max_rounds = 5
        for _ in range(max_rounds):
            response = self.llm.invoke(self.messages)
            self.messages.append(response)
            self.full_history.append(response)

            if response.tool_calls:
                for tc in response.tool_calls:
                    tool_name = tc["name"]
                    result = tool_map[tool_name].invoke(tc["args"]) if tool_name in tool_map else "未知工具"
                    tool_msg = ToolMessage(content=result, tool_call_id=tc["id"])
                    self.messages.append(tool_msg)
                    self.full_history.append(tool_msg)
            else:
                # 裁剪窗口
                self._trim_window()
                return response.content
        return "达到最大推理轮数"

    def _trim_window(self):
        """[新增] 滑动窗口裁剪：只保留最近 window_size 轮对话"""
        # 保留 SystemMessage + 最近 window_size * 2 条消息（每轮 = Human + AI）
        max_messages = self.window_size * 2 + 1  # +1 for SystemMessage
        if len(self.messages) > max_messages:
            removed = len(self.messages) - max_messages
            self.messages = [self.messages[0]] + self.messages[-(max_messages - 1):]
            console.print(f"  [dim]窗口裁剪：移除了 {removed} 条旧消息，保留最近 {self.window_size} 轮[/dim]", style="dim")

    def get_stats(self):
        """[新增] 获取记忆统计信息"""
        return {
            "full_history": len(self.full_history),
            "window_messages": len(self.messages),
            "window_size": self.window_size,
        }

# [新增] 对比三种记忆模式
console.print("\n[bold cyan]三种记忆模式对比[/bold cyan]")

table = Table(title="记忆模式对比", show_header=True)
table.add_column("模式", style="cyan", width=15)
table.add_column("保存内容", style="white", width=25)
table.add_column("Token 消耗", style="yellow", width=15)
table.add_column("适用场景", style="green", width=25)
table.add_row("无记忆", "只保留当前轮", "最低", "单轮问答")
table.add_row("全记忆", "所有对话历史", "持续增长", "短对话")
table.add_row("窗口记忆", "最近 K 轮", "稳定可控", "中长对话")
console.print(table)

# [新增] 运行窗口记忆 Agent 演示
console.print("\n[bold cyan]窗口记忆 Agent 演示（window_size=3）[/bold cyan]")

agent = WindowMemoryAgent(window_size=3)

test_messages = [
    "你好，我叫小明",              # 第 1 轮
    "北京天气怎么样？",             # 第 2 轮
    "上海呢？",                    # 第 3 轮（测试记忆）
    "帮我算一下 2 的 10 次方",      # 第 4 轮（第 1 轮可能被裁剪）
    "我叫什么名字？",              # 第 5 轮（测试是否还记得）
    "广州天气怎么样？",             # 第 6 轮
]

for msg in test_messages:
    console.print(f"\n[bold]你：{msg}[/bold]")
    console.print("-" * 40)
    response = agent.chat(msg)
    console.print(f"Agent：{response}", style="green")

    # [新增] 显示记忆状态
    stats = agent.get_stats()
    console.print(f"  [dim]完整历史：{stats['full_history']} 条 | 窗口内：{stats['window_messages']} 条 | 窗口大小：{stats['window_size']} 轮[/dim]")

# [新增] 最终状态
console.print("\n[bold cyan]最终记忆状态[/bold cyan]")
stats = agent.get_stats()
console.print(f"  完整历史总消息数：{stats['full_history']}")
console.print(f"  窗口内消息数：{stats['window_messages']}（SystemMessage + 最近 {stats['window_size']} 轮）")

console.print(Panel(
    "[bold]窗口记忆的工作原理：[/bold]\n\n"
    "  窗口大小 = 3 表示只保留最近 3 轮对话\n"
    "  每轮 = 1 个 HumanMessage + 1 个 AIMessage（可能还有 ToolMessage）\n"
    "  当对话超过 3 轮时，最旧的消息会被移除\n\n"
    "[bold]效果：[/bold]\n"
    "  - Agent 能记住最近 3 轮的内容（如上海天气）\n"
    "  - 更早的内容会被遗忘（如用户的名字）\n"
    "  - Token 消耗保持稳定，不会无限增长",
    title="窗口记忆原理",
    style="green"
))

console.print("\n练习 3 完成！", style="bold green")
