"""记忆管理模块"""

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from rich.table import Table

class ConversationMemory:
    """对话记忆管理类，支持滑动窗口裁剪"""

    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.full_history = []
        self.messages = []

    def add_system(self, content: str):
        msg = SystemMessage(content=content)
        self.messages.append(msg)
        self.full_history.append(msg)

    def add_user(self, content: str):
        msg = HumanMessage(content=content)
        self.messages.append(msg)
        self.full_history.append(msg)

    def add_ai(self, content: str = ""):
        msg = AIMessage(content=content)
        self.messages.append(msg)
        self.full_history.append(msg)
        return msg

    def add_tool(self, content: str, tool_call_id: str):
        msg = ToolMessage(content=content, tool_call_id=tool_call_id)
        self.messages.append(msg)
        self.full_history.append(msg)

    def update_ai(self, msg, content: str):
        msg.content = content

    def get_context(self) -> list:
        self._trim()
        return self.messages[:]

    def _trim(self):
        max_msgs = self.window_size * 2 + len([m for m in self.messages if isinstance(m, SystemMessage)])
        if len(self.messages) > max_msgs:
            system_msgs = [m for m in self.messages if isinstance(m, SystemMessage)]
            non_system = [m for m in self.messages if not isinstance(m, SystemMessage)]
            self.messages = system_msgs + non_system[-(max_msgs - len(system_msgs)):]

    def get_history_table(self):
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

    def clear(self):
        self.full_history.clear()
        self.messages.clear()

    def get_stats(self) -> dict:
        return {"total_messages": len(self.full_history), "context_messages": len(self.messages), "window_size": self.window_size}
