"""
Day 13 - Memory 模块：对话记忆管理

整合 Day 9 的记忆知识，管理对话历史和上下文。
支持窗口记忆、历史裁剪、导出功能。
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from rich.console import Console
from rich.table import Table

console = Console()


class ConversationMemory:
    """对话记忆管理类

    功能：
    1. 保存对话历史
    2. 滑动窗口裁剪（防止 Token 超限）
    3. 获取历史记录
    4. 清空/导出历史
    """

    def __init__(self, window_size: int = 10):
        """
        初始化记忆管理器。

        参数:
            window_size: 窗口大小，保留最近几轮对话（1轮=Human+AI）
        """
        self.window_size = window_size
        self.full_history = []   # 完整历史（用于展示）
        self.messages = []       # 发送给 LLM 的消息（受窗口限制）

    def add_system(self, content: str):
        """添加系统提示词"""
        msg = SystemMessage(content=content)
        self.messages.append(msg)
        self.full_history.append(msg)

    def add_user(self, content: str):
        """添加用户消息"""
        msg = HumanMessage(content=content)
        self.messages.append(msg)
        self.full_history.append(msg)

    def add_ai(self, content: str = ""):
        """添加 AI 消息（占位，稍后更新内容）"""
        msg = AIMessage(content=content)
        self.messages.append(msg)
        self.full_history.append(msg)
        return msg

    def add_tool(self, content: str, tool_call_id: str):
        """添加工具执行结果"""
        msg = ToolMessage(content=content, tool_call_id=tool_call_id)
        self.messages.append(msg)
        self.full_history.append(msg)

    def update_ai(self, msg: AIMessage, content: str):
        """更新 AI 消息内容"""
        msg.content = content

    def get_context(self) -> list:
        """获取发送给 LLM 的上下文（已裁剪）"""
        self._trim()
        return self.messages[:]  # 返回副本

    def get_history_table(self) -> str:
        """获取格式化的历史记录表格"""
        table = Table(title=f"对话历史（共 {len(self.full_history)} 条）")
        table.add_column("序号", style="dim", width=6)
        table.add_column("角色", style="cyan", width=10)
        table.add_column("内容", style="white", width=70)

        count = 0
        for msg in self.full_history:
            if isinstance(msg, (HumanMessage, AIMessage)):
                count += 1
                role = "你" if isinstance(msg, HumanMessage) else "AI"
                text = msg.content[:60] + "..." if len(msg.content) > 60 else msg.content
                table.add_row(str(count), role, text)
        return table

    def _trim(self):
        """滑动窗口裁剪"""
        # 保留 SystemMessage + 最近 window_size 轮
        max_msgs = self.window_size * 2 + len([m for m in self.messages if isinstance(m, SystemMessage)])
        if len(self.messages) > max_msgs:
            # 保留 SystemMessage(s)
            system_msgs = [m for m in self.messages if isinstance(m, SystemMessage)]
            # 保留最近的窗口
            non_system = [m for m in self.messages if not isinstance(m, SystemMessage)]
            self.messages = system_msgs + non_system[-(max_msgs - len(system_msgs)):]

    def clear(self):
        """清空历史"""
        self.full_history.clear()
        self.messages.clear()

    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "total_messages": len(self.full_history),
            "context_messages": len(self.messages),
            "window_size": self.window_size,
        }


if __name__ == "__main__":
    console.print("=" * 60, style="bold blue")
    console.print("Day 13 - Memory 模块测试", style="bold blue")
    console.print("=" * 60, style="bold blue")

    memory = ConversationMemory(window_size=5)
    memory.add_system("你是一个智能助手")
    memory.add_user("北京天气怎么样？")
    memory.add_ai("北京今天 25°C，晴天")
    memory.add_user("上海呢？")
    memory.add_ai("上海 28°C，多云")

    stats = memory.get_stats()
    console.print(f"  历史消息：{stats['total_messages']} 条", style="green")
    console.print(f"  窗口大小：{stats['window_size']} 轮", style="green")
    console.print(f"  上下文中：{stats['context_messages']} 条", style="green")
    console.print("\n[bold green]Memory 模块测试完成[/bold green]")
