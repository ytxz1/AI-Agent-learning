"""练习 01：项目经历提炼。

目标：
1. 读取项目经历素材；
2. 生成简历项目 bullet；
3. 写入 output/resume_project.md。
"""

from __future__ import annotations

from rich.console import Console

from modules.profile_loader import load_project_profile
from modules.report_writer import write_markdown
from modules.resume_builder import ResumeBuilder


console = Console()


def main() -> None:
    """运行项目经历提炼。"""

    console.rule("[bold green]练习 01：项目经历提炼")
    profile = load_project_profile()
    builder = ResumeBuilder(profile)
    resume_section = builder.build_resume_section()
    output_path = write_markdown("resume_project.md", resume_section)

    console.print(resume_section)
    console.print("\n已写入：", output_path)

    # 练习题答案：
    # 题目：简历项目经历不要写成流水账，应该突出什么？
    # 如何添加：
    # 应该突出技术、动作、问题、结果和能力，而不是简单列出“我学习了很多内容”。


if __name__ == "__main__":
    main()
