"""Day27 的数据模型。

这里的数据模型服务于“简历和面试准备”：
- ProjectProfile 表示项目素材；
- ResumeBullet 表示简历 bullet；
- InterviewQuestion 表示面试题；
- MockFeedback 表示模拟面试反馈。
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Challenge(BaseModel):
    """项目中遇到的问题和解决方案。"""

    problem: str
    solution: str


class ProjectProfile(BaseModel):
    """项目经历素材。"""

    project_name: str
    role: str
    duration: str
    background: str
    features: list[str]
    tech_stack: list[str]
    highlights: list[str]
    challenges: list[Challenge]
    results: list[str]


class ResumeBullet(BaseModel):
    """简历项目经历中的一条 bullet。"""

    content: str
    focus: str = Field(description="这条 bullet 突出的能力。")


class InterviewQuestion(BaseModel):
    """面试题。"""

    category: str
    question: str
    answer_hint: str


class MockFeedback(BaseModel):
    """模拟面试反馈。"""

    question: str
    answer: str
    score: int = Field(ge=0, le=100)
    strengths: list[str]
    improvements: list[str]
    polished_answer: str


if __name__ == "__main__":
    # 练习题答案 1：
    # 如何创建一条简历 bullet？
    # 如何添加：传入 content 和 focus。
    bullet = ResumeBullet(
        content="使用 FastAPI 将 Agent 能力封装为 REST API，支持问答、流式响应和健康检查。",
        focus="后端接口化能力",
    )
    print("练习题答案 1：ResumeBullet 创建成功")
    print(bullet.model_dump())
