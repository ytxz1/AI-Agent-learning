"""报告写入工具。

Day26 的练习脚本会生成一些 Markdown 报告。
为了避免每个脚本重复写文件逻辑，这里统一封装。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


DAY26_DIR = Path(__file__).resolve().parents[1]
if str(DAY26_DIR) not in sys.path:
    sys.path.insert(0, str(DAY26_DIR))

try:
    from .schemas import GitHubReport
except ImportError:
    from schemas import GitHubReport


OUTPUT_DIR = DAY26_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def write_text_report(file_name: str, content: str) -> Path:
    """写入文本报告。"""

    output_path = OUTPUT_DIR / file_name
    output_path.write_text(content, encoding="utf-8")
    return output_path


def write_github_report(report: GitHubReport) -> tuple[Path, Path]:
    """同时写入 Markdown 和 JSON 版本报告。"""

    markdown_lines = [
        f"# {report.project_name} GitHub 优化报告",
        "",
        f"- 目标路径：`{report.target_path}`",
        f"- 当前评分：**{report.score}/100**",
        "",
        "## 检查结果",
    ]

    for check in report.checks:
        status = "通过" if check.passed else "需要优化"
        markdown_lines.append(f"- {check.title}：{status}")
        markdown_lines.append(f"  - 详情：{check.detail}")
        markdown_lines.append(f"  - 建议：{check.suggestion}")

    markdown_lines.extend(["", "## 项目亮点"])
    markdown_lines.extend([f"- {highlight}" for highlight in report.highlights])
    markdown_lines.extend(["", "## 下一步行动"])
    markdown_lines.extend([f"- {action}" for action in report.next_actions])

    md_path = write_text_report("github_report.md", "\n".join(markdown_lines))
    json_path = OUTPUT_DIR / "github_report.json"
    json_path.write_text(
        json.dumps(report.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return md_path, json_path


if __name__ == "__main__":
    # 练习题答案 6：
    # 如何写入一个简单报告？
    # 如何添加：调用 write_text_report()。
    path = write_text_report("demo_report.md", "# 练习题答案 6\n\n报告写入成功。")
    print("练习题答案 6：报告已写入", path)
