"""Day26 的数据模型。

这里使用 Pydantic 是为了让检查结果结构稳定。
例如：
- 每个文件用 ProjectFile 表示；
- 每个检查项用 CheckItem 表示；
- 最终 GitHub 优化报告用 GitHubReport 表示。
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ProjectFile(BaseModel):
    """项目文件信息。"""

    path: str
    suffix: str
    size: int
    description: str = ""


class CheckItem(BaseModel):
    """单个检查项。"""

    title: str
    passed: bool
    detail: str
    suggestion: str


class GitHubReport(BaseModel):
    """GitHub 优化报告。"""

    project_name: str
    target_path: str
    score: int = Field(ge=0, le=100)
    checks: list[CheckItem]
    highlights: list[str]
    next_actions: list[str]


class ScreenshotPlan(BaseModel):
    """截图计划。"""

    title: str
    target_page: str
    purpose: str
    file_name: str


if __name__ == "__main__":
    # 练习题答案 1：
    # 如何创建一个检查项？
    # 如何添加：传入 title、passed、detail、suggestion。
    item = CheckItem(
        title="README 是否存在",
        passed=True,
        detail="项目中找到了 README.md。",
        suggestion="继续补充运行截图和项目亮点。",
    )
    print("练习题答案 1：CheckItem 创建成功")
    print(item.model_dump())
