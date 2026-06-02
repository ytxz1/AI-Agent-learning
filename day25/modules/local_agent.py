"""本地模拟 Agent。

Day25 的重点是前端界面，所以不能强制要求你必须先启动后端。
这个 LocalAgent 用来在没有后端 API 时提供本地回答。

它的作用不是替代大模型，而是保证页面可以完整跑通：
- 输入问题；
- 得到回答；
- 展示来源；
- 展示使用过的工具；
- 保存聊天记录。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


DAY25_DIR = Path(__file__).resolve().parents[1]
if str(DAY25_DIR) not in sys.path:
    sys.path.insert(0, str(DAY25_DIR))

try:
    from .schemas import ChatResponse
except ImportError:
    from schemas import ChatResponse


class LocalAgent:
    """本地模拟 Agent 类。"""

    def answer(self, question: str) -> ChatResponse:
        """根据用户问题生成本地回答。"""

        clean_question = question.strip()
        if not clean_question:
            return ChatResponse(
                answer="你还没有输入问题。请先在输入框里写一个问题。",
                source="local",
                used_tools=["input_checker"],
            )

        used_tools: list[str] = []
        answer_parts = [
            "这是 Day25 本地前端演示 Agent 的回答。",
            f"你刚才的问题是：{clean_question}",
        ]

        if "streamlit" in clean_question.lower() or "前端" in clean_question:
            used_tools.append("frontend_hint")
            answer_parts.append(
                "Day25 的重点是用 Streamlit 把后端能力做成可交互的 Web 页面。"
            )

        expression = self._extract_math_expression(clean_question)
        if expression:
            used_tools.append("calculator")
            answer_parts.append(f"我检测到一个简单表达式：{expression}")
            answer_parts.append(f"计算结果：{self._safe_calculate(expression)}")

        if not used_tools:
            used_tools.append("study_summary")
            answer_parts.append(
                "建议你先运行 01-05 的练习脚本，再用 streamlit run app.py 打开页面。"
            )

        return ChatResponse(
            answer="\n".join(answer_parts),
            source="local",
            used_tools=used_tools,
        )

    def _extract_math_expression(self, text: str) -> str | None:
        """提取简单数学表达式。"""

        if not any(char in text for char in ["+", "-", "*", "/"]):
            return None

        match = re.search(r"[-+*/().\d\s]{3,}", text)
        if not match:
            return None

        expression = match.group(0).strip()
        return expression if any(char.isdigit() for char in expression) else None

    def _safe_calculate(self, expression: str) -> str:
        """只计算简单表达式。

        这里为了教学简洁使用 eval，但先用正则限制了字符范围。
        真实项目中建议使用更严格的 AST 解析方式。
        """

        if not re.fullmatch(r"[-+*/().\d\s]+", expression):
            return "表达式包含不允许的字符，已拒绝计算。"

        try:
            return str(eval(expression, {"__builtins__": {}}, {}))
        except Exception as exc:
            return f"计算失败：{exc}"


if __name__ == "__main__":
    # 练习题答案 2：
    # 如何不打开网页，直接测试本地 Agent？
    # 如何添加：创建 LocalAgent，然后调用 answer()。
    agent = LocalAgent()
    response = agent.answer("Day25 前端页面要学什么？")
    print("练习题答案 2：LocalAgent 调用成功")
    print(response.model_dump())
