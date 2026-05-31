"""
Day 9 - Memory 记忆：ConversationBufferMemory 对话缓冲记忆

这是最基础的记忆类型，将所有对话历史完整保存在内存中。
优点：信息零丢失，AI 能记住所有细节。
缺点：随着对话变长，token 消耗越来越大，最终会超过模型上下文窗口限制。

知识点：
1. ConversationBufferMemory 的创建和使用
2. 消息的添加和读取
3. 记忆对对话效果的影响
"""

# ==============================
# 导入所需模块
# ==============================

# ChatOpenAI: LangChain 的 Chat 模型封装
from langchain_openai import ChatOpenAI

# ChatPromptTemplate: 对话提示词模板
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# ConversationBufferMemory: 对话缓冲记忆，保存所有消息
from langchain_classic.memory import ConversationBufferMemory

# StrOutputParser: 字符串解析器
from langchain_core.output_parsers import StrOutputParser

# 配置变量
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

# Rich: 终端美化输出
from rich.console import Console
from rich.panel import Panel

# 创建 LLM 实例
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=MODEL_NAME,
    temperature=0.7,
)

# 创建 Rich 控制台
console = Console()

print("=" * 60)
print("Day 9 - ConversationBufferMemory 对话缓冲记忆")
print("=" * 60)

# ==============================
# 1. 认识 Memory 对象
# ==============================

# ConversationBufferMemory 是最简单的记忆类型
# 它把每一条消息都保存下来，不做任何压缩或摘要
console.print("\n[bold]1. 创建 Memory 对象[/bold]", style="cyan")

memory = ConversationBufferMemory(
    return_messages=True,  # True = 返回消息对象列表（适合 Chat 模型）
                            # False = 返回拼接后的字符串（适合旧版 LLM）
)

# 查看初始状态：空记忆
print(f"初始记忆: {memory.chat_memory.messages}")
print(f"记忆类型: {type(memory)}")

# ==============================
# 2. 手动添加消息到记忆
# ==============================

# 可以手动往记忆里添加消息
# 这样即使不经过 LLM，也能构建对话历史
console.print("\n[bold]2. 手动添加消息[/bold]", style="cyan")

# 添加用户消息
memory.chat_memory.add_user_message("你好，我叫小明")
# 添加 AI 回复
memory.chat_memory.add_ai_message("你好小明！很高兴认识你。有什么我可以帮你的吗？")

# 查看当前记忆
print("当前记忆:")
for msg in memory.chat_memory.messages:
    role = "用户" if msg.type == "human" else "AI"
    print(f"  [{role}] {msg.content}")

# ==============================
# 3. 记忆在 Chain 中的使用
# ==============================

# 核心：用 MessagesPlaceholder 占位符把记忆注入到提示词中
# 每次调用 Chain 时，LangChain 会自动把记忆中的消息填充到这个占位符
console.print("\n[bold]3. 记忆 + Chain 结合[/bold]", style="cyan")

# 创建一个新的记忆（干净的）
memory_conversation = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history",  # 在提示词中对应的变量名
)

# 提示词模板
# MessagesPlaceholder 是专门用来放消息列表的占位符
# 它和普通变量不同：普通变量填字符串，它填消息列表
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的AI助手。记住用户说过的话。"),
    MessagesPlaceholder(variable_name="chat_history"),  # 记忆占位符
    ("human", "{input}"),  # 用户当前输入
])

# 创建 Chain
chain = prompt | llm | StrOutputParser()

# 模拟多轮对话
conversations = [
    "你好，我叫小红",
    "我是学生，在学 Python",
    "你还记得我叫什么名字吗？",
    "我在学什么编程语言？",
]

for user_input in conversations:
    console.print(f"\n[bold]用户: {user_input}[/bold]")

    # 获取当前记忆中的消息列表
    chat_history = memory_conversation.load_memory_variables({})["chat_history"]

    # 调用 Chain，传入记忆和用户输入
    result = chain.invoke({
        "chat_history": chat_history,
        "input": user_input,
    })

    console.print(f"[green]AI: {result}[/green]")

    # 把这轮对话保存到记忆中
    memory_conversation.chat_memory.add_user_message(user_input)
    memory_conversation.chat_memory.add_ai_message(result)

# ==============================
# 4. 查看完整记忆
# ==============================

console.print("\n[bold]4. 查看完整记忆[/bold]", style="cyan")

all_messages = memory_conversation.load_memory_variables({})["chat_history"]
print(f"总共 {len(all_messages)} 条消息:")
for i, msg in enumerate(all_messages, 1):
    role = "用户" if msg.type == "human" else "AI"
    print(f"  {i}. [{role}] {msg.content}")

# ==============================
# 5. 清空记忆
# ==============================

console.print("\n[bold]5. 清空记忆[/bold]", style="cyan")

# clear() 方法清空所有记忆
memory_conversation.clear()
remaining = memory_conversation.load_memory_variables({})["chat_history"]
print(f"清空后消息数: {len(remaining)}")

console.print("\n✅ ConversationBufferMemory 演示完成！", style="bold green")