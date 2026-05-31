"""
Day 10 - 练习 3（进阶）：代码助手 Agent

任务：构建一个代码助手 Agent，支持代码生成、解释、运行。

功能：
  1. generate_code  - 根据需求生成代码
  2. explain_code   - 解释代码的含义
  3. run_code       - 在安全沙箱中运行 Python 代码
  4. format_code    - 格式化代码（添加注释）

知识点：
  1. 多工具协作的 Agent
  2. 代码沙箱的安全执行
  3. LLM + 工具的代码工作流
"""

import os
import sys
import io
import traceback
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()

print("=" * 60)
print("Day 10 - 练习 3：代码助手 Agent")
print("=" * 60)

# ==============================
# 定义工具
# ==============================

@tool
def run_python_code(code: str) -> str:
    """在安全沙箱中运行 Python 代码并返回输出结果。当用户想运行、测试代码时使用此工具。
    参数: code - 要运行的 Python 代码字符串"""
    # 禁止的危险操作
    dangerous_keywords = [
        "os.system", "subprocess", "shutil.rmtree", "os.remove",
        "os.rmdir", "open(", "__import__", "eval(", "exec(",
        "import os", "import sys", "import shutil",
    ]
    # 注意：这里只是基础的安全检查，生产环境需要用真正的沙箱
    for keyword in dangerous_keywords:
        if keyword in code:
            return f"安全警告：代码包含危险操作 '{keyword}'，已拒绝执行。代码沙箱不允许文件系统操作和系统命令调用。"

    # 重定向标准输出，捕获代码的打印输出
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redirected_output = io.StringIO()
    redirected_error = io.StringIO()
    sys.stdout = redirected_output
    sys.stderr = redirected_error

    try:
        # 使用受限的全局命名空间执行代码
        safe_globals = {
            "__builtins__": {
                "print": print, "range": range, "len": len, "str": str,
                "int": int, "float": float, "list": list, "dict": dict,
                "tuple": tuple, "set": set, "bool": bool, "type": type,
                "isinstance": isinstance, "enumerate": enumerate,
                "zip": zip, "map": map, "filter": filter, "sorted": sorted,
                "reversed": reversed, "sum": sum, "min": min, "max": max,
                "abs": abs, "round": round, "pow": pow, "divmod": divmod,
                "any": any, "all": all, "True": True, "False": False,
                "None": None, "Exception": Exception, "ValueError": ValueError,
                "TypeError": TypeError, "IndexError": IndexError,
                "KeyError": KeyError, "ZeroDivisionError": ZeroDivisionError,
            },
            "math": __import__("math"),
            "datetime": __import__("datetime"),
        }
        exec(code, safe_globals)
        stdout_output = redirected_output.getvalue()
        stderr_output = redirected_error.getvalue()

        if stderr_output:
            return f"运行完成（有警告）：\n{stdout_output}\n警告/错误：{stderr_output}"
        elif stdout_output:
            return f"运行成功：\n{stdout_output}"
        else:
            return "运行成功（无输出）"
    except Exception as e:
        error_msg = traceback.format_exc()
        return f"运行失败：\n{error_msg}"
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

@tool
def explain_code(code: str) -> str:
    """解释一段 Python 代码的含义。当用户不理解某段代码时使用此工具。
    参数: code - 要解释的 Python 代码"""
    lines = code.strip().split("\n")
    analysis = []
    analysis.append(f"代码共 {len(lines)} 行")
    # 分析代码结构
    has_function = any("def " in line for line in lines)
    has_class = any("class " in line for line in lines)
    has_loop = any("for " in line or "while " in line for line in lines)
    has_condition = any("if " in line for line in lines)
    has_import = any("import " in line for line in lines)
    has_list_comp = any("[" in line and "for" in line and "in" in line for line in lines)

    structures = []
    if has_import:
        structures.append("导入模块")
    if has_class:
        structures.append("定义类")
    if has_function:
        structures.append("定义函数")
    if has_loop:
        structures.append("循环结构")
    if has_condition:
        structures.append("条件判断")
    if has_list_comp:
        structures.append("列表推导式")

    analysis.append("代码结构：" + "、".join(structures) if structures else "简单表达式")
    return "\n".join(analysis)

@tool
def format_code_with_comments(code: str) -> str:
    """为代码添加中文注释，帮助理解代码。当用户希望给代码加注释时使用此工具。
    参数: code - 要添加注释的 Python 代码"""
    lines = code.strip().split("\n")
    commented = []
    for line in lines:
        stripped = line.strip()
        # 根据代码内容添加简单注释
        if stripped.startswith("import ") or stripped.startswith("from "):
            commented.append(line + "  # 导入模块")
        elif stripped.startswith("def "):
            func_name = stripped.split("(")[0].replace("def ", "")
            commented.append(line + f"  # 定义函数 {func_name}")
        elif stripped.startswith("class "):
            class_name = stripped.split("(")[0].split(":")[0].replace("class ", "")
            commented.append(line + f"  # 定义类 {class_name}")
        elif stripped.startswith("for "):
            commented.append(line + "  # 循环")
        elif stripped.startswith("if "):
            commented.append(line + "  # 条件判断")
        elif stripped.startswith("return "):
            commented.append(line + "  # 返回结果")
        elif stripped.startswith("print("):
            commented.append(line + "  # 打印输出")
        else:
            commented.append(line)
    return "\n".join(commented)

