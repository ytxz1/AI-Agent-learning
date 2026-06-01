"""Python 基础能力模块。

这里放 Day 1 反复会用到的小函数：
- 构建个人信息
- 判断成绩等级
- 过滤偶数
- 生成乘法表
- 统计单词
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable


def build_profile(name: str, age: int, skills: list[str]) -> dict:
    """把零散变量组合成一个字典。"""
    return {
        "name": name,
        "age": age,
        "skills": skills,
        "skill_count": len(skills),
        "is_adult": age >= 18,
    }


def format_profile(profile: dict) -> str:
    """把个人信息字典格式化成适合展示的文字。"""
    skills = "、".join(profile.get("skills", [])) or "暂无"
    adult_text = "成年人" if profile.get("is_adult") else "未成年人"
    return (
        f"姓名：{profile.get('name')}\n"
        f"年龄：{profile.get('age')}（{adult_text}）\n"
        f"技能：{skills}\n"
        f"技能数量：{profile.get('skill_count')}"
    )


def calculate_grade(score: float) -> str:
    """根据分数返回等级。"""
    if score < 0 or score > 100:
        return "无效分数"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "E"


def filter_even_numbers(numbers: Iterable[int]) -> list[int]:
    """从数字列表中筛选偶数。"""
    return [number for number in numbers if number % 2 == 0]


def multiplication_table(size: int = 9) -> list[str]:
    """生成乘法表。"""
    rows = []
    for row in range(1, size + 1):
        items = []
        for col in range(1, row + 1):
            items.append(f"{col}x{row}={col * row}")
        rows.append("  ".join(items))
    return rows


def count_words(text: str, top_n: int = 5) -> list[tuple[str, int]]:
    """统计文本中出现最多的英文单词。"""
    words = []
    for raw in text.lower().replace("\n", " ").split(" "):
        word = raw.strip(".,!?;:()[]{}\"'")
        if word:
            words.append(word)
    return Counter(words).most_common(top_n)

