"""学生类模块。

Day 2 会开始学习类和对象。
这里用 Student 类来表示一个学生，并把“求平均分、判断等级”等逻辑封装到类中。
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Student:
    """一个简单的学生对象。"""

    id: int
    name: str
    age: int
    scores: dict[str, float]
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        """从字典创建 Student 对象。"""
        return cls(
            id=int(data["id"]),
            name=str(data["name"]),
            age=int(data["age"]),
            scores=dict(data.get("scores", {})),
            tags=list(data.get("tags", [])),
        )

    def to_dict(self) -> dict:
        """把 Student 对象转换回字典。"""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "scores": self.scores,
            "tags": self.tags,
            "average": self.average_score(),
            "level": self.level(),
        }

    def average_score(self) -> float:
        """计算平均分。"""
        if not self.scores:
            return 0.0
        return round(sum(self.scores.values()) / len(self.scores), 2)

    def level(self) -> str:
        """根据平均分判断等级。"""
        average = self.average_score()
        if average >= 90:
            return "优秀"
        if average >= 80:
            return "良好"
        if average >= 70:
            return "合格"
        if average >= 60:
            return "需加强"
        return "未通过"

    def has_tag(self, tag: str) -> bool:
        """判断学生是否有某个标签。"""
        return tag in set(self.tags)

