"""Agent 核心服务。

这个文件负责把“用户问题”转换成“Agent 回答”。

它支持两种模式：
1. 如果配置了 OPENAI_API_KEY，优先尝试调用 OpenAI；
2. 如果没有配置 API Key，或者在线调用失败，自动使用本地模拟回答。

这样设计的原因：
- 你有 Key 时，可以体验真实大模型 API；
- 你没有 Key 时，项目仍然能完整跑通；
- 网络或模型配置出问题时，不影响 Day23 学习 FastAPI 接口化。
"""

from __future__ import annotations

import sys
import time
from collections.abc import Generator
from pathlib import Path


DAY23_DIR = Path(__file__).resolve().parents[1]
if str(DAY23_DIR) not in sys.path:
    sys.path.insert(0, str(DAY23_DIR))

from config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL

try:
    from .exceptions import EmptyQuestionError
    from .schemas import AgentRequest, AgentResponse
    from .tools import extract_math_expression, read_learning_plan, safe_calculate, search_knowledge
except ImportError:
    from exceptions import EmptyQuestionError
    from schemas import AgentRequest, AgentResponse
    from tools import extract_math_expression, read_learning_plan, safe_calculate, search_knowledge


class AgentService:
    """Agent 服务类。

    路由层只负责接收 HTTP 请求，真正的业务逻辑放在这里。
    这样做可以让代码更清楚，也方便后续测试。
    """

    def __init__(self) -> None:
        self.has_openai_key = bool(OPENAI_API_KEY)

    def chat(self, request: AgentRequest) -> AgentResponse:
        """普通问答入口。"""

        question = request.question.strip()
        if not question:
            raise EmptyQuestionError("问题不能为空，请输入一个有效问题。")

        if self.has_openai_key:
            try:
                return self._chat_with_openai(request)
            except Exception as exc:
                # 在线调用失败时，降级到本地回答，保证学习项目可运行。
                fallback = self._chat_locally(question, request.use_tools)
                fallback.answer = f"{fallback.answer}\n\n注意：在线模型调用失败，已使用本地备用回答。错误信息：{exc}"
                return fallback

        return self._chat_locally(question, request.use_tools)

    def stream_chat(self, request: AgentRequest) -> Generator[str, None, None]:
        """流式问答入口。

        为了让学习脚本稳定，这里先生成完整回答，再按字符分片返回。
        真实项目中可以直接转发大模型的 streaming chunks。
        """

        response = self.chat(request)
        for char in response.answer:
            yield char
            time.sleep(0.005)

    def _chat_with_openai(self, request: AgentRequest) -> AgentResponse:
        """调用 OpenAI 生成回答。"""

        from openai import OpenAI

        client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
        )

        tool_context = ""
        used_tools: list[str] = []
        if request.use_tools:
            tool_context = read_learning_plan()
            used_tools.append("read_learning_plan")

        completion = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "你是一个中文 AI Agent 学习助手。"
                        "回答要清楚、具体、适合初学者。"
                    ),
                },
                {
                    "role": "user",
                    "content": f"本地知识库：\n{tool_context}\n\n用户问题：{request.question}",
                },
            ],
            temperature=0.3,
        )

        answer = completion.choices[0].message.content or "模型没有返回内容。"
        return AgentResponse(answer=answer, source="openai", used_tools=used_tools)

    def _chat_locally(self, question: str, use_tools: bool) -> AgentResponse:
        """本地模拟回答。

        这个函数不是为了假装成大模型，而是为了让你理解：
        Agent API 的外壳、路由、响应结构、流式输出都可以先跑通。
        """

        used_tools: list[str] = []
        answer_parts = [
            "这是 Day23 本地 Agent 的回答。",
            f"你的问题是：{question}",
        ]

        if use_tools:
            math_expression = extract_math_expression(question)
            if math_expression:
                used_tools.append("safe_calculate")
                answer_parts.append(f"计算工具结果：{safe_calculate(math_expression)}")

            if "day23" in question.lower() or "api" in question.lower() or "接口" in question:
                used_tools.append("search_knowledge")
                answer_parts.append("知识库搜索结果：")
                answer_parts.append(search_knowledge("API"))
            else:
                used_tools.append("read_learning_plan")
                answer_parts.append("学习计划摘要：")
                answer_parts.append(read_learning_plan().splitlines()[0])

        answer_parts.append("建议：先运行 01-05 的练习脚本，再用 uvicorn 启动完整 API。")
        return AgentResponse(
            answer="\n".join(answer_parts),
            source="local-fallback",
            used_tools=used_tools,
        )


if __name__ == "__main__":
    # 练习题答案 4：
    # 如何不用启动服务器，直接测试 AgentService？
    # 如何添加：创建 AgentService，然后传入 AgentRequest。
    service = AgentService()
    result = service.chat(AgentRequest(question="Day23 为什么要学习 API？"))
    print("练习题答案 4：AgentService 调用成功")
    print(result.model_dump())
