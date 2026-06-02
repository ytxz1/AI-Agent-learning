"""Day23 的 Pydantic 数据模型。

API 项目中，数据模型就是接口契约。
它会告诉 FastAPI：
- 请求体应该有哪些字段；
- 字段类型是什么；
- 字段是否必填；
- 响应应该返回什么结构；
- 自动文档应该如何展示。
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    """Agent 普通问答接口的请求模型。"""

    question: str = Field(
        ...,
        min_length=1,
        description="用户问题，不能为空。",
        examples=["Day23 主要学习什么？"],
    )
    use_tools: bool = Field(
        default=True,
        description="是否允许 Agent 使用本地工具。",
    )
    stream: bool = Field(
        default=False,
        description="是否希望流式输出。普通 /agent/chat 接口会忽略这个字段。",
    )


class AgentResponse(BaseModel):
    """Agent 普通问答接口的响应模型。"""

    answer: str
    source: str = Field(description="回答来源：openai 或 local-fallback。")
    used_tools: list[str] = Field(default_factory=list, description="本次回答使用过的工具名称。")


class StreamChunk(BaseModel):
    """流式接口中每个片段的数据结构。"""

    delta: str
    done: bool = False


class ToolResult(BaseModel):
    """工具调用结果模型。"""

    tool_name: str
    result: str


class HealthStatus(BaseModel):
    """健康检查响应模型。"""

    status: str
    app_name: str
    version: str
    api_prefix: str


class Message(BaseModel):
    """通用消息响应模型。"""

    message: str


class ErrorResponse(BaseModel):
    """统一错误响应模型。"""

    error: str
    detail: str


if __name__ == "__main__":
    # 练习题答案 1：
    # 如何手动创建一个 AgentRequest？
    # 如何添加：传入 question，其他字段可以使用默认值。
    request = AgentRequest(question="请介绍 Day23 的任务")
    print("练习题答案 1：AgentRequest 创建成功")
    print(request.model_dump())
