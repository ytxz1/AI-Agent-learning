"""
Day 13 - Agent 模块：智能代理

整合 Day 11 的 Agent 知识，实现 ReAct 推理和工具选择。
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from modules.tools import all_tools, tool_map
from modules.memory import ConversationMemory
from modules.rag import RAGModule
from rich.console import Console

console = Console()


class SmartAgent:
    """智能 Agent：整合 Tools + Memory + RAG + ReAct 推理

    功能模式：
    1. chat - 普通对话（带记忆）
    2. tool - 工具增强问答（ReAct 推理）
    3. rag - 文档检索问答
    """

    MODE_CHAT = "chat"
    MODE_TOOL = "tool"
    MODE_RAG = "rag"

    def __init__(self):
        """初始化 Agent"""
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
            model=MODEL_NAME,
            temperature=0.7,
        )
        self.memory = ConversationMemory(window_size=10)
        self.rag = RAGModule(llm=self.llm)
        self.tools = all_tools
        self.tool_map = tool_map
        self.current_mode = self.MODE_CHAT

        # 初始化 RAG
        rag_init = self.rag.init()
        self.rag_available = self.rag._initialized

        # 设置系统提示词
        self._init_system_prompt()

    def _init_system_prompt(self):
        """初始化系统提示词"""
        self.memory.add_system(
            "你是一个综合智能助手，支持以下功能：\n"
            "1. 普通对话 - 日常聊天\n"
            "2. 工具调用 - 计算、天气、搜索、时间、单位换算\n"
            "3. 文档问答 - 基于已有文档回答问题\n"
            "请根据用户的问题选择合适的回答方式。"
        )

    def chat_mode(self, user_input: str) -> str:
        """普通对话模式（带记忆）"""
        self.memory.add_user(user_input)
        ai_msg = self.memory.add_ai()
        context = self.memory.get_context()
        response = self.llm.invoke(context)
        self.memory.update_ai(ai_msg, response.content)
        self.current_mode = self.MODE_CHAT
        return response.content

    def tool_mode(self, user_input: str, max_rounds: int = 5) -> str:
        """工具增强模式（ReAct 推理）"""
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

    def rag_mode(self, question: str) -> str:
        """文档问答模式"""
        self.current_mode = self.MODE_RAG
        if not self.rag_available:
            return "RAG 系统不可用，请先检查文档目录"
        self.memory.add_user(question)
        answer = self.rag.query(question)
        ai_msg = self.memory.add_ai(answer)
        return answer

    def auto_mode(self, user_input: str) -> str:
        """自动选择模式"""
        # 检测意图
        try:
            intent_prompt = f"分析以下问题的类型。只需回答一个词：chat（聊天）、tool（需要工具查询）、rag（文档知识）：\n问题：{user_input}"
            intent = self.llm.invoke([HumanMessage(content=intent_prompt)]).content.strip().lower()

            if "rag" in intent or "文档" in intent:
                return self.rag_mode(user_input)
            elif "tool" in intent:
                return self.tool_mode(user_input)
            else:
                return self.chat_mode(user_input)
        except:
            return self.chat_mode(user_input)

    def switch_mode(self, mode: str):
        """切换模式"""
        mode_map = {"chat": self.MODE_CHAT, "tool": self.MODE_TOOL, "rag": self.MODE_RAG}
        if mode in mode_map:
            self.current_mode = mode_map[mode]
            return f"已切换到 {mode} 模式"
        return f"未知模式：{mode}，支持：chat、tool、rag"

    def get_history(self):
        """获取对话历史"""
        return self.memory.get_history_table()

    def clear_memory(self):
        """清空记忆"""
        self.memory.clear()
        self._init_system_prompt()
        return "对话历史已清空"


if __name__ == "__main__":
    console.print("=" * 60, style="bold blue")
    console.print("Day 13 - Agent 模块测试", style="bold blue")
    console.print("=" * 60, style="bold blue")

    agent = SmartAgent()
    console.print(f"  RAG 可用：{agent.rag_available}", style="green")
    console.print(f"  工具数量：{len(agent.tools)}", style="green")

    # 测试聊天模式
    console.print("\n[bold cyan]测试聊天模式：[/bold cyan]")
    result = agent.chat_mode("你好！")
    console.print(f"  {result}", style="green")

    # 测试工具模式
    console.print("\n[bold cyan]测试工具模式：[/bold cyan]")
    result = agent.tool_mode("计算 2 的 10 次方")
    console.print(f"  {result}", style="green")

    console.print("\n[bold green]Agent 模块测试完成[/bold green]")
