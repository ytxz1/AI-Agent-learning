"""JSON output parser with basic repair helpers."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ParseResult:
    ok: bool
    data: Optional[Dict[str, Any]] = None
    error: str = ""
    raw: str = ""


class JsonOutputParser:
    def extract_json_block(self, text: str) -> str:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return text.strip()
        return text[start : end + 1]

    def try_repair(self, text: str) -> str:
        repaired = text.strip()
        repaired = repaired.replace("```json", "").replace("```", "").strip()
        repaired = self.extract_json_block(repaired)
        repaired = repaired.replace("\n", " ")
        repaired = re.sub(r",\s*}", "}", repaired)
        repaired = re.sub(r",\s*]", "]", repaired)
        if repaired.startswith("'") and repaired.endswith("'"):
            repaired = repaired[1:-1]
        return repaired.strip()

    def parse(self, text: str) -> ParseResult:
        candidates = [text, self.extract_json_block(text), self.try_repair(text)]
        last_error = ""
        for candidate in candidates:
            try:
                data = json.loads(candidate)
                if isinstance(data, dict):
                    return ParseResult(ok=True, data=data, raw=text)
                last_error = "Parsed JSON is not an object"
            except Exception as exc:
                last_error = str(exc)
        return ParseResult(ok=False, error=last_error, raw=text)

