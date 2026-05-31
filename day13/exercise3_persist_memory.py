"""
Day 13 - 练习 3（进阶）：记忆持久化

任务：实现对话历史的保存和加载（JSON 文件持久化）。

新增内容（标注 [新增]）：
  1. [新增] save_to_json 方法
  2. [新增] load_from_json 方法
  3. [新增] 跨会话记忆恢复
"""

import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.memory import ConversationMemory
from rich.console import Console
from rich.panel import Panel

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 13 - 练习 3：记忆持久化", style="bold blue")
console.print("=" * 60, style="bold blue")


# [新增] 持久化记忆类
class PersistentMemory(ConversationMemory):
    """支持保存和加载的持久化记忆"""

    def __init__(self, window_size: int = 10):
        super().__init__(window_size)
        self.save_path = os.path.join(os.path.dirname(__file__), "data", "memory.json")
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)

    def save_to_json(self):
        """[新增] 保存对话历史到 JSON 文件"""
        data = {
            "save_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "window_size": self.window_size,
            "history": [],
        }
        for msg in self.full_history:
            msg_type = type(msg).__name__
            if hasattr(msg, "content"):
                data["history"].append({"type": msg_type, "content": msg.content})

        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return f"已保存 {len(data['history'])} 条记录到 {self.save_path}"

    def load_from_json(self) -> str:
        """[新增] 从 JSON 文件加载对话历史"""
        if not os.path.exists(self.save_path):
            return "没有找到保存的记忆文件"

        with open(self.save_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.clear()
        self.window_size = data.get("window_size", 10)

        for item in data.get("history", []):
            msg_type = item["type"]
            content = item["content"]
            if msg_type == "SystemMessage":
                self.add_system(content)
            elif msg_type == "HumanMessage":
                self.add_user(content)
            elif msg_type == "AIMessage":
                self.add_ai(content)

        return f"已加载 {len(data['history'])} 条记录"

    def has_saved_data(self) -> bool:
        return os.path.exists(self.save_path)


# [新增] 测试
console.print("[bold cyan][新增] 测试记忆持久化[/bold cyan]")

memory = PersistentMemory(window_size=10)
memory.add_system("你是一个智能助手")
memory.add_user("你好，我叫小明")
memory.add_ai("你好小明！我是智能助手。")
memory.add_user("北京天气怎么样？")
memory.add_ai("北京今天 25°C，晴天")

# 保存
result = memory.save_to_json()
console.print(f"  保存：{result}", style="green")

# 清空
memory.clear()
console.print(f"  清空后消息数：{memory.get_stats()['total_messages']}", style="yellow")

# 加载
result = memory.load_from_json()
console.print(f"  加载：{result}", style="green")
console.print(f"  加载后消息数：{memory.get_stats()['total_messages']}", style="green")

# 验证记忆恢复
console.print("\n[bold cyan]验证记忆恢复：[/bold cyan]")
for msg in memory.full_history:
    if hasattr(msg, "content"):
        console.print(f"  [{type(msg).__name__}] {msg.content[:60]}", style="white")

console.print(Panel(
    "[bold]持久化的价值：[/bold]\n"
    "  - 重启程序后对话历史不丢失\n"
    "  - 可以跨会话恢复上下文\n"
    "  - 数据可以导出和分析",
    title="记忆持久化总结",
    style="green"
))

console.print("\n练习 3 完成！", style="bold green")
