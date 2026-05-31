"""
Day 11 - 练习 4（挑战）：代码助手 Agent

任务：构建一个代码助手 Agent，支持代码生成、解释、运行、审查。

新增内容（标注 [新增]）：
  1. [新增] run_code 工具（安全沙箱执行 Python 代码）
  2. [新增] explain_code 工具（分析代码结构）
  3. [新增] review_code 工具（代码审查，给出改进建议）
  4. [新增] CodeAssistantAgent 类
"""

import os, sys, io, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 11 - 练习 4：代码助手 Agent", style="bold blue")
console.print("=" * 60, style="bold blue")

# [新增] 工具 1：安全运行 Python 代码
@tool
def run_code(code: str) -> str:
    """在安全沙箱中运行 Python 代码并返回输出。当用户想运行、测试代码时使用。
    参数: code - 要运行的 Python 代码字符串"""
    # 危险操作检查
    dangerous = ["os.system", "subprocess", "shutil", "os.remove", "os.rmdir",
                 "__import__", "open(", "import os", "import sys", "import shutil"]
    for kw in dangerous:
        if kw in code:
            return f"安全警告：代码包含危险操作 '{kw}'，已拒绝执行。"

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redirected = io.StringIO()
    sys.stdout = redirected
    sys.stderr = io.StringIO()
    try:
        safe_builtins = {
            "print": print, "range": range, "len": len, "str": str,
            "int": int, "float": float, "list": list, "dict": dict,
            "tuple": tuple, "set": set, "bool": bool, "type": type,
            "isinstance": isinstance, "enumerate": enumerate, "zip": zip,
            "sorted": sorted, "reversed": reversed, "sum": sum,
            "min": min, "max": max, "abs": abs, "round": round,
            "True": True, "False": False, "None": None,
            "Exception": Exception, "ValueError": ValueError,
            "TypeError": TypeError, "IndexError": IndexError,
            "KeyError": KeyError, "ZeroDivisionError": ZeroDivisionError,
        }
        exec(code, {"__builtins__": safe_builtins, "math": __import__("math")})
        output = redirected.getvalue()
        return f"运行成功：\n{output}" if output else "运行成功（无输出）"
    except Exception:
        return f"运行失败：\n{traceback.format_exc()}"
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

# [新增] 工具 2：分析代码结构
@tool
def explain_code(code: str) -> str:
    """分析并解释一段 Python 代码的结构和含义。当用户不理解某段代码时使用。
    参数: code - 要解释的 Python 代码"""
    lines = code.strip().split("\n")
    analysis = [f"代码共 {len(lines)} 行"]
    structures = []
    if any("import " in l for l in lines):
        structures.append("导入模块")
    if any("class " in l for l in lines):
        structures.append("定义类")
    if any("def " in l for l in lines):
        structures.append("定义函数")
    if any("for " in l or "while " in l for l in lines):
        structures.append("循环结构")
    if any("if " in l for l in lines):
        structures.append("条件判断")
    if any("[" in l and "for" in l and "in" in l for l in lines):
        structures.append("列表推导式")
    if any("try:" in l for l in lines):
        structures.append("异常处理")
    if any("lambda " in l for l in lines):
        structures.append("Lambda 表达式")
    analysis.append("包含结构：" + "、".join(structures) if structures else "简单表达式")

    # 提取函数名
    funcs = [l.strip().split("(")[0].replace("def ", "") for l in lines if l.strip().startswith("def ")]
    if funcs:
        analysis.append("定义的函数：" + ", ".join(funcs))
    return "\n".join(analysis)

# [新增] 工具 3：代码审查
@tool
def review_code(code: str) -> str:
    """审查代码并给出改进建议。当用户想优化代码时使用。
    参数: code - 要审查的 Python 代码"""
    suggestions = []
    lines = code.strip().split("\n")

    # 检查常见问题
    if not any(l.strip().startswith('"""') or l.strip().startswith("'''") for l in lines[:3]):
        suggestions.append("建议添加模块级 docstring 文档字符串")
    for i, line in enumerate(lines, 1):
        if "eval(" in line and "safe" not in line.lower():
            suggestions.append(f"第 {i} 行：使用 eval() 有安全风险，建议用 ast.literal_eval() 替代")
        if len(line) > 100:
            suggestions.append(f"第 {i} 行：行长度超过 100 字符，建议拆分")
        if line.strip().startswith("#") is False and "=" in line and "==" not in line:
            parts = line.split("=")
            if len(parts) == 2 and parts[0].strip() == parts[0].strip().lower():
                pass  # 合理的变量名
    if not any("try" in l for l in lines):
        if any("open(" in l or "request" in l for l in lines):
            suggestions.append("建议添加异常处理（try/except）")
    if not suggestions:
        suggestions.append("代码结构良好，暂无改进建议。")
    return "代码审查结果：\n" + "\n".join(f"  - {s}" for s in suggestions)

all_tools = [run_code, explain_code, review_code]
tool_map = {t.name: t for t in all_tools}

llm = ChatOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, model=MODEL_NAME, temperature=0.7)

# [新增] 代码助手 Agent 类
class CodeAssistantAgent:
    """代码助手 Agent：生成、解释、运行、审查代码"""

    def __init__(self):
        self.system_prompt = SystemMessage(content=(
            "你是一个代码助手 Agent，专门帮助用户编写、理解和运行 Python 代码。\n"
            "工具：run_code（运行代码）、explain_code（解释代码）、review_code（审查代码）\n"
            "根据用户需求选择合适的工具。如果用户想运行代码，先运行再解释结果。"
        ))
        self.messages = [self.system_prompt]
        self.llm = llm.bind_tools(all_tools)

    def chat(self, user_input, max_rounds=5):
        self.messages.append(HumanMessage(content=user_input))
        for _ in range(max_rounds):
            response = self.llm.invoke(self.messages)
            self.messages.append(response)
            if response.tool_calls:
                for tc in response.tool_calls:
                    console.print(f"  [工具] {tc['name']}", style="yellow")
                    result = tool_map[tc["name"]].invoke(tc["args"]) if tc["name"] in tool_map else "未知工具"
                    display = result if len(result) < 200 else result[:200] + "..."
                    console.print(f"  [结果] {display}", style="green")
                    self.messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
            else:
                return response.content
        return "达到最大推理轮数"

# 演示
console.print("\n[bold cyan]代码助手 Agent 演示[/bold cyan]")
agent = CodeAssistantAgent()

# 测试1：运行代码
console.print("\n[bold]测试 1：运行代码[/bold]")
r = agent.chat("运行这段代码：\nresult = [x**2 for x in range(10)]\nprint(result)")
console.print(f"Agent：{r}", style="bold green")

# 测试2：解释代码
console.print("\n[bold]测试 2：解释代码[/bold]")
r = agent.chat("解释一下这段代码：\ndef fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)")
console.print(f"Agent：{r}", style="bold green")

# 测试3：审查代码
console.print("\n[bold]测试 3：审查代码[/bold]")
r = agent.chat("帮我审查一下这段代码：\ndef calc(x):\n    return eval(x)")
console.print(f"Agent：{r}", style="bold green")

# 测试4：生成并运行
console.print("\n[bold]测试 4：生成并运行[/bold]")
r = agent.chat("写一个九九乘法表的代码，然后运行它")
console.print(f"Agent：{r}", style="bold green")

console.print("\n练习 4 完成！", style="bold green")
