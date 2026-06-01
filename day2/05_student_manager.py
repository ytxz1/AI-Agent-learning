"""Day 2 - 综合小项目：学生成绩管理器。"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from config import OUTPUT_REPORT, STUDENTS_JSON, TEXT_REPORT
from modules.collections_tools import collect_all_tags, group_students_by_level, sort_students_by_average
from modules.json_tools import load_json, save_json
from modules.student import Student


console = Console()


def load_students() -> list[Student]:
    """从 JSON 文件加载学生对象。"""
    return [Student.from_dict(item) for item in load_json(STUDENTS_JSON)]


def build_report(students: list[Student]) -> dict:
    """生成结构化报告。"""
    sorted_students = sort_students_by_average(students)
    return {
        "student_count": len(students),
        "all_tags": sorted(collect_all_tags(students)),
        "groups": group_students_by_level(students),
        "students": [student.to_dict() for student in sorted_students],
    }


def write_text_report(report: dict) -> None:
    """生成一份适合人阅读的文本报告。"""
    lines = [
        "Day 2 学生成绩报告",
        f"学生数量：{report['student_count']}",
        f"所有标签：{', '.join(report['all_tags'])}",
        "",
        "学生排行：",
    ]
    for student in report["students"]:
        lines.append(
            f"- {student['name']}：平均分 {student['average']}，等级 {student['level']}"
        )
    TEXT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    TEXT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    students = load_students()
    report = build_report(students)
    save_json(OUTPUT_REPORT, report)
    write_text_report(report)

    table = Table(title="学生成绩管理器", show_header=True)
    table.add_column("姓名", style="cyan")
    table.add_column("平均分", style="green")
    table.add_column("等级", style="yellow")

    for student in report["students"]:
        table.add_row(student["name"], str(student["average"]), student["level"])

    console.print(table)
    console.print(f"\nJSON 报告：{OUTPUT_REPORT}", style="green")
    console.print(f"文本报告：{TEXT_REPORT}", style="green")


if __name__ == "__main__":
    main()

