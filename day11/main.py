"""
Day 11 - 综合实践：交互式智能 Agent 助手

整合所有 Agent 知识，构建一个完整的交互式智能助手。
运行方式：python main.py
"""

import os, sys, math, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# ==============================
# 定义工具集
# ==============================

@tool
def calculator(expression: str) -> str:
    """执行数学计算，支持加减乘除、幂运算、三角函数等。参数: expression - 数学表达式"""
    try:
        safe_dict = {"abs": abs, "round": round, "min": min, "max": max,
                     "sqrt": math.sqrt, "pow": pow, "pi": math.pi, "e": math.e,
                     "sin": math.sin, "cos": math.cos, "tan": math.tan,
                     "log": math.log, "log10": math.log10, "factorial": math.factorial}
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        if isinstance(result, float) and result == int(result):
            return str(int(result))
        return str(round(result, 6))
    except Exception as e:
        return f"计算错误：{e}"

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息。参数: city - 城市名称"""
    data = {
        "北京": "25°C，晴天，湿度40%，北风2级",
        "上海": "28°C，多云，湿度65%，东南风3级",
        "广州": "32°C，雷阵雨，湿度85%，南风2级",
        "深圳": "30°C，小雨，湿度75%，东风3级",
        "杭州": "26°C，阴天，湿度55%，西风2级",
    }
    return data.get(city, f"未找到 {city} 的天气信息，支持：{', '.join(data.keys())}")

@tool
def search_knowledge(query: str) -> str:
    """搜索知识库获取信息。参数: query - 搜索关键词"""
    knowledge = {
        "python": "Python 是一种高级编程语言，以简洁易读著称。",
        "机器学习": "机器学习是 AI 的分支，使计算机从数据中学习。",
        "langchain": "LangChain 是构建 LLM 应用的开源框架。",
        "agent": "AI Agent 是能自主决策和执行任务的智能体。",
        "transformer": "Transformer 是 2017 年 Google 提出的神经网络架构。",
    }
    results = []
    for key, value in knowledge.items():
        if key in query.lower():
            results.append(f"【{key}】{value}")
    return "\n".join(results) if results else f"未找到与「{query}」相关的信息"

@tool
def get_current_time() -> str:
    """获取当前日期和时间。"""
    now = datetime.datetime.now()
    weekdays = ["一", "二", "三", "四", "五", "六", "日"]
    return now.strftime(f"%Y年%m月%d日 %H:%M:%S（星期{weekdays[now.weekday()]}）")

@tool
def analyze_text(text: str) -> str:
    """分析文本的基本信息。参数: text - 要分析的文本"""
    char_count = len(text)
    chinese_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    return f"字符数：{char_count}，中文字符：{chinese_count}，词数：{len(text.split())}"

@tool
def unit_convert(value: float, from_unit: str, to_unit: str) -> str:
    """进行单位换算（温度、长度、重量）。参数: value - 数值, from_unit - 原单位, to_unit - 目标单位"""
    conversions = {
        ("摄氏度", "华氏度"): lambda v: v * 9 / 5 + 32,
        ("华氏度", "摄氏度"): lambda v: (v - 32) * 5 / 9,
        ("千米", "英里"): lambda v: v * 0.621371,
        ("英里", "千米"): lambda v: v / 0.621371,
        ("千克", "磅"): lambda v: v * 2.20462,
        ("磅", "千克"): lambda v: v / 2.20462,
    }
    key = (from_unit, to_unit)
    if key in conversions:
        result = conversions[key](value)
        return f"{value} {from_unit} = {round(result, 4)} {to_unit}"
    return f"不支持从 {from_unit} 到 {to_unit} 的换算"

all_tools = [calculator, get_weather, search_knowledge, get_current_time, analyze_text, unit_convert]
tool_map = {t.name: t for t in all_tools}

# ==============================
# Agent 类
# ==============================

class InteractiveAgent:
    """交互式智能 Agent 助手"""

    def __init__(self, max_history=30, max_rounds=5):
        self.max_history = max_history
        self.max_rounds = max_rounds
        self.system_prompt = SystemMessage(content=(
            "你是一个功能强大的智能助手，名叫 Day11 Agent。"
            "拥有计算、天气、搜索、时间、文本分析、单位换算等工具。"
            "根据用户问题选择合适的工具，记住之前的对话。回答要简洁准确。"
        ))
        self.messages = [self.system_prompt]
        llm_obj = ChatOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, model=MODEL_NAME, temperature=0.7)
        self.llm = llm_obj.bind_tools(all_tools)

    def chat(self, user_input):
        """处理用户输入并返回回答"""
        self.messages.append(HumanMessage(content=user_input))

        for _ in range(self.max_rounds):
            response = self.llm.invoke(self.messages)
            self.messages.append(response)

            if response.tool_calls:
                for tc in response.tool_calls:
                    tool_name = tc["name"]
                    tool_args = tc["args"]
                    if tool_name in tool_map:
                        try:
                            result = tool_map[tool_name].invoke(tool_args)
                        except Exception as e:
                            result = f"工具执行错误：{e}"
                    else:
                        result = f"未知工具：{tool_name}"
                    console.print(f"  [dim]工具: {tool_name}({tool_args})[/dim]")
                    console.print(f"  [dim]结果: {result}[/dim]")
                    self.messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
            else:
                self._trim_history()
                return response.content
        return "达到最大推理轮数，请尝试简化问题。"

    def _trim_history(self):
        if len(self.messages) > self.max_history:
            self.messages = [self.messages[0]] + self.messages[-(self.max_history - 1):]

    def clear(self):
        self.messages = [self.system_prompt]
        console.print("[dim]对话历史已清空[/dim]")

# ==============================
# 菜单和主程序
# ==============================

def show_menu():
    table = Table(title="Day 11 - 智能 Agent 助手", show_header=True, header_style="bold magenta")
    table.add_column("命令", style="green", width=12)
    table.add_column("说明", style="white")
    table.add_row("直接输入", "和 Agent 对话，自动调用工具")
    table.add_row("tools", "查看所有可用工具")
    table.add_row("history", "查看对话历史")
    table.add_row("clear", "清空对话历史")
    table.add_row("example", "查看示例问题")
    table.add_row("q", "退出程序")
    console.print(table)

def show_tools():
    console.print("\n[bold cyan]可用工具：[/bold cyan]")
    for t in all_tools:
        desc = t.description.split("。")[0] if t.description else "无描述"
        console.print(f"  {t.name}: {desc}", style="green")

def show_examples():
    examples = [
        "帮我算一下 2 的 20 次方",
        "北京天气怎么样？",
        "什么是机器学习？",
        "现在几点了？",
        "把 25 摄氏度转换成华氏度",
        "帮我分析这段文字：人工智能正在改变世界",
        "上海天气怎么样？然后把气温转换成华氏度",
    ]
    console.print("\n[bold cyan]示例问题：[/bold cyan]")
    for i, ex in enumerate(examples, 1):
        console.print(f"  {i}. {ex}", style="yellow")

def main():
    console.print(Panel.fit(
        "Day 11 - 智能 Agent 助手\n"
        "整合 LLM + Tools + Memory\n"
        "输入 example 查看示例问题",
        style="bold green"
    ))
    show_menu()
    agent = InteractiveAgent()

    while True:
        try:
            user_input = input("\n你：").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n再见！", style="bold red")
            break

        if not user_input:
            continue

        cmd = user_input.lower()
        if cmd == "q":
            console.print("\n再见！", style="bold red")
            break
        elif cmd == "tools":
            show_tools()
            continue
        elif cmd == "history":
            for msg in agent.messages:
                if isinstance(msg, HumanMessage):
                    console.print(f"  你：{msg.content}", style="cyan")
                elif isinstance(msg, AIMessage):
                    content = msg.content if msg.content else "[工具调用]"
                    console.print(f"  AI：{content[:80]}", style="green")
            continue
        elif cmd == "clear":
            agent.clear()
            continue
        elif cmd == "example":
            show_examples()
            continue

        with console.status("[bold green]思考中..."):
            response = agent.chat(user_input)
        console.print(f"\nAgent：{response}", style="bold green")

if __name__ == "__main__":
    main()
