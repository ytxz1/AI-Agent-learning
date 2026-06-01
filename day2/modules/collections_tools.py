"""集合、列表、字典练习工具。

这里集中演示 Day 2 的几个重点：
- list 排序
- dict 分组
- set 去重
"""

from __future__ import annotations

from collections import defaultdict

from .student import Student


def sort_students_by_average(students: list[Student], reverse: bool = True) -> list[Student]:
    """按平均分排序学生。"""
    return sorted(students, key=lambda student: student.average_score(), reverse=reverse)


def group_students_by_level(students: list[Student]) -> dict[str, list[str]]:
    """按成绩等级给学生分组。"""
    groups: dict[str, list[str]] = defaultdict(list)
    for student in students:
        groups[student.level()].append(student.name)
    return dict(groups)


def collect_all_tags(students: list[Student]) -> set[str]:
    """收集所有学生标签，并用 set 自动去重。"""
    tags: set[str] = set()
    for student in students:
        tags.update(student.tags)
    return tags


def find_students_by_tag(students: list[Student], tag: str) -> list[Student]:
    """根据标签筛选学生。"""
    return [student for student in students if student.has_tag(tag)]

