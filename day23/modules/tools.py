"""Agent 可以调用的本地工具。

Day23 还不是复杂 Agent 框架，所以我们先做几个简单但实用的工具：
- 获取当前学习计划说明；
- 根据关键词搜索本地知识库；
- 做一个简单计算器。

这些工具会被 AgentService 调用，用来模拟“Agent 使用工具回答问题”的过程。
"""

from __future__ import annotations

import ast
import operator
import re
import sys
from pathlib import Path


DAY23_DIR = Path(__file__).resolve().parents[1]
if str(DAY23_DIR) not in sys.path:
    sys.path.insert(0, str(DAY23_DIR))

from config import KNOWLEDGE_FILE

try:
    from .exceptions import ToolExecutionError
except ImportError:
    from exceptions import ToolExecutionError


def read_learning_plan() -> str:
    """读取 Day23 知识库内容。"""

    if not KNOWLEDGE_FILE.exists():
        return "知识库文件不存在，请检查 data/agent_knowledge.txt。"
    return KNOWLEDGE_FILE.read_text(encoding="utf-8")


def search_knowledge(keyword: str) -> str:
    """在本地知识库中按关键词搜索相关行。"""

    content = read_learning_plan()
    matched_lines = [
        line.strip()
        for line in content.splitlines()
        if keyword.lower() in line.lower() and line.strip()
    ]

    if not matched_lines:
        return f"没有在 Day23 知识库中找到关键词：{keyword}"

    return "\n".join(matched_lines)


def safe_calculate(expression: str) -> str:
    """安全计算简单数学表达式。

    这里只允许加减乘除和括号，避免执行危险代码。
    """

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
    }

    def evaluate(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](evaluate(node.left), evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](evaluate(node.operand))
        raise ToolExecutionError("计算器只支持数字、加减乘除和括号")

    try:
        parsed = ast.parse(expression, mode="eval")
        result = evaluate(parsed)
    except AgentAPIError:
        raise
    except Exception as exc:
        raise ToolExecutionError(f"计算表达式失败：{exc}") from exc

    return f"{expression} = {result:g}"


def extract_math_expression(text: str) -> str | None:
    """从用户问题中提取简单数学表达式。"""

    # 只有出现真正的运算符时，才认为用户可能想计算。
    # 这样可以避免把 “Day23” 里的 23 误识别成数学表达式。
    if not any(operator_char in text for operator_char in ["+", "-", "*", "/"]):
        return None

    match = re.search(r"[-+*/().\d\s]{3,}", text)
    if not match:
        return None

    expression = match.group(0).strip()
    if any(char.isdigit() for char in expression):
        return expression
    return None


# 这里放在底部，避免 safe_calculate 里引用异常类时循环导入。
try:
    from .exceptions import AgentAPIError
except ImportError:
    from exceptions import AgentAPIError


if __name__ == "__main__":
    # 练习题答案 3：
    # 如何直接测试工具函数？
    # 如何添加：调用 read_learning_plan、search_knowledge、safe_calculate。
    print("练习题答案 3：读取知识库前 80 个字符")
    print(read_learning_plan()[:80])
    print("\n搜索关键词 API：")
    print(search_knowledge("API"))
    print("\n计算器：")
    print(safe_calculate("3 * (4 + 2)"))
