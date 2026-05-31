"""Schema definitions for structured output tasks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class SchemaField:
    name: str
    field_type: str
    required: bool = True
    description: str = ""
    default: Any = None


@dataclass
class OutputSchema:
    name: str
    description: str
    fields: List[SchemaField] = field(default_factory=list)

    def field_names(self) -> List[str]:
        return [field.name for field in self.fields]

    def to_prompt_block(self) -> str:
        lines = [f"Schema name: {self.name}", f"Description: {self.description}", "Fields:"]
        for item in self.fields:
            req = "required" if item.required else "optional"
            desc = f" - {item.description}" if item.description else ""
            default = f" default={item.default!r}" if item.default is not None else ""
            lines.append(f"- {item.name} ({item.field_type}, {req}){default}{desc}")
        return "\n".join(lines)


def build_intent_schema() -> OutputSchema:
    return OutputSchema(
        name="intent_classification",
        description="Classify user intent and extract a few useful fields.",
        fields=[
            SchemaField("intent", "string", True, "Main user intent, such as question, translate, summarize, extract."),
            SchemaField("confidence", "number", True, "Confidence score from 0 to 1."),
            SchemaField("entities", "array[string]", True, "Important entities mentioned by the user."),
            SchemaField("need_tool", "boolean", True, "Whether external tool is needed."),
        ],
    )


def build_extraction_schema() -> OutputSchema:
    return OutputSchema(
        name="information_extraction",
        description="Extract structured information from a short text.",
        fields=[
            SchemaField("title", "string", True, "Short title of the input text."),
            SchemaField("summary", "string", True, "One-sentence summary."),
            SchemaField("keywords", "array[string]", True, "Three to five keywords."),
            SchemaField("category", "string", True, "A simple category label."),
        ],
    )


def build_resume_schema() -> OutputSchema:
    return OutputSchema(
        name="resume_extraction",
        description="Extract basic resume information.",
        fields=[
            SchemaField("name", "string", True, "Person name."),
            SchemaField("education", "string", True, "Education level or school."),
            SchemaField("skills", "array[string]", True, "List of skills."),
            SchemaField("experience_years", "number", False, "Estimated years of experience.", 0),
        ],
    )

