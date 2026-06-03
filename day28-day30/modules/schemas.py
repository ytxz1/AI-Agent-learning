"""Day28-Day30 的数据模型。"""

from __future__ import annotations

from pydantic import BaseModel, Field


class JobTarget(BaseModel):
    """目标岗位。"""

    company: str
    role: str
    city: str
    source: str
    jd_keywords: list[str]
    match_reason: str
    priority: str = Field(description="优先级：high / medium / low。")


class ApplicationRecord(BaseModel):
    """投递记录。"""

    company: str
    role: str
    date: str
    channel: str
    status: str
    next_action: str
    note: str


class InterviewReview(BaseModel):
    """面试复盘记录。"""

    company: str
    role: str
    interview_date: str
    questions: list[str]
    good_points: list[str]
    to_improve: list[str]
    result: str


class SprintCheckItem(BaseModel):
    """冲刺检查项。"""

    title: str
    done: bool
    suggestion: str


if __name__ == "__main__":
    # 练习题答案 1：
    # 如何创建一条投递记录？
    # 如何添加：传入公司、岗位、日期、渠道、状态、下一步行动和备注。
    record = ApplicationRecord(
        company="示例公司",
        role="AI Agent 实习生",
        date="2026-06-03",
        channel="Boss 直聘",
        status="已投递",
        next_action="2 天后跟进",
        note="重点突出 FastAPI 和 Agent API 项目。",
    )
    print("练习题答案 1：投递记录创建成功")
    print(record.model_dump())
