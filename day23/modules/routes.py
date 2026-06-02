"""Day23 的 FastAPI 路由。

这里把 Agent 能力包装成 HTTP 接口。

重点接口：
- POST /api/agent/chat：普通 JSON 问答；
- POST /api/agent/stream：流式问答；
- GET /api/health：健康检查；
- GET /api/tools：查看当前可用工具。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import StreamingResponse


DAY23_DIR = Path(__file__).resolve().parents[1]
if str(DAY23_DIR) not in sys.path:
    sys.path.insert(0, str(DAY23_DIR))

from config import API_PREFIX, APP_NAME, APP_VERSION

try:
    from .agent_service import AgentService
    from .schemas import AgentRequest, AgentResponse, HealthStatus, Message
except ImportError:
    from agent_service import AgentService
    from schemas import AgentRequest, AgentResponse, HealthStatus, Message


router = APIRouter(prefix=API_PREFIX, tags=["Agent API"])
agent_service = AgentService()


@router.get("/health", response_model=HealthStatus)
def health_check() -> HealthStatus:
    """健康检查接口。"""

    return HealthStatus(
        status="ok",
        app_name=APP_NAME,
        version=APP_VERSION,
        api_prefix=API_PREFIX,
    )


@router.get("/tools", response_model=list[str])
def list_tools() -> list[str]:
    """查看当前 Agent 可以使用的工具。"""

    return [
        "read_learning_plan",
        "search_knowledge",
        "safe_calculate",
    ]


@router.post("/agent/chat", response_model=AgentResponse)
def chat_with_agent(request: AgentRequest) -> AgentResponse:
    """普通 Agent 问答接口。

    前端或其他系统发送 JSON：
    {
      "question": "Day23 主要学习什么？",
      "use_tools": true
    }
    """

    return agent_service.chat(request)


@router.post("/agent/stream")
def stream_with_agent(request: AgentRequest) -> StreamingResponse:
    """流式 Agent 问答接口。

    这里用 Server-Sent Events 风格返回：
    data: {"delta": "字", "done": false}
    """

    def event_generator():
        for char in agent_service.stream_chat(request):
            payload = json.dumps({"delta": char, "done": False}, ensure_ascii=False)
            yield f"data: {payload}\n\n"

        done_payload = json.dumps({"delta": "", "done": True}, ensure_ascii=False)
        yield f"data: {done_payload}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/agent/example", response_model=Message)
def agent_example() -> Message:
    """给初学者看的调用示例。"""

    return Message(message="请向 POST /api/agent/chat 发送 JSON：{'question': 'Day23 学什么？'}")


if __name__ == "__main__":
    # 练习题答案 5：
    # 如何查看当前路由文件注册了哪些接口？
    # 如何添加：遍历 router.routes，打印 methods 和 path。
    print("练习题答案 5：当前注册的接口如下")
    for route in router.routes:
        methods = ",".join(sorted(route.methods or []))
        print(f"{methods:10s} {route.path}")