@tool
def generate_snippet(language: str, description: str) -> str:
    """根据描述生成代码片段。当用户需要生成代码时使用此工具。
    参数: language - 编程语言（如 python）, description - 代码功能描述"""
    # 预设的代码片段库
    snippets = {
        ("python", "排序"): "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr\n\nresult = bubble_sort([64, 34, 25, 12, 22, 11, 90])\nprint(result)",
        ("python", "斐波那契"): "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\nfor i in range(10):\n    print(fibonacci(i), end=' ')",
        ("python", "读文件"): "def read_file(filepath):\n    try:\n        with open(filepath, 'r', encoding='utf-8') as f:\n            return f.read()\n    except FileNotFoundError:\n        return '文件不存在'\n    except Exception as e:\n        return f'读取错误：{e}'",
        ("python", "列表去重"): "def remove_duplicates(lst):\n    return list(dict.fromkeys(lst))\n\noriginal = [1, 2, 2, 3, 3, 3, 4, 5, 5]\nresult = remove_duplicates(original)\nprint(f'原列表：{original}')\nprint(f'去重后：{result}')",
        ("python", "九九乘法表"): "for i in range(1, 10):\n    for j in range(1, i + 1):\n        print(f'{j}x{i}={i*j}', end='\\t')\n    print()",
        ("python", "猜数字"): "import random\n\nsecret = random.randint(1, 100)\nattempts = 0\n\nprint('猜数字游戏！范围 1-100')\nwhile True:\n    guess = int(input('请输入你的猜测：'))\n    attempts += 1\n    if guess < secret:\n        print('太小了！')\n    elif guess > secret:\n        print('太大了！')\n    else:\n        print(f'恭喜！你用了 {attempts} 次猜对了！')\n        break",
    }
    # 查找匹配的代码片段
    for (lang, keyword), code in snippets.items():
        if lang == language.lower() and keyword in description:
            return f"生成的 {language} 代码（{description}）：\n\n{code}"
    return f"暂无预设的 {language} '{description}' 代码片段。请尝试：排序、斐波那契、读文件、列表去重、九九乘法表、猜数字"

tools = [run_python_code, explain_code, format_code_with_comments, generate_snippet]

# ==============================
# Agent 循环
# ==============================

system_prompt = SystemMessage(content=(
    "你是一个代码助手 Agent，专门帮助用户编写、理解和运行 Python 代码。\n"
    "你的工具：\n"
    "1. run_python_code - 运行 Python 代码\n"
    "2. explain_code - 解释代码含义\n"
    "3. format_code_with_comments - 给代码加注释\n"
    "4. generate_snippet - 根据描述生成代码片段\n"
    "请根据用户需求选择合适的工具。"
))

def run_agent(user_input: str, max_rounds: int = 5):
    """运行代码助手 Agent"""
    console.print(f"\n[bold]用户: {user_input}[/bold]")
    llm_with_tools = llm.bind_tools(tools)
    messages = [system_prompt, HumanMessage(content=user_input)]

    for round_num in range(max_rounds):
        console.print(f"[dim]--- 第 {round_num + 1} 轮 ---[/dim]")
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            for tc in response.tool_calls:
                tool_name = tc["name"]
                tool_args = tc["args"]
                console.print(f"  [工具] {tool_name}", style="yellow")
                tool_func = next((t for t in tools if t.name == tool_name), None)
                if tool_func:
                    result = tool_func.invoke(tool_args)
                else:
                    result = "未知工具"
                display = result if len(result) < 300 else result[:300] + "..."
                console.print(f"  [结果] {display}", style="green")
                messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
        else:
            console.print(f"\n[bold green]AI: {response.content}[/bold green]")
            return response.content
    return "达到最大调用轮数"

# ==============================
# LLM 实例
# ==============================

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=MODEL_NAME,
    temperature=0.7,
)

# ==============================
# 测试
# ==============================

console.print(Panel.fit("Day 10 - 练习 3：代码助手 Agent", style="bold green"))

# 测试1：生成代码
run_agent("帮我生成一个九九乘法表的 Python 代码")

# 测试2：解释代码
run_agent("帮我解释一下这段代码：\ndef fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)")

# 测试3：运行代码
run_agent("运行这段代码：\nresult = [x**2 for x in range(10)]\nprint(result)")

# 测试4：生成并运行
run_agent("帮我写一个列表去重的函数，然后运行它测试一下")

console.print("\n" + "=" * 60, style="bold green")
console.print("练习 3 完成：代码助手 Agent 构建成功！", style="bold green")
console.print("=" * 60, style="bold green")
