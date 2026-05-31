"""结构化输出校验工具。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from schemas.output_schema import OutputSchema


@dataclass
class ValidationResult:
    """校验结果。"""

    ok: bool
    errors: List[str]


def _type_matches(value: Any, field_type: str) -> bool:
    """检查值的类型是否符合 schema 要求。"""
    if field_type == "string":
        return isinstance(value, str)
    if field_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if field_type == "boolean":
        return isinstance(value, bool)
    if field_type == "array[string]":
        return isinstance(value, list) and all(isinstance(item, str) for item in value)
    if field_type == "object":
        return isinstance(value, dict)
    return True


def validate_payload(schema: OutputSchema, payload: Dict[str, Any]) -> ValidationResult:
    """根据 schema 校验模型输出。

    解析成功不代表内容一定对，所以这里再做一层字段和类型检查。
    """
    errors: List[str] = []

    for field in schema.fields:
        # 必填字段缺失，直接报错。
        if field.required and field.name not in payload:
            errors.append(f"缺少必填字段：{field.name}")
            continue

        if field.name not in payload:
            continue

        value = payload[field.name]
        if not _type_matches(value, field.field_type):
            errors.append(
                f"字段类型不匹配：{field.name}，期望 {field.field_type}，实际是 {type(value).__name__}"
            )

    return ValidationResult(ok=not errors, errors=errors)
