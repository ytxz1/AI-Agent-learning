"""Day26 GitHub 优化项目模块包。

模块分工：
- schemas.py：检查结果和报告的数据模型；
- project_scanner.py：扫描项目结构；
- readme_reviewer.py：检查 README 完整度；
- github_advisor.py：生成 GitHub 展示建议；
- doc_generator.py：生成展示文档和清单；
- report_writer.py：把报告写入 output 文件夹。
"""

from .github_advisor import GitHubAdvisor
from .project_scanner import ProjectScanner
from .readme_reviewer import ReadmeReviewer
from .schemas import CheckItem, GitHubReport, ProjectFile

__all__ = [
    "GitHubAdvisor",
    "ProjectScanner",
    "ReadmeReviewer",
    "CheckItem",
    "GitHubReport",
    "ProjectFile",
]
