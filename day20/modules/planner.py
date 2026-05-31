"""计划生成模块。

这个模块负责把用户的 Coding 请求整理成结构化计划。
如果配置了 API Key，就优先调用在线模型生成计划；
如果没有配置，就用规则生成一个可读的本地计划。
"""

from __future__ import annotations

import json
import re
from typing import Iterable

from config import OPENAI_API_KEY, OPENAI_BASE_URL, PLAN_MODEL, TEMPERATURE

try:
    from langchain_core.messages import HumanMessage
    from langchain_openai import ChatOpenAI
except Exception:  # pragma: no cover
    ChatOpenAI = None
    HumanMessage = None


def _extract_json(text: str) -> dict:
    """尽量从模型输出中提取 JSON。"""
    try:
        return json.loads(text)
    except Exception:
        pass

    code_block = re.search(r"```json\s*(.*?)\s*```", text, re.S)
    if code_block:
        try:
            return json.loads(code_block.group(1))
        except Exception:
            pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except Exception:
            pass

    raise ValueError("无法提取 JSON")


class CodingPlanner:
    """把用户请求整理成 Coding 计划。"""

    def __init__(self):
        self.api_enabled = bool(OPENAI_API_KEY and ChatOpenAI is not None)
        self.llm = None
        if self.api_enabled:
            try:
                self.llm = ChatOpenAI(
                    api_key=OPENAI_API_KEY,
                    base_url=OPENAI_BASE_URL,
                    model=PLAN_MODEL,
                    temperature=TEMPERATURE,
                )
            except Exception:
                self.api_enabled = False
                self.llm = None

    def _local_plan(self, request: str, workspace_summary: dict, focus_files: Iterable[str] | None = None) -> dict:
        """本地兜底计划。"""
        lower = request.lower()
        steps = []

        if any(word in lower for word in ["bug", "error", "报错", "修复", "fix"]):
            steps.extend([
                {"step": "阅读报错信息", "files": list(focus_files or []), "purpose": "定位问题来源"},
                {"step": "检查相关代码", "files": list(focus_files or []), "purpose": "找到可能的逻辑错误"},
                {"step": "修改并验证", "files": list(focus_files or []), "purpose": "完成修复并做基础验证"},
            ])
        elif any(word in lower for word in ["feature", "功能", "添加", "增加", "implement"]):
            steps.extend([
                {"step": "梳理需求", "files": list(focus_files or []), "purpose": "明确要新增什么功能"},
                {"step": "定位入口和数据流", "files": list(focus_files or []), "purpose": "找出需要修改的文件"},
                {"step": "实现并补充验证", "files": list(focus_files or []), "purpose": "完成新增功能并检查结果"},
            ])
        else:
            steps.extend([
                {"step": "理解需求", "files": list(focus_files or []), "purpose": "确认用户真正想改什么"},
                {"step": "扫描相关文件", "files": list(focus_files or []), "purpose": "找到最可能受影响的代码"},
                {"step": "形成修改方案", "files": list(focus_files or []), "purpose": "输出可执行计划"},
            ])

        return {
            "objective": request,
            "mode": "local",
            "workspace_summary": workspace_summary,
            "assumptions": [
                "当前使用本地规则生成计划",
                "如果给出具体文件，计划会更准确",
            ],
            "steps": steps,
            "validation": [
                "确认影响文件是否一致",
                "检查语法或运行入口",
                "复查修改点是否完整",
            ],
            "risks": [
                "需求如果不够具体，计划只能做保守推断",
                "如果涉及多个文件，后续还需要进一步拆解",
            ],
        }

    def _build_prompt(self, request: str, workspace_summary: dict, focus_files: Iterable[str] | None = None) -> str:
        files_text = "\n".join(f"- {item}" for item in (focus_files or [])) or "- 无"
        return (
            "你是一个专业的 Coding Agent 规划器。请根据用户请求和工作区信息，输出严格 JSON。\n"
            "要求：\n"
            "1. 只输出 JSON，不要额外解释。\n"
            "2. JSON 必须包含：objective, mode, assumptions, steps, validation, risks, workspace_summary。\n"
            "3. steps 是数组，每个元素包含 step, files, purpose。\n"
            "4. mode 只能是 plan / implement / review / local。\n"
            "5. 如果信息不足，要写清楚不确定点，不要编造。\n\n"
            f"用户请求：{request}\n\n"
            f"工作区摘要：{json.dumps(workspace_summary, ensure_ascii=False, indent=2)}\n\n"
            f"建议关注文件：\n{files_text}"
        )

    def generate_plan(self, request: str, workspace_summary: dict, focus_files: Iterable[str] | None = None) -> dict:
        """生成结构化计划。"""
        if self.llm is None:
            return self._local_plan(request, workspace_summary, focus_files)

        try:
            response = self.llm.invoke([HumanMessage(content=self._build_prompt(request, workspace_summary, focus_files))])
            raw_text = getattr(response, "content", str(response))
            data = _extract_json(raw_text)
            data.setdefault("objective", request)
            data.setdefault("mode", "plan")
            data.setdefault("workspace_summary", workspace_summary)
            return data
        except Exception:
            return self._local_plan(request, workspace_summary, focus_files)

