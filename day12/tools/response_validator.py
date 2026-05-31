"""Validation helpers for structured output."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from schemas.output_schema import OutputSchema


@dataclass
class ValidationResult:
    ok: bool
    errors: List[str]


def _type_matches(value: Any, field_type: str) -> bool:
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
    errors: List[str] = []
    for field in schema.fields:
        if field.required and field.name not in payload:
            errors.append(f"Missing required field: {field.name}")
            continue
        if field.name not in payload:
            continue
        value = payload[field.name]
        if not _type_matches(value, field.field_type):
            errors.append(
                f"Field type mismatch for {field.name}: expected {field.field_type}, got {type(value).__name__}"
            )
    return ValidationResult(ok=not errors, errors=errors)

