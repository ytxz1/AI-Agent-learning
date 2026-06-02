"""Day25 的数据模型。

虽然 Streamlit 前端不像 FastAPI 那样必须写 response_model，
但我们仍然使用 Pydantic 来管理数据结构。

这样做的好处：
- 聊天消息格式稳定；
- API 返回值容易校验；
- README 和代码解释更清楚；
- 后续接入真实后端时更不容易乱。
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """单条聊天消息。"""

    role: str = Field(description="消息角色：user 或 assistant。")
    content: str = Field(description="消息内容。")
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))


class ChatResponse(BaseModel):
    """Agent 回答结构。"""

    answer: str
    source: str = "local"
    used_tools: list[str] = Field(default_factory=list)


class UIStatus(BaseModel):
    """页面状态展示模型。"""

    mode: str
    api_url: str
    message_count: int


if __name__ == "__main__":
    # 练习题答案 1：
    # 如何创建一条聊天消息？
    # 如何添加：传入 role 和 content，created_at 会自动生成。
    message = ChatMessage(role="user", content="请介绍 Day25")
    print("练习题答案 1：ChatMessage 创建成功")
    print(message.model_dump())
