"""JSON 输出解析器，带基础修复能力。"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ParseResult:
    """解析结果，成功或失败都统一用这个结构返回。"""

    ok: bool
    data: Optional[Dict[str, Any]] = None
    error: str = ""
    raw: str = ""


class JsonOutputParser:
    """负责从模型输出中提取并解析 JSON。"""

    def extract_json_block(self, text: str) -> str:
        """尝试从文本中截取最外层 JSON 对象。

        很多模型会在 JSON 外面额外补一句解释，这里会尽量把 JSON 主体截出来。
        """
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return text.strip()
        return text[start : end + 1]

    def try_repair(self, text: str) -> str:
        """对常见的格式问题做轻量修复。

        这里只做最常见的修复：
        - 去掉 ```json 代码块
        - 去掉多余逗号
        - 去掉外层多余引号
        """
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
        """依次尝试原文、截取版、修复版。

        只要其中一种方式解析成功，就返回成功结果。
        """
        candidates = [text, self.extract_json_block(text), self.try_repair(text)]
        last_error = ""

        for candidate in candidates:
            try:
                data = json.loads(candidate)
                if isinstance(data, dict):
                    return ParseResult(ok=True, data=data, raw=text)
                last_error = "解析后的结果不是 JSON 对象。"
            except Exception as exc:
                # 记录最后一次错误，方便调试。
                last_error = str(exc)

        return ParseResult(ok=False, error=last_error, raw=text)
