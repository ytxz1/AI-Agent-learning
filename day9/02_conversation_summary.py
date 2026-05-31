"""
Day 9 - Memory 记忆：ConversationSummaryMemory 对话摘要记忆

ConversationSummaryMemory 会用 LLM 把对话历史压缩成摘要。
优点：节省 token，能记住很长的对话。
缺点：会丢失细节，摘要需要额外调用 LLM（产生额外费用）。

知识点：
1. ConversationSummaryMemory 的工作原理
2. 摘要如何随对话更新
3. 摘要 vs 缓冲记忆的对比
"""

# ==============================
# 导入所需模块
# ==============================

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationSummaryMemory
from langchain_core.output_parsers import StrOutputParser
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel

# 创建 LLM 实例
# 注意：SummaryMemory 需要 LLM 来生成摘要，所以需要两个 LLM 实例：
# 一个用于对话，一个用于生成摘要（也可以用同一个）
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=MODEL_NAME,
    temperature=0.7,
)

console = Console()

print("=" * 60)
print("Day 9 - ConversationSummaryMemory 对话摘要记忆")
print("=" * 60)

# ==============================
# 1. 创建 Summary Memory
# ==============================

# ConversationSummaryMemory 会自动调用 LLM 把对话历史压缩成摘要
# 每次添加新消息时，都会更新摘要
console.print("\n[bold]1. 创建 Summary Memory[/bold]", style="cyan")

memory = ConversationSummaryMemory(
    llm=llm,  # 必须传入 LLM，因为需要它来生成摘要
    return_messages=True,
    memory_key="chat_history",
)

# ==============================
# 2. 模拟对话并观察摘要变化
# ==============================

# 每轮对话后，memory 会自动调用 LLM 更新摘要
# 我们可以观察摘要是如何变化的
console.print("\n[bold]2. 观察摘要变化[/bold]", style="cyan")

conversations = [
    ("我叫张三，是一名程序员", "张三"),
    ("我最近在学习机器学习，特别是深度学习方向", "机器学习"),
    ("我在用 Python 和 TensorFlow 做项目", "Python/TensorFlow"),
    ("我的目标是成为一名 AI 工程师", "AI工程师"),
]

for user_input, keyword in conversations:
    console.print(f"\n[bold]用户: {user_input}[/bold]")

    # 保存用户消息（这会触发摘要更新）
    memory.save_context(
        {"input": user_input},           # 用户输入
        {"output": f"好的{keyword}！"}   # AI 回复（模拟）
    )

    # 查看当前摘要
    summary = memory.load_memory_variables({})["chat_history"]
    console.print(f"[yellow]当前摘要: {summary[0].content}[/yellow]")

# ==============================
# 3. 使用摘要记忆进行对话
# ==============================

console.print("\n[bold]3. 用摘要记忆对话[/bold]", style="cyan")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手。以下是之前对话的摘要：\n{chat_history}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()

# 测试：AI 能否从摘要中回忆起信息
test_questions = [
    "我叫什么名字？",
    "我在学什么技术？",
    "我的职业目标是什么？",
]

for question in test_questions:
    console.print(f"\n[bold]用户: {question}[/bold]")
    chat_history = memory.load_memory_variables({})["chat_history"]
    result = chain.invoke({
        "chat_history": chat_history,
        "input": question,
    })
    console.print(f"[green]AI: {result}[/green]")

# ==============================
# 4. 摘要 vs 缓冲记忆对比
# ==============================

console.print("\n[bold]4. 摘要 vs 缓冲记忆对比[/bold]", style="cyan")

print("""
┌──────────────────┬─────────────────────┬─────────────────────┐
│                  │ ConversationBuffer  │ ConversationSummary │
├──────────────────┼─────────────────────┼─────────────────────┤
│ 信息保留         │ 完整保留            │ 压缩为摘要          │
│ Token 消耗       │ 随对话线性增长      │ 基本恒定            │
│ 细节准确度       │ 高（原文保留）      │ 中（可能丢失细节）  │
│ 额外 API 调用    │ 无                  │ 每次更新都要调 LLM  │
│ 适用场景         │ 短对话/需要精确回忆 │ 长对话/节省 token    │
│ 最大容量         │ 受模型上下文限制    │ 理论上无限          │
└──────────────────┴─────────────────────┴─────────────────────┘
""")

console.print("✅ ConversationSummaryMemory 演示完成！", style="bold green")