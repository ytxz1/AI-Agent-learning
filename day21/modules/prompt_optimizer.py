"""提示词优化模块。

Day 21 的一个目标是“优化提示词”。
这个模块用本地规则检查提示词是否包含角色、上下文、任务、约束和输出格式。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PromptReview:
    """提示词评估结果。"""

    score: int
    strengths: list[str]
    issues: list[str]
    improved_prompt: str


class PromptOptimizer:
    """提示词优化器。"""

    def review(self, prompt: str, task_name: str = "项目任务") -> PromptReview:
        """评估并优化提示词。"""
        strengths: list[str] = []
        issues: list[str] = []
        score = 40

        checks = [
            ("角色", ["你是", "助手", "专家", "Agent"], 12),
            ("上下文", ["上下文", "资料", "文档", "代码"], 12),
            ("任务", ["请", "需要", "目标", "任务"], 12),
            ("约束", ["不要", "必须", "只根据", "如果"], 12),
            ("输出格式", ["JSON", "列表", "步骤", "格式"], 12),
        ]

        for label, keywords, points in checks:
            if any(keyword.lower() in prompt.lower() for keyword in keywords):
                strengths.append(f"包含{label}信息")
                score += points
            else:
                issues.append(f"缺少明确的{label}说明")

        score = min(score, 100)
        improved_prompt = self.build_template(task_name)
        return PromptReview(score=score, strengths=strengths, issues=issues, improved_prompt=improved_prompt)

    def build_template(self, task_name: str) -> str:
        """生成一个更稳的提示词模板。"""
        return (
            f"你是一个严谨的 AI 项目优化助手，当前任务是：{task_name}。\n\n"
            "【上下文】\n"
            "我会提供项目文件、用户需求、现有输出或检索结果。\n\n"
            "【你的任务】\n"
            "1. 先判断当前问题属于提示词、检索、代码、配置还是用户体验。\n"
            "2. 给出最小、安全、可验证的优化建议。\n"
            "3. 如果信息不足，请明确说明缺少什么。\n\n"
            "【约束】\n"
            "1. 不要编造不存在的文件或接口。\n"
            "2. 不要建议破坏性操作。\n"
            "3. 优先保留现有项目结构。\n\n"
            "【输出格式】\n"
            "请按 JSON 输出：objective, diagnosis, changes, validation, risks。"
        )
