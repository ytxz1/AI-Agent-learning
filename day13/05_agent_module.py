"""Day 13 - Agent 模块：综合智能助手。

这个文件把 Tools、Memory、输出解析模块和 LLM 组合在一起，
让项目同时具备：
- 普通聊天
- 工具调用
- 输出解析
- 自动模式判断
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from rich.console import Console

from config import MODEL_NAME, OPENAI_API_KEY, OPENAI_BASE_URL
from modules.memory import ConversationMemory
from modules.output_parser import OutputParserModule
from modules.tools import all_tools, tool_map

console = Console()


class SmartAgent:
    """整合 Tools + Memory + 输出解析 + ReAct 推理的 Agent。"""

    MODE_CHAT = "chat"
    MODE_TOOL = "tool"
    MODE_PARSE = "parse"

    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
            model=MODEL_NAME,
            temperature=0.7,
        )
        self.memory = ConversationMemory(window_size=10)
        self.output_parser = OutputParserModule(llm=self.llm)
        self.tools = all_tools
        self.tool_map = tool_map
        self.current_mode = self.MODE_CHAT

        # 初始化输出解析模块
        parse_init = self.output_parser.init()
        self.output_parser_available = self.output_parser._initialized

        # 初始化系统提示词
        self._init_system_prompt()

    def _init_system_prompt(self):
        """把项目角色和能力写进系统提示词。"""
        self.memory.add_system(
            "你是一个综合智能助手，支持以下功能：\n"
            "1. 普通对话：进行自然聊天和信息交流。\n"
            "2. 工具调用：当用户需要计算、天气、时间、单位换算等结果时，优先调用工具。\n"
            "3. 输出解析：当用户要求整理、提取、结构化、JSON 输出时，优先输出结构化结果。\n"
            "请根据用户问题选择最合适的回答方式。"
        )

    def chat_mode(self, user_input: str) -> str:
        """普通对话模式。"""
        self.memory.add_user(user_input)
        ai_msg = self.memory.add_ai()
        context = self.memory.get_context()
        response = self.llm.invoke(context)
        self.memory.update_ai(ai_msg, response.content)
        self.current_mode = self.MODE_CHAT
        return response.content

    def tool_mode(self, user_input: str, max_rounds: int = 5) -> str:
        """工具增强模式：通过 ReAct 思路调用工具。"""
        self.current_mode = self.MODE_TOOL
        self.memory.add_user(user_input)
        llm_with_tools = self.llm.bind_tools(self.tools)
        messages = self.memory.get_context()[:]

        for _ in range(max_rounds):
            response = llm_with_tools.invoke(messages)
            messages.append(response)

            if response.tool_calls:
                for tc in response.tool_calls:
                    tool_name = tc["name"]
                    tool_args = tc["args"]
                    result = self.tool_map[tool_name].invoke(tool_args) if tool_name in self.tool_map else "未知工具"
                    console.print(f"  [工具] {tool_name}({tool_args}) -> {result}", style="dim yellow")
                    messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
            else:
                ai_msg = self.memory.add_ai(response.content)
                return response.content

        return "达到最大推理轮数"

    def parse_mode(self, user_input: str) -> str:
        """输出解析模式：把用户内容整理成结构化 JSON。"""
        self.current_mode = self.MODE_PARSE
        self.memory.add_user(user_input)
        answer = self.output_parser.query(user_input)
        self.memory.add_ai(answer)
        return answer

    def auto_mode(self, user_input: str) -> str:
        """自动判断该使用哪种模式。"""
        try:
            intent_prompt = (
                "分析以下问题的类型，只需回答一个词：\n"
                "chat（普通聊天）、tool（需要工具查询）、parse（需要输出解析）。\n"
                f"问题：{user_input}"
            )
            intent = self.llm.invoke([HumanMessage(content=intent_prompt)]).content.strip().lower()

            if "parse" in intent or "结构化" in intent or "json" in intent or "整理" in intent:
                return self.parse_mode(user_input)
            if "tool" in intent or "工具" in intent:
                return self.tool_mode(user_input)
            return self.chat_mode(user_input)
        except Exception:
            return self.chat_mode(user_input)

    def switch_mode(self, mode: str):
        """手动切换模式。"""
        mode_map = {
            "chat": self.MODE_CHAT,
            "tool": self.MODE_TOOL,
            "parse": self.MODE_PARSE,
        }
        if mode in mode_map:
            self.current_mode = mode_map[mode]
            return f"已切换到 {mode} 模式"
        return f"未知模式：{mode}，支持：chat、tool、parse"

    def get_history(self):
        """获取对话历史。"""
        return self.memory.get_history_table()

    def clear_memory(self):
        """清空记忆并重新写入系统提示词。"""
        self.memory.clear()
        self._init_system_prompt()
        return "对话历史已清空"


if __name__ == "__main__":
    console.print("=" * 60, style="bold blue")
    console.print("Day 13 - Agent 模块测试", style="bold blue")
    console.print("=" * 60, style="bold blue")

    agent = SmartAgent()
    console.print(f"  输出解析模块可用：{agent.output_parser_available}", style="green")
    console.print(f"  工具数量：{len(agent.tools)}", style="green")

    console.print("\n[bold cyan]测试聊天模式[/bold cyan]")
    result = agent.chat_mode("你好")
    console.print(f"  {result}", style="green")

    console.print("\n[bold cyan]测试工具模式[/bold cyan]")
    result = agent.tool_mode("计算 2 的 10 次方")
    console.print(f"  {result}", style="green")

    console.print("\n[bold cyan]测试输出解析模式[/bold cyan]")
    result = agent.parse_mode("请把这段需求整理成 JSON：我要做一个天气助手，需要支持北京、上海和深圳。")
    console.print(f"  {result}", style="green")

    console.print("\n[bold green]Agent 模块测试完成[/bold green]")
