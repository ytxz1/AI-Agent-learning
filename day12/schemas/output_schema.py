"""结构化输出的字段定义与提示词生成。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class SchemaField:
    """表示一个输出字段。"""

    name: str
    field_type: str
    required: bool = True
    description: str = ""
    default: Any = None


@dataclass
class OutputSchema:
    """表示一份完整的输出结构。"""

    name: str
    description: str
    fields: List[SchemaField] = field(default_factory=list)

    def field_names(self) -> List[str]:
        """返回字段名列表，方便调试。"""
        return [item.name for item in self.fields]

    def to_prompt_block(self) -> str:
        """把 schema 转成提示词文本，传给模型。"""
        lines = [
            f"Schema 名称：{self.name}",
            f"Schema 说明：{self.description}",
            "字段定义：",
        ]
        for item in self.fields:
            required_text = "必填" if item.required else "可选"
            desc_text = f"；说明：{item.description}" if item.description else ""
            default_text = f"；默认值：{item.default!r}" if item.default is not None else ""
            lines.append(f"- {item.name}（类型：{item.field_type}，{required_text}）{desc_text}{default_text}")
        return "\n".join(lines)


def build_intent_schema() -> OutputSchema:
    """构建“意图识别” schema。"""
    return OutputSchema(
        name="intent_classification",
        description="用于识别用户意图并抽取几个关键字段。",
        fields=[
            SchemaField("intent", "string", True, "用户的主要意图，例如问答、翻译、总结、抽取。"),
            SchemaField("confidence", "number", True, "置信度，范围 0 到 1。"),
            SchemaField("entities", "array[string]", True, "用户提到的重要实体。"),
            SchemaField("need_tool", "boolean", True, "是否需要调用外部工具。"),
        ],
    )


def build_extraction_schema() -> OutputSchema:
    """构建“信息抽取” schema。"""
    return OutputSchema(
        name="information_extraction",
        description="从一小段文本中抽取结构化信息。",
        fields=[
            SchemaField("title", "string", True, "文本的简短标题。"),
            SchemaField("summary", "string", True, "一句话摘要。"),
            SchemaField("keywords", "array[string]", True, "三个到五个关键词。"),
            SchemaField("category", "string", True, "一个简单的分类标签。"),
        ],
    )


def build_resume_schema() -> OutputSchema:
    """构建“简历抽取” schema。"""
    return OutputSchema(
        name="resume_extraction",
        description="抽取简历里的基础信息。",
        fields=[
            SchemaField("name", "string", True, "姓名。"),
            SchemaField("education", "string", True, "学历或学校。"),
            SchemaField("skills", "array[string]", True, "技能列表。"),
            SchemaField("experience_years", "number", False, "估计的工作年限。", 0),
        ],
    )
