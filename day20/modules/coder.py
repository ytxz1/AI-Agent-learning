"""代码草案生成模块。

这个模块负责把计划转成“文件变更草案”。
它的目标不是直接替你修改真实项目，而是输出一个清晰的 change set，
方便你审阅后再决定是否落盘。
"""

from __future__ import annotations

import json
import re
from typing import Iterable

from config import CODE_MODEL, OPENAI_API_KEY, OPENAI_BASE_URL, TEMPERATURE

try:
    from langchain_core.messages import HumanMessage
    from langchain_openai import ChatOpenAI
except Exception:  # pragma: no cover
    ChatOpenAI = None
    HumanMessage = None


def _extract_json(text: str) -> dict:
    """尽量从模型输出中提取 JSON。"""
    # 情况 1：模型直接输出纯 JSON。
    try:
        return json.loads(text)
    except Exception:
        pass

    # 情况 2：模型把 JSON 放在 ```json 代码块里。
    code_block = re.search(r"```json\s*(.*?)\s*```", text, re.S)
    if code_block:
        try:
            return json.loads(code_block.group(1))
        except Exception:
            pass

    # 情况 3：模型输出里混入解释，尝试截取 JSON 主体。
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except Exception:
            pass

    raise ValueError("无法提取 JSON")


class ChangeSetBuilder:
    """把计划转成文件变更草案。"""

    def __init__(self):
        # 有 API Key 时优先在线生成代码草案，否则使用本地兜底。
        self.api_enabled = bool(OPENAI_API_KEY and ChatOpenAI is not None)
        self.llm = None
        if self.api_enabled:
            try:
                self.llm = ChatOpenAI(
                    api_key=OPENAI_API_KEY,
                    base_url=OPENAI_BASE_URL,
                    model=CODE_MODEL,
                    temperature=TEMPERATURE,
                )
            except Exception:
                # 初始化失败时回退本地模式。
                self.api_enabled = False
                self.llm = None

    def _local_changes(self, request: str, plan: dict, focus_files: Iterable[str] | None = None) -> dict:
        """本地兜底 change set。"""
        files = list(focus_files or [])
        target = files[0] if files else "main.py"
        return {
            "objective": request,
            "mode": "local",
            "summary": "本地模式下生成的是审阅草案，不会直接修改文件。",
            "files": [
                {
                    "path": target,
                    "action": "review",
                    "explanation": "根据用户请求和计划，建议在该文件中实现修改。",
                    "content": f"# 这里是对 {target} 的修改草案占位。\n# 需求：{request}\n# 计划：{json.dumps(plan, ensure_ascii=False)}",
                }
            ],
            "tests": [
                "确认目标文件是否正确",
                "检查修改前后逻辑是否一致",
                "运行语法检查或基本测试",
            ],
        }

    def _build_prompt(self, request: str, plan: dict, workspace_excerpt: str, focus_files: Iterable[str] | None = None) -> str:
        """构建给在线模型的代码草案提示词。"""
        files_text = "\n".join(f"- {item}" for item in (focus_files or [])) or "- 无"
        return (
            "你是一个 Coding Agent 的代码草案生成器。请根据请求、计划和代码上下文，输出严格 JSON。\n"
            "要求：\n"
            "1. 只输出 JSON，不要解释。\n"
            "2. JSON 必须包含：objective, mode, summary, files, tests, notes。\n"
            "3. files 是数组，每个元素包含 path, action, explanation, content。\n"
            "4. action 只能是 create / update / delete / review。\n"
            "5. content 必须是可读代码或明确的草案，不要空白。\n"
            "6. 如果上下文不足，尽量给出安全的最小修改方案。\n\n"
            f"用户请求：{request}\n\n"
            f"计划：{json.dumps(plan, ensure_ascii=False, indent=2)}\n\n"
            f"代码上下文：\n{workspace_excerpt}\n\n"
            f"建议关注文件：\n{files_text}"
        )

    def generate_change_set(self, request: str, plan: dict, workspace_excerpt: str, focus_files: Iterable[str] | None = None) -> dict:
        """生成文件变更草案。"""
        if self.llm is None:
            return self._local_changes(request, plan, focus_files)

        try:
            # 在线模式：让模型输出严格 JSON，然后解析成 change set。
            response = self.llm.invoke([HumanMessage(content=self._build_prompt(request, plan, workspace_excerpt, focus_files))])
            raw_text = getattr(response, "content", str(response))
            data = _extract_json(raw_text)
            data.setdefault("objective", request)
            data.setdefault("mode", "code")
            return data
        except Exception:
            # 在线失败时回退本地草案，保证流程不断。
            return self._local_changes(request, plan, focus_files)
