"""用于演示结构化输出的模拟模型。

这个模块不依赖真实 API，主要目的是让 Day 12 的流程可以直接运行。
它会故意输出一些“带噪声”的结果，方便你观察解析和修复流程。
"""

from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path
from typing import Dict, List


# 允许单独运行这个文件时，也能找到项目根目录里的模块。
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from schemas.output_schema import OutputSchema


class MockStructuredModel:
    """模拟一个会输出 JSON 的模型。"""

    def __init__(self, seed: int = 42):
        # 固定随机种子，保证每次演示更容易复现。
        self.random = random.Random(seed)

    def _extract_keywords(self, text: str, limit: int = 4) -> List[str]:
        """从文本中抽取关键词。"""
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

        return keywords or ["未知"]

    def _classification_payload(self, prompt: str) -> Dict:
        """模拟“意图识别”的返回结果。"""
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
        """模拟“信息抽取”的返回结果。"""
        return {
            "title": "结构化抽取结果",
            "summary": prompt[:80] + ("..." if len(prompt) > 80 else ""),
            "keywords": self._extract_keywords(prompt, 5),
            "category": "文本抽取",
        }

    def _resume_payload(self, prompt: str) -> Dict:
        """模拟“简历抽取”的返回结果。"""
        skills = self._extract_keywords(prompt, 4)
        return {
            "name": "未知",
            "education": "未知",
            "skills": skills,
            "experience_years": 0,
        }

    def generate(self, prompt: str, schema: OutputSchema, strict: bool = False) -> str:
        """根据 schema 生成 JSON 字符串。"""
        if schema.name == "intent_classification":
            payload = self._classification_payload(prompt)
        elif schema.name == "resume_extraction":
            payload = self._resume_payload(prompt)
        else:
            payload = self._extraction_payload(prompt)

        if strict:
            return json.dumps(payload, ensure_ascii=False, indent=2)

        # 故意随机加一点格式噪声，用来演示解析和修复。
        style = self.random.choice(["plain", "fenced", "noisy"])
        if style == "plain":
            return json.dumps(payload, ensure_ascii=False)
        if style == "fenced":
            return f"```json\n{json.dumps(payload, ensure_ascii=False, indent=2)}\n```"
        return f"好的，下面是 JSON 结果：\n{json.dumps(payload, ensure_ascii=False)}"


if __name__ == "__main__":
    # 直接运行这个文件时，做一个最小演示。
    demo_model = MockStructuredModel()
    from schemas.output_schema import build_extraction_schema

    sample_schema = build_extraction_schema()
    sample_prompt = "请提取摘要和关键词：Python 是一门非常适合 AI 开发的语言。"
    print(demo_model.generate(sample_prompt, sample_schema))
