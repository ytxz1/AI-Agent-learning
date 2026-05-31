"""A small mock model used to demonstrate structured output."""

from __future__ import annotations

import json
import random
import re
from typing import Dict, List

from schemas.output_schema import OutputSchema


class MockStructuredModel:
    def __init__(self, seed: int = 42):
        self.random = random.Random(seed)

    def _extract_keywords(self, text: str, limit: int = 4) -> List[str]:
        tokens = re.findall(r"[A-Za-z0-9\u4e00-\u9fff]+", text)
        keywords: List[str] = []
        for token in tokens:
            token = token.strip()
            if len(token) <= 1:
                continue
            if token not in keywords:
                keywords.append(token)
            if len(keywords) >= limit:
                break
        return keywords or ["unknown"]

    def _classification_payload(self, prompt: str) -> Dict:
        lower = prompt.lower()
        if "translate" in lower or "翻译" in prompt:
            intent = "translate"
            need_tool = True
        elif "summar" in lower or "总结" in prompt:
            intent = "summarize"
            need_tool = False
        elif "extract" in lower or "提取" in prompt:
            intent = "extract"
            need_tool = False
        elif "weather" in lower or "天气" in prompt:
            intent = "weather_query"
            need_tool = True
        else:
            intent = "question"
            need_tool = False
        return {
            "intent": intent,
            "confidence": 0.91,
            "entities": self._extract_keywords(prompt, 3),
            "need_tool": need_tool,
        }

    def _extraction_payload(self, prompt: str) -> Dict:
        return {
            "title": "Structured extraction result",
            "summary": prompt[:80] + ("..." if len(prompt) > 80 else ""),
            "keywords": self._extract_keywords(prompt, 5),
            "category": "text_extraction",
        }

    def _resume_payload(self, prompt: str) -> Dict:
        skills = self._extract_keywords(prompt, 4)
        return {
            "name": "Unknown",
            "education": "Unknown",
            "skills": skills,
            "experience_years": 0,
        }

    def generate(self, prompt: str, schema: OutputSchema, strict: bool = False) -> str:
        if schema.name == "intent_classification":
            payload = self._classification_payload(prompt)
        elif schema.name == "resume_extraction":
            payload = self._resume_payload(prompt)
        else:
            payload = self._extraction_payload(prompt)

        if strict:
            return json.dumps(payload, ensure_ascii=False, indent=2)

        # Intentionally inject small formatting issues sometimes to demonstrate parsing/repair.
        style = self.random.choice(["plain", "fenced", "noisy"])
        if style == "plain":
            return json.dumps(payload, ensure_ascii=False)
        if style == "fenced":
            return f"```json\n{json.dumps(payload, ensure_ascii=False, indent=2)}\n```"
        return f"Sure, here is the JSON result:\n{json.dumps(payload, ensure_ascii=False)}"

