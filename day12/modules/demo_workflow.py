"""Day 12 结构化输出工作流。

这个文件把整条流程串起来：
1. 选择 schema
2. 生成提示词
3. 调用模拟模型
4. 解析 JSON
5. 校验字段
6. 失败后重试

它既可以被 `main.py` 调用，也可以单独执行调试。
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict


# 允许这个文件被“单独运行”时也能找到项目根目录。
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import MAX_RETRY
from parsers.json_parser import JsonOutputParser
from schemas.output_schema import (
    OutputSchema,
    build_extraction_schema,
    build_intent_schema,
    build_resume_schema,
)
from tools.response_validator import validate_payload

from modules.mock_model import MockStructuredModel


class StructuredOutputWorkflow:
    """结构化输出工作流主类。"""

    def __init__(self, max_retry: int = MAX_RETRY):
        # max_retry 表示：解析失败或校验失败后，最多再尝试几次。
        self.max_retry = max_retry
        self.model = MockStructuredModel()
        self.parser = JsonOutputParser()

    def _pick_schema(self, task: str) -> OutputSchema:
        """根据任务类型选择对应的 schema。"""
        task = task.lower().strip()
        if task in {"intent", "classify", "classification"}:
            return build_intent_schema()
        if task in {"resume", "cv"}:
            return build_resume_schema()
        return build_extraction_schema()

    def run(self, task: str, text: str, strict: bool = False) -> Dict:
        """运行完整的结构化输出流程。"""
        schema = self._pick_schema(task)
        prompt = self._build_prompt(schema, text, strict=strict)

        last_error = ""
        raw_output = ""
        parsed = None
        validation = None

        for attempt in range(self.max_retry + 1):
            # 1. 让模型生成输出
            raw_output = self.model.generate(prompt, schema, strict=(strict or attempt > 0))

            # 2. 尝试解析 JSON
            parse_result = self.parser.parse(raw_output)
            if not parse_result.ok:
                last_error = parse_result.error
                prompt = self._build_retry_prompt(schema, text, parse_result.error)
                continue

            parsed = parse_result.data or {}

            # 3. 校验字段是否符合 schema
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

            # 4. 字段不合格就继续重试
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
        """构建首次提示词。"""
        strict_line = "请只输出合法 JSON。" if strict else "请输出 JSON。"
        return (
            f"你是一个结构化输出助手。\n"
            f"{strict_line}\n\n"
            f"{schema.to_prompt_block()}\n\n"
            f"输入文本：\n{text}\n"
        )

    def _build_retry_prompt(self, schema: OutputSchema, text: str, error: str) -> str:
        """构建重试提示词，把上一次的错误告诉模型。"""
        return (
            f"上一次输出有问题：{error}。\n"
            f"请严格返回和 schema 完全匹配的 JSON，不要加额外解释。\n\n"
            f"{schema.to_prompt_block()}\n\n"
            f"输入文本：\n{text}\n"
        )

