"""
Day 9 - Memory 记忆：ConversationBufferWindowMemory 滑动窗口记忆

ConversationBufferWindowMemory 只保留最近 K 轮对话。
优点：控制 token 消耗，保留最近的上下文。
缺点：丢失早期对话内容。

知识点：
1. k 参数的含义和设置
2. 滑动窗口的工作原理
3. 不同 k 值对对话效果的影响
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_core.output_parsers import StrOutputParser
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=MODEL_NAME,
    temperature=0.7,
)

console = Console()

print("=" * 60)
print("Day 9 - ConversationBufferWindowMemory 滑动窗口记忆")
print("=" * 60)

# ==============================
# 1. 创建窗口记忆（k=3，只保留最近3轮）
# ==============================

# k=3 表示只保留最近 3 轮对话（3条用户消息 + 3条AI回复 = 最多6条消息）
# 超出的部分会被自动丢弃
console.print("\n[bold]1. 创建窗口记忆 (k=3)[/bold]", style="cyan")

memory = ConversationBufferWindowMemory(
    k=3,                   # 保留最近 3 轮对话
    return_messages=True,
    memory_key="chat_history",
)

# ==============================
# 2. 模拟 6 轮对话
# ==============================

# 通过 6 轮对话，观察只有最近 3 轮被保留
console.print("\n[bold]2. 模拟 6 轮对话[/bold]", style="cyan")

conversations = [
    "第1轮：我叫小A",
    "第2轮：我在学Python",
    "第3轮：我喜欢吃火锅",
    "第4轮：我在北京工作",
    "第5轮：我养了一只猫",
    "第6轮：我最近在减肥",
]

for i, user_input in enumerate(conversations, 1):
    memory.save_context(
        {"input": user_input},
        {"output": f"收到第{i}轮信息"},
    )

    # 每轮都查看当前记忆
    messages = memory.load_memory_variables({})["chat_history"]
    msg_count = len(messages)
    console.print(f"  第{i}轮后 → 记忆中有 {msg_count} 条消息")

# ==============================
# 3. 查看最终记忆内容
# ==============================

console.print("\n[bold]3. 最终记忆内容（只有最近3轮）[/bold]", style="cyan")

messages = memory.load_memory_variables({})["chat_history"]
for msg in messages:
    role = "用户" if msg.type == "human" else "AI"
    console.print(f"  [{role}] {msg.content}")

# ==============================
# 4. 测试：早期信息是否丢失
# ==============================

console.print("\n[bold]4. 测试早期信息[/bold]", style="cyan")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()

# 这些是早期对话的内容，应该已经丢失
test_questions = [
    "我叫什么名字？",       # 第1轮 - 应该忘了
    "我在学什么？",         # 第2轮 - 应该忘了
    "我在哪里工作？",       # 第4轮 - 应该还记得
    "我养了什么宠物？",     # 第5轮 - 应该还记得
]

for question in test_questions:
    chat_history = memory.load_memory_variables({})["chat_history"]
    result = chain.invoke({
        "chat_history": chat_history,
        "input": question,
    })
    console.print(f"  问: {question}")
    console.print(f"  答: {result}\n")

# ==============================
# 5. 不同 k 值对比
# ==============================

console.print("\n[bold]5. 不同 k 值对比[/bold]", style="cyan")

print("""
┌──────┬──────────────────┬───────────────────────────────────┐
│ k 值 │ 保留对话轮数     │ 特点                              │
├──────┼──────────────────┼───────────────────────────────────┤
│  1   │ 只保留最新 1 轮  │ 几乎没有上下文，像单轮对话        │
│  3   │ 保留最近 3 轮    │ 轻量级，适合简单场景              │
│  5   │ 保留最近 5 轮    │ 平衡选择，大多数场景够用          │
│  10  │ 保留最近 10 轮   │ 上下文丰富，但 token 消耗较大     │
│  20  │ 保留最近 20 轮   │ 接近完整记忆，需要大上下文窗口    │
└──────┴──────────────────┴───────────────────────────────────┘

选择建议：
- 简单问答机器人 → k=3~5
- 客服助手 → k=5~10
- 个人助理 → k=10~20
- 需要精确回忆 → 用 BufferMemory（不限制）
""")

console.print("✅ ConversationBufferWindowMemory 演示完成！", style="bold green")