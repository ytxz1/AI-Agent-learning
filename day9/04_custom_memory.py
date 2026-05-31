"""
Day 9 - Memory 记忆：自定义记忆 + 实用技巧

当内置 Memory 不满足需求时，可以自己实现记忆逻辑。
本示例演示：
1. 自定义记忆类（存储用户画像）
2. 组合多种记忆类型
3. 记忆的序列化和持久化（保存到文件）

知识点：
1. BaseChatMemory 基类
2. 自定义记忆的实现
3. 记忆的保存和加载
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    CombinedMemory,
)
from langchain_core.output_parsers import StrOutputParser
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
import json
import os

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=MODEL_NAME,
    temperature=0.7,
)

console = Console()

print("=" * 60)
print("Day 9 - 自定义记忆 + 实用技巧")
print("=" * 60)

# ==============================
# 1. 组合记忆（CombinedMemory）
# ==============================

# CombinedMemory 可以同时使用多种记忆类型
# 比如：短期用 BufferMemory，长期用 SummaryMemory
console.print("\n[bold]1. 组合记忆 CombinedMemory[/bold]", style="cyan")

# 短期记忆：保留最近 3 轮
short_memory = ConversationBufferWindowMemory(
    k=3,
    return_messages=True,
    memory_key="short_history",
)

# 长期记忆：保留所有对话（这里用 Buffer 模拟，实际可用 Summary）
long_memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="long_history",
)

# 组合两种记忆
combined = CombinedMemory(
    memories=[short_memory, long_memory]
)

# 模拟对话
conversations = [
    ("我叫小明", "你好小明"),
    ("我在学Python", "Python很棒"),
    ("我住在北京", "北京是个好地方"),
    ("我喜欢编程", "编程很有意思"),
    ("我养了一只狗", "真可爱"),
]

for user_input, ai_output in conversations:
    short_memory.save_context({"input": user_input}, {"output": ai_output})
    long_memory.save_context({"input": user_input}, {"output": ai_output})

# 查看组合记忆
vars_dict = combined.load_memory_variables({})
print(f"短期记忆: {len(vars_dict['short_history'])} 条")
print(f"长期记忆: {len(vars_dict['long_history'])} 条")

# ==============================
# 2. 自定义记忆：用户画像
# ==============================

# 有时候我们需要记录用户的固定信息（如姓名、偏好）
# 这些信息不需要每轮都重复，用自定义记忆来处理
console.print("\n[bold]2. 自定义记忆：用户画像[/bold]", style="cyan")

class UserProfileMemory:
    """
    自定义记忆类：维护用户画像
    可以从对话中提取用户信息并保存
    """

    def __init__(self):
        self.profile = {}  # 存储用户画像

    def update_profile(self, key, value):
        """更新用户画像"""
        self.profile[key] = value

    def get_profile_string(self):
        """获取用户画像的字符串描述"""
        if not self.profile:
            return "暂无用户信息"
        lines = [f"{k}: {v}" for k, v in self.profile.items()]
        return "\n".join(lines)

    def clear(self):
        """清空画像"""
        self.profile = {}

# 使用自定义记忆
profile_memory = UserProfileMemory()

# 从对话中提取信息
profile_memory.update_profile("姓名", "小明")
profile_memory.update_profile("职业", "Python 开发者")
profile_memory.update_profile("兴趣", "机器学习")
profile_memory.update_profile("城市", "北京")

print("用户画像:")
print(profile_memory.get_profile_string())

# ==============================
# 3. 记忆的文件持久化
# ==============================

# 把记忆保存到文件，下次启动时可以恢复
console.print("\n[bold]3. 记忆持久化（保存到文件）[/bold]", style="cyan")

class FileMemory:
    """
    基于文件的持久化记忆
    把对话历史保存到 JSON 文件中
    """

    def __init__(self, filepath="memory.json"):
        self.filepath = filepath
        self.messages = []
        self.load()  # 启动时自动加载

    def add_message(self, role, content):
        """添加消息"""
        self.messages.append({"role": role, "content": content})
        self.save()  # 每次添加后自动保存

    def get_messages(self):
        """获取所有消息"""
        return self.messages

    def save(self):
        """保存到文件"""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)

    def load(self):
        """从文件加载"""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.messages = json.load(f)

    def clear(self):
        """清空记忆"""
        self.messages = []
        self.save()

# 测试持久化记忆
file_memory = FileMemory("day9_memory.json")

# 添加一些消息
file_memory.add_message("user", "你好，我叫小红")
file_memory.add_message("ai", "你好小红！")
file_memory.add_message("user", "我在学LangChain")
file_memory.add_message("ai", "LangChain很棒！")

print(f"保存了 {len(file_memory.get_messages())} 条消息到文件")

# 模拟重新加载
file_memory2 = FileMemory("day9_memory.json")
print(f"重新加载后有 {len(file_memory2.get_messages())} 条消息")

# 清理测试文件
if os.path.exists("day9_memory.json"):
    os.remove("day9_memory.json")

# ==============================
# 4. 记忆管理最佳实践
# ==============================

console.print("\n[bold]4. 记忆管理最佳实践[/bold]", style="cyan")

print("""
┌──────────────────────────────────────────────────────────────────┐
│                     记忆管理最佳实践                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. 选择合适的记忆类型                                           │
│     - 短对话（<10轮）→ ConversationBufferMemory                  │
│     - 长对话（>10轮）→ ConversationSummaryMemory                 │
│     - 只需近期上下文 → ConversationBufferWindowMemory (k=5~10)  │
│     - 复杂场景 → CombinedMemory 组合多种类型                     │
│                                                                  │
│  2. 设置合理的 memory_key                                        │
│     - 要和提示词模板中的占位符名称一致                            │
│     - 建议用 "chat_history" 作为统一命名                         │
│                                                                  │
│  3. 注意 token 预算                                              │
│     - 每条消息约占 50~200 tokens                                 │
│     - 留出足够空间给系统提示词和用户输入                          │
│     - DeepSeek 上下文窗口 64K，GPT-4 约 128K                     │
│                                                                  │
│  4. 定期清理                                                     │
│     - 长时间运行的机器人需要定期 clear()                          │
│     - 或者用 WindowMemory 自动限制                               │
│                                                                  │
│  5. 持久化存储                                                   │
│     - 生产环境建议用 Redis / 数据库存储记忆                       │
│     - 开发环境可以用文件存储                                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
""")

console.print("✅ 自定义记忆演示完成！", style="bold green")