"""
Day 10 - 练习 2（中等）：给 Agent 添加文件读取工具

任务：修改 04_tool_agent.py，添加一个读取文件的工具

新增内容（标注 [新增]）：
  1. [新增] read_file 工具定义
  2. [新增] list_files 工具定义
  3. [新增] 测试文件操作相关的 Agent 对话
"""

import os
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
print("Day 10 - 练习 2：给 Agent 添加文件读取工具")
print("=" * 60)

# ==============================
# 1. 定义原有工具
# ==============================

@tool
def calculator(expression: str) -> str:
    """执行数学计算。当需要计算数学表达式时使用。
    参数: expression - 数学表达式"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误：{e}"

@tool
def get_weather(city: str) -> str:
    """获取城市天气。当用户问天气时使用。
    参数: city - 城市名称"""
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
    参数: text - 待翻译的文本, target_language - 目标语言"""
    translations = {
        ("你好", "英文"): "Hello",
        ("谢谢", "英文"): "Thank you",
        ("python", "中文"): "Python是一种编程语言",
    }
    key = (text.lower(), target_language)
    return translations.get(key, f"暂时无法翻译{text}为{target_language}")

# ==============================
# [新增] 2. 添加文件读取工具
# ==============================
console.print("\n[bold][新增] 定义文件操作工具...[/bold]", style="cyan")

SAFE_DIR = os.path.dirname(os.path.abspath(__file__))

@tool
def read_file(file_path: str) -> str:
    """读取文件内容。当用户想查看某个文件时使用此工具。
    参数: file_path - 文件路径（相对于当前目录），如 config.py"""
    try:
        full_path = os.path.normpath(os.path.join(SAFE_DIR, file_path))
        if not full_path.startswith(SAFE_DIR):
            return "错误：不允许访问安全目录之外的文件"
        if not os.path.exists(full_path):
            return f"错误：文件 {file_path} 不存在"
        file_size = os.path.getsize(full_path)
        if file_size > 10240:
            return f"错误：文件过大（{file_size} 字节），限制 10KB"
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"文件 {file_path} 的内容（{len(content)} 字符）：\n{content}"
    except UnicodeDecodeError:
        return f"错误：文件 {file_path} 不是文本文件，无法读取"
    except Exception as e:
        return f"读取文件错误：{e}"

@tool
def list_files(directory: str = ".") -> str:
    """列出目录下的文件。当用户想查看某个目录下有什么文件时使用此工具。
    参数: directory - 目录路径（相对于当前目录），默认为当前目录"""
    try:
        full_path = os.path.normpath(os.path.join(SAFE_DIR, directory))
        if not full_path.startswith(SAFE_DIR):
            return "错误：不允许访问安全目录之外的目录"
        if not os.path.isdir(full_path):
            return f"错误：{directory} 不是目录"
        items = os.listdir(full_path)
        if not items:
            return f"目录 {directory} 是空的"
        dirs = [f for f in items if os.path.isdir(os.path.join(full_path, f))]
        files = [f for f in items if os.path.isfile(os.path.join(full_path, f))]
        result = f"目录 {directory} 的内容："
        if dirs:
            result += f"\n  文件夹：{', '.join(dirs)}"
        if files:
            result += f"\n  文件：{', '.join(files)}"
        return result
    except Exception as e:
        return f"列出文件错误：{e}"

tools = [calculator, get_weather, translate_text, read_file, list_files]

# ==============================
# 3. Agent 循环
# ==============================

def run_agent(user_input: str, max_rounds: int = 5):
    """运行工具代理"""
    console.print(f"\n[bold]用户: {user_input}[/bold]")
    llm_with_tools = llm.bind_tools(tools)
    messages = [HumanMessage(content=user_input)]

    for round_num in range(max_rounds):
        console.print(f"\n[dim]--- 第 {round_num + 1} 轮 ---[/dim]")
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            console.print(f"[yellow]LLM 决定调用工具: {len(response.tool_calls)} 个[/yellow]")
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                console.print(f"  调用: {tool_name}({tool_args})", style="cyan")
                tool_func = next((t for t in tools if t.name == tool_name), None)
                if tool_func:
                    result = tool_func.invoke(tool_args)
                else:
                    result = "未知工具"
                display_result = result if len(result) < 200 else result[:200] + "..."
                console.print(f"  结果: {display_result}", style="green")
                messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
        else:
            console.print(f"\n[bold green]AI: {response.content}[/bold green]")
            return response.content

    console.print("[red]达到最大调用轮数[/red]")
    return "达到最大调用轮数"

# ==============================
# 4. 测试
# ==============================

console.print(Panel.fit("Day 10 - 练习 2：带文件操作的 Agent", style="bold green"))

run_agent("北京天气怎么样？")
run_agent("计算 123 * 456")
run_agent("当前目录下有哪些文件？")
run_agent("帮我读取 config.py 文件的内容")
run_agent("requirements.txt 里面写了什么？")

console.print("\n" + "=" * 60, style="bold green")
console.print("练习 2 完成：成功添加了文件读取工具！", style="bold green")
console.print("=" * 60, style="bold green")
