"""练习 05：模拟面试。

目标：
1. 选择一个常见问题；
2. 给出一段回答；
3. 使用 MockInterviewer 评分；
4. 写入 output/mock_interview_feedback.md。
"""

from __future__ import annotations

from rich.console import Console

from modules.mock_interviewer import MockInterviewer
from modules.report_writer import write_json, write_markdown


console = Console()


def main() -> None:
    """运行模拟面试。"""

    console.rule("[bold green]练习 05：模拟面试")

    question = "请介绍一下你这个 AI Agent 项目。"
    answer = (
        "我完成了一个 AI Agent 学习项目，项目目标是把 AI 能力从脚本做成可以展示的产品雏形。"
        "我使用 FastAPI 封装 API，使用 Streamlit 做前端页面，使用 Docker 准备部署。"
        "项目中遇到的问题是没有 API Key 或网络异常时无法演示，所以我设计了本地 fallback。"
        "最终结果是完成了从后端接口、部署配置到前端页面的完整链路。"
    )

    feedback = MockInterviewer().evaluate(question, answer)

    md_content = f"""# 模拟面试反馈

## 问题

{feedback.question}

## 我的回答

{feedback.answer}

## 评分

{feedback.score}/100

## 优点

{chr(10).join(f"- {item}" for item in feedback.strengths)}

## 需要改进

{chr(10).join(f"- {item}" for item in feedback.improvements)}

## 优化建议

{feedback.polished_answer}
"""

    md_path = write_markdown("mock_interview_feedback.md", md_content)
    json_path = write_json("mock_interview_feedback.json", feedback.model_dump())

    console.print("评分：", feedback.score)
    console.print("Markdown 反馈：", md_path)
    console.print("JSON 反馈：", json_path)
    console.print(feedback.model_dump())

    # 练习题答案：
    # 题目：模拟面试回答最重要的结构是什么？
    # 如何添加：
    # 使用“背景 - 行动 - 问题 - 解决 - 结果 - 收获”的结构回答。


if __name__ == "__main__":
    main()
