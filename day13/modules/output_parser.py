"""输出解析模块。

这个模块负责把自然语言内容整理成结构化结果，重点演示：
- 如何抽取关键信息
- 如何把结果整理成 JSON
- 如何在没有 LLM 的情况下用规则兜底
- 如何在 LLM 输出不规范时进行修复
"""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import HumanMessage
from rich.console import Console

console = Console()


class OutputParserModule:
    """把输入内容整理成结构化 JSON 的小模块。"""

    def __init__(self, llm=None):
        self.llm = llm
        self._initialized = False
        self.last_result: Dict[str, Any] | None = None

    def init(self) -> str:
        """初始化模块。

        这里没有复杂的资源加载逻辑，所以只要对象可用就算初始化完成。
        """
        self._initialized = True
        return "输出解析模块初始化完成"

    def _build_prompt(self, text: str) -> str:
        """构造给 LLM 的提示词，要求它只输出 JSON。"""
        return (
            "你是一个输出解析器，请把用户输入整理成 JSON。\n"
            "要求：\n"
            "1. 只输出 JSON，不要输出多余解释。\n"
            "2. 字段必须包含：原始输入、意图分类、摘要、关键词、实体、是否需要工具、建议动作、置信度。\n"
            "3. 关键词和实体都用数组表示。\n"
            "4. 置信度使用 0 到 1 之间的小数。\n"
            "5. 如果信息不完整，也要尽量补全，但不要编造不存在的事实。\n\n"
            f"用户输入：{text}"
        )

    def _extract_json(self, raw_text: str) -> Dict[str, Any]:
        """从 LLM 输出中提取 JSON。

        有些模型可能会在 JSON 前后加解释，这里会尽量把真正的 JSON 块取出来。
        """
        try:
            return json.loads(raw_text)
        except Exception:
            pass

        # 先找代码块中的 JSON
        fenced_match = re.search(r"```json\s*(.*?)\s*```", raw_text, re.S)
        if fenced_match:
            candidate = fenced_match.group(1)
            try:
                return json.loads(candidate)
            except Exception:
                pass

        # 再尝试截取第一个 { 到最后一个 }
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = raw_text[start : end + 1]
            try:
                return json.loads(candidate)
            except Exception:
                pass

        raise ValueError("无法从 LLM 输出中解析出 JSON")

    def _guess_intent(self, text: str) -> str:
        """根据关键词粗略判断意图。"""
        lowered = text.lower()
        if any(word in text for word in ["计算", "天气", "时间", "翻译", "单位换算", "查询"]):
            return "工具查询"
        if any(word in text for word in ["整理", "结构化", "JSON", "表格", "字段", "提取", "解析"]):
            return "输出解析"
        if any(word in text for word in ["你好", "你是谁", "帮我聊聊", "聊一聊"]):
            return "普通对话"
        if "plan" in lowered or "步骤" in text:
            return "任务拆解"
        return "信息整理"

    def _extract_keywords(self, text: str) -> List[str]:
        """提取一组简短的关键词。"""
        candidates = [
            "输出解析",
            "结构化",
            "JSON",
            "总结",
            "提取",
            "整理",
            "分类",
            "字段",
            "表格",
            "步骤",
            "需求",
            "工具",
            "聊天",
            "天气",
            "计算",
            "翻译",
            "时间",
            "单位换算",
        ]
        results = [word for word in candidates if word in text]

        # 如果候选关键词太少，就把文本里出现的常见数字、英文词补进去
        if len(results) < 3:
            extra = re.findall(r"[A-Za-z0-9_]+", text)
            for item in extra:
                if item not in results and len(item) > 1:
                    results.append(item)
                if len(results) >= 5:
                    break

        return results[:5]

    def _extract_entities(self, text: str) -> List[str]:
        """抽取比较像实体的片段。"""
        entities = []
        for pattern in [
            r"[A-Za-z]{2,}",
            r"\d+(?:\.\d+)?",
            r"[北京上海广州深圳杭州成都重庆][市]?",
        ]:
            for match in re.findall(pattern, text):
                if match not in entities:
                    entities.append(match)
        return entities[:5]

    def _heuristic_parse(self, text: str) -> Dict[str, Any]:
        """当没有 LLM 或 LLM 解析失败时，使用规则生成结果。"""
        keywords = self._extract_keywords(text)
        entities = self._extract_entities(text)
        intent = self._guess_intent(text)
        need_tool = any(word in text for word in ["计算", "天气", "时间", "翻译", "单位换算", "查询"])

        return {
            "原始输入": text,
            "意图分类": intent,
            "摘要": text[:80] + ("..." if len(text) > 80 else ""),
            "关键词": keywords,
            "实体": entities,
            "是否需要工具": need_tool,
            "建议动作": [
                "先确认用户目标",
                "再根据意图决定是否需要工具",
                "最后把结果整理成清晰格式",
            ],
            "置信度": 0.72 if keywords else 0.55,
            "解析方式": "规则解析",
        }

    def parse(self, text: str) -> Dict[str, Any]:
        """把自然语言内容解析为结构化字典。"""
        if not self._initialized:
            self.init()

        if self.llm is not None:
            try:
                response = self.llm.invoke([HumanMessage(content=self._build_prompt(text))])
                raw_text = getattr(response, "content", str(response))
                data = self._extract_json(raw_text)
                data.setdefault("原始输入", text)
                data.setdefault("解析方式", "LLM 解析")
                self.last_result = data
                return data
            except Exception as exc:
                data = self._heuristic_parse(text)
                data["解析方式"] = "规则兜底"
                data["解析备注"] = str(exc)
                self.last_result = data
                return data

        data = self._heuristic_parse(text)
        self.last_result = data
        return data

    def format_result(self, data: Optional[Dict[str, Any]] = None) -> str:
        """把结构化结果格式化成漂亮的 JSON 文本。"""
        if data is None:
            data = self.last_result or {}
        return json.dumps(data, ensure_ascii=False, indent=2)

    def query(self, text: str) -> str:
        """对外统一入口：输入文本，返回 JSON 字符串。"""
        return self.format_result(self.parse(text))

    def demo_samples(self) -> List[str]:
        """返回几个适合演示的样例。"""
        return [
            "请把这段需求整理成 JSON：我要做一个天气助手，需要支持北京、上海和深圳。",
            "帮我提炼这段内容的关键词和任务步骤：先收集数据，再做清洗，最后导出结果。",
            "把下面的话结构化一下：我想了解 Python、LangChain 和 Agent 的关系。",
        ]


if __name__ == "__main__":
    console.print("=" * 60, style="bold blue")
    console.print("Day 13 - 输出解析模块测试", style="bold blue")
    console.print("=" * 60, style="bold blue")

    parser = OutputParserModule()
    parser.init()

    for i, sample in enumerate(parser.demo_samples(), 1):
        console.print(f"\n[bold cyan]示例 {i}[/bold cyan]", style="cyan")
        console.print(sample, style="yellow")
        console.print(parser.query(sample), style="green")

    console.print("\n[bold green]输出解析模块测试完成[/bold green]")
