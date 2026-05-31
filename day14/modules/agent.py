"""Day 14 - 工具调用 Agent

这个 Agent 的重点是：
1. 识别是否需要工具
2. 选择工具并传参
3. 执行工具
4. 把工具结果整理成自然语言
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from rich.console import Console

from config import MAX_ROUNDS, MODEL_NAME, OPENAI_API_KEY, OPENAI_BASE_URL, TEMPERATURE
from .tools import all_tools, calculator, get_current_time, get_weather, tool_map, translate, unit_convert


@dataclass
class AgentStatus:
    mode: str
    api_available: bool
    tool_count: int
    history_count: int


class ToolAgent:
    MODE_CHAT = "chat"
    MODE_TOOL = "tool"
    MODE_AUTO = "auto"

    def __init__(self):
        self.console = Console()
        self.tools = all_tools
        self.tool_map = tool_map
        self.current_mode = self.MODE_AUTO
        self.max_history_messages = 12
        self.history = [SystemMessage(content=self._system_prompt())]
        self.api_available = bool(OPENAI_API_KEY)
        self.llm = None

        if self.api_available:
            self.llm = ChatOpenAI(
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_BASE_URL,
                model=MODEL_NAME,
                temperature=TEMPERATURE,
            )

    def _system_prompt(self) -> str:
        return (
            "你是一个工具调用型 AI Agent。"
            "你的任务是根据用户问题决定是否调用工具。"
            "如果需要工具，优先准确调用工具并读取结果。"
            "如果不需要工具，直接自然、简洁地回答。"
            "当用户提出组合任务时，可以连续调用多个工具。"
            "当参数不完整时，先尝试补全；如果补全不了，要明确说明。"
        )

    def _trim_history(self):
        recent = self.history[1:][-self.max_history_messages :]
        self.history = [self.history[0]] + recent

    def _context(self):
        return self.history[:]

    def _store_turn(self, user_input: str, answer: str):
        self.history.append(HumanMessage(content=user_input))
        self.history.append(AIMessage(content=answer))
        self._trim_history()

    def _invoke_tool(self, tool_name: str, tool_args: dict):
        tool = self.tool_map.get(tool_name)
        if not tool:
            return f"未找到工具：{tool_name}"
        try:
            return tool.invoke(tool_args)
        except Exception as exc:
            return f"工具 {tool_name} 执行失败：{exc}"

    def _needs_tool(self, text: str) -> bool:
        keywords = [
            "天气",
            "翻译",
            "时间",
            "几点",
            "算",
            "计算",
            "换算",
            "转换",
            "摄氏",
            "华氏",
            "公里",
            "英里",
            "公斤",
            "磅",
            "meter",
            "mile",
            "kg",
            "lb",
        ]
        if any(keyword.lower() in text.lower() for keyword in keywords):
            return True
        if re.search(r"\d+\s*[\+\-\*\/\%\(\)\^]\s*\d+", text):
            return True
        return False

    def _fallback_chat(self, user_input: str) -> str:
        return (
            f"我收到了你的问题：{user_input}\n"
            "当前环境没有配置 API，所以这里给你一个离线占位回复。"
            "如果你补上 API Key，Day 14 就能真正走工具调用流程。"
        )

    def _fallback_tool_answer(self, user_input: str) -> str:
        text = user_input.strip()

        math_match = re.search(r"([0-9\.\+\-\*\/\%\(\)\s\^]+)", text)
        if any(ch in text for ch in "+-*/%^") and math_match:
            expr = math_match.group(1).strip().replace("^", "**")
            result = calculator.invoke({"expression": expr})
            return f"计算结果：{result}"

        if "天气" in text:
            city = self._guess_city(text)
            result = get_weather.invoke({"city": city})
            return f"天气结果：{result}"

        if "翻译" in text:
            target_language = self._guess_target_language(text)
            source_text = self._guess_translate_text(text)
            result = translate.invoke({"text": source_text, "target_language": target_language})
            return f"翻译结果：{result}"

        if "时间" in text or "几点" in text:
            result = get_current_time.invoke({"timezone_name": "local"})
            return f"当前时间：{result}"

        if "换算" in text or "转换" in text:
            parsed = self._guess_unit_conversion(text)
            if parsed:
                value, from_unit, to_unit = parsed
                result = unit_convert.invoke(
                    {"value": value, "from_unit": from_unit, "to_unit": to_unit}
                )
                return f"换算结果：{result}"

        return self._fallback_chat(user_input)

    def _guess_city(self, text: str) -> str:
        city_candidates = ["北京", "上海", "广州", "深圳", "杭州", "成都"]
        for city in city_candidates:
            if city in text:
                return city
        return "北京"

    def _guess_target_language(self, text: str) -> str:
        if "英文" in text or "英语" in text or "en" in text.lower():
            return "English"
        if "中文" in text or "汉语" in text or "zh" in text.lower():
            return "Chinese"
        return "English"

    def _guess_translate_text(self, text: str) -> str:
        patterns = [
            r"翻译[:：]\s*(.+?)\s*(?:成|为|到|去)?(?:英文|英语|中文|汉语|English|Chinese|en|zh)?$",
            r"把\s*(.+?)\s*(?:翻译|转成|转换成)",
            r"translate\s+(.+?)\s+to",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip(" “”\"'")
        return text.replace("翻译", "").strip(" ：:") or "你好"

    def _guess_unit_conversion(self, text: str):
        patterns = [
            (r"(\d+(?:\.\d+)?)\s*(?:摄氏度|celsius|c)\s*(?:转|换算成|换成|到)\s*(?:华氏度|fahrenheit|f)", "celsius", "fahrenheit"),
            (r"(\d+(?:\.\d+)?)\s*(?:华氏度|fahrenheit|f)\s*(?:转|换算成|换成|到)\s*(?:摄氏度|celsius|c)", "fahrenheit", "celsius"),
            (r"(\d+(?:\.\d+)?)\s*(?:公里|km|kilometer)\s*(?:转|换算成|换成|到)\s*(?:英里|mile)", "km", "mile"),
            (r"(\d+(?:\.\d+)?)\s*(?:公斤|kg|kilogram)\s*(?:转|换算成|换成|到)\s*(?:磅|lb|pound)", "kg", "lb"),
        ]
        for pattern, from_unit, to_unit in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1)), from_unit, to_unit
        return None

    def chat_mode(self, user_input: str) -> str:
        """普通聊天模式：只回答，不调用工具。"""
        self.current_mode = self.MODE_CHAT
        if not self.api_available:
            answer = self._fallback_chat(user_input)
            self._store_turn(user_input, answer)
            return answer

        messages = self._context() + [HumanMessage(content=user_input)]
        response = self.llm.invoke(messages)
        answer = response.content or ""
        self._store_turn(user_input, answer)
        return answer

    def tool_mode(self, user_input: str, max_rounds: int = MAX_ROUNDS) -> str:
        """工具调用模式：让模型自己决定何时调用工具。"""
        self.current_mode = self.MODE_TOOL
        if not self.api_available:
            answer = self._fallback_tool_answer(user_input)
            self._store_turn(user_input, answer)
            return answer

        messages = self._context() + [HumanMessage(content=user_input)]
        llm_with_tools = self.llm.bind_tools(self.tools)

        for _ in range(max_rounds):
            response = llm_with_tools.invoke(messages)
            messages.append(response)

            tool_calls = getattr(response, "tool_calls", None) or []
            if tool_calls:
                for tool_call in tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call.get("args", {}) or {}
                    result = self._invoke_tool(tool_name, tool_args)
                    self.console.print(
                        f"  [tool] {tool_name}({tool_args}) -> {result}",
                        style="dim yellow",
                    )
                    messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
                continue

            answer = response.content or ""
            self._store_turn(user_input, answer)
            return answer

        answer = "已达到最大工具调用轮数。"
        self._store_turn(user_input, answer)
        return answer

    def auto_mode(self, user_input: str) -> str:
        """自动模式：根据问题类型判断走聊天还是工具。"""
        self.current_mode = self.MODE_AUTO
        if self._needs_tool(user_input):
            return self.tool_mode(user_input)
        return self.chat_mode(user_input)

    def switch_mode(self, mode: str) -> str:
        mode = mode.strip().lower()
        if mode in {self.MODE_CHAT, self.MODE_TOOL, self.MODE_AUTO}:
            self.current_mode = mode
            return f"已切换到 {mode} 模式"
        return f"未知模式：{mode}，可选 chat / tool / auto"

    def clear_history(self) -> str:
        self.history = [SystemMessage(content=self._system_prompt())]
        return "历史记录已清空"

    def get_history(self) -> str:
        lines = []
        for item in self.history[1:]:
            role = getattr(item, "type", "message")
            content = getattr(item, "content", "")
            lines.append(f"[{role}] {content}")
        return "\n".join(lines) if lines else "暂无历史记录"

    def get_tools_text(self) -> str:
        lines = []
        for item in self.tools:
            desc = item.description.split("\n", 1)[0]
            lines.append(f"- {item.name}: {desc}")
        return "\n".join(lines)

    def get_status(self) -> AgentStatus:
        return AgentStatus(
            mode=self.current_mode,
            api_available=self.api_available,
            tool_count=len(self.tools),
            history_count=max(len(self.history) - 1, 0),
        )
