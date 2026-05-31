"""Structured output workflow used by the Day 12 demo."""

from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Optional

from config import MAX_RETRY
from parsers.json_parser import JsonOutputParser
from schemas.output_schema import (
    OutputSchema,
    build_extraction_schema,
    build_intent_schema,
    build_resume_schema,
)
from tools.response_validator import validate_payload
from .mock_model import MockStructuredModel


class StructuredOutputWorkflow:
    def __init__(self, max_retry: int = MAX_RETRY):
        self.max_retry = max_retry
        self.model = MockStructuredModel()
        self.parser = JsonOutputParser()

    def _pick_schema(self, task: str) -> OutputSchema:
        task = task.lower().strip()
        if task in {"intent", "classify", "classification"}:
            return build_intent_schema()
        if task in {"resume", "cv"}:
            return build_resume_schema()
        return build_extraction_schema()

    def run(self, task: str, text: str, strict: bool = False) -> Dict:
        schema = self._pick_schema(task)
        prompt = self._build_prompt(schema, text, strict=strict)

        last_error = ""
        raw_output = ""
        parsed = None
        validation = None

        for attempt in range(self.max_retry + 1):
            raw_output = self.model.generate(prompt, schema, strict=(strict or attempt > 0))
            parse_result = self.parser.parse(raw_output)
            if not parse_result.ok:
                last_error = parse_result.error
                prompt = self._build_retry_prompt(schema, text, parse_result.error)
                continue

            parsed = parse_result.data or {}
            validation = validate_payload(schema, parsed)
            if validation.ok:
                return {
                    "ok": True,
                    "schema": schema.name,
                    "prompt": prompt,
                    "raw_output": raw_output,
                    "parsed": parsed,
                    "validation_errors": [],
                    "attempts": attempt + 1,
                }

            last_error = "; ".join(validation.errors)
            prompt = self._build_retry_prompt(schema, text, last_error)

        return {
            "ok": False,
            "schema": schema.name,
            "prompt": prompt,
            "raw_output": raw_output,
            "parsed": parsed,
            "validation_errors": validation.errors if validation else [last_error],
            "attempts": self.max_retry + 1,
        }

    def _build_prompt(self, schema: OutputSchema, text: str, strict: bool = False) -> str:
        strict_line = "Return ONLY valid JSON." if strict else "Return JSON output."
        return (
            f"You are a structured output assistant.\n"
            f"{strict_line}\n\n"
            f"{schema.to_prompt_block()}\n\n"
            f"Input text:\n{text}\n"
        )

    def _build_retry_prompt(self, schema: OutputSchema, text: str, error: str) -> str:
        return (
            f"The previous output had issues: {error}.\n"
            f"Please return ONLY JSON that matches the schema exactly.\n\n"
            f"{schema.to_prompt_block()}\n\n"
            f"Input text:\n{text}\n"
        )

