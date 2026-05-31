"""
Day 9 - Memory 记忆：综合实践 - 智能记忆助手

将今天所有 Memory 知识整合到一个完整的交互式应用中。
功能：支持多种记忆模式的智能问答助手。

运行方式：
    python main.py
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryMemory,
    CombinedMemory,
)
from langchain_core.output_parsers import StrOutputParser
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# ==============================
# 初始化
# ==============================

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=MODEL_NAME,
    temperature=0.7,
)

parser = StrOutputParser()
console = Console()

# ==============================
# 创建记忆实例
# ==============================

# 完整记忆：保留所有对话
buffer_memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history",
)

# 窗口记忆：保留最近 5 轮
window_memory = ConversationBufferWindowMemory(
    k=5,
    return_messages=True,
    memory_key="chat_history",
)

# 摘要记忆：压缩为摘要
summary_memory = ConversationSummaryMemory(
    llm=llm,
    return_messages=True,
    memory_key="chat_history",
)

# 记忆模式映射
modes = {
    "1": ("完整记忆（Buffer）", buffer_memory, "保留所有对话，信息零丢失，但 token 消耗大"),
    "2": ("窗口记忆（Window k=5）", window_memory, "只保留最近5轮对话，平衡性能和上下文"),
    "3": ("摘要记忆（Summary）", summary_memory, "压缩为摘要，省 token，但可能丢失细节"),
}

# 当前状态
current_mode = "1"
current_name, current_memory, _ = modes[current_mode]

# 对话计数器
turn_count = 0

# ==============================
# 提示词模板
# ==============================

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "你是一个聪明且友好的AI助手。\n"
     "你会记住用户说过的所有重要信息。\n"
     "如果用户问你之前说过什么，请根据记忆如实回答。\n"
     "回答简洁、自然、友好。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

chain = prompt | llm | parser

# ==============================
# 核心函数
# ==============================

def get_ai_response(user_input):
    """获取 AI 回复并更新记忆"""
    global turn_count

    chat_history = current_memory.load_memory_variables({})["chat_history"]
    result = chain.invoke({
        "chat_history": chat_history,
        "input": user_input,
    })

    current_memory.chat_memory.add_user_message(user_input)
    current_memory.chat_memory.add_ai_message(result)
    turn_count += 1

    return result

def show_menu():
    """显示功能菜单"""
    table = Table(title="Day 9 智能记忆助手", show_header=True)
    table.add_column("选项", style="cyan", width=8)
    table.add_column("功能", style="green", width=14)
    table.add_column("说明", style="white")

    table.add_row("1/2/3", "切换记忆模式", "完整 / 窗口 / 摘要")
    table.add_row("4", "查看记忆", "显示当前记忆内容")
    table.add_row("5", "清空记忆", "清除所有对话历史")
    table.add_row("6", "查看统计", "显示对话轮数和记忆条数")
    table.add_row("直接输入", "对话", "和 AI 聊天")
    table.add_row("q", "退出", "退出程序")

    console.print(table)

def show_memory_content():
    """显示当前记忆的详细内容"""
    messages = current_memory.load_memory_variables({})["chat_history"]
    if not messages:
        console.print("当前记忆为空", style="yellow")
        return

    console.print(f"\n[bold cyan]当前记忆 - {current_name}[/bold cyan]")
    console.print(f"共 {len(messages)} 条消息：\n")

    for i, msg in enumerate(messages, 1):
        if msg.type == "human":
            console.print(f"  {i}. [用户] {msg.content}", style="bold")
        else:
            console.print(f"  {i}. [AI]   {msg.content}", style="green")

def show_stats():
    """显示统计信息"""
    messages = current_memory.load_memory_variables({})["chat_history"]
    user_count = sum(1 for m in messages if m.type == "human")
    ai_count = sum(1 for m in messages if m.type == "ai")

    table = Table(title="对话统计", show_header=True)
    table.add_column("指标", style="cyan")
    table.add_column("值", style="green")

    table.add_row("当前模式", current_name)
    table.add_row("总对话轮数", str(turn_count))
    table.add_row("记忆中用户消息", str(user_count))
    table.add_row("记忆中AI回复", str(ai_count))
    table.add_row("记忆总条数", str(len(messages)))

    console.print(table)

# ==============================
# 主程序
# ==============================

def main():
    global current_mode, current_name, current_memory
    console.print(
        Panel.fit(
            "Day 9 - 智能记忆助手\n"
            "支持三种记忆模式，让 AI 记住你说过的每一句话",
            style="bold green"
        )
    )

    show_menu()
    console.print(f"\n当前模式: [cyan]{current_name}[/cyan]\n")

    while True:
        user_input = input("你: ").strip()

        if not user_input:
            continue

        # 退出
        if user_input.lower() == "q":
            console.print("\n再见！", style="bold red")
            break

        # 切换模式
        if user_input in modes:
            current_mode = user_input
            current_name, current_memory, desc = modes[current_mode]
            console.print(f"已切换到: [cyan]{current_name}[/cyan]", style="bold yellow")
            console.print(f"  说明: {desc}\n")
            continue

        # 查看记忆
        if user_input == "4":
            show_memory_content()
            continue

        # 清空记忆
        if user_input == "5":
            current_memory.clear()
            console.print("记忆已清空", style="bold yellow")
            continue

        # 查看统计
        if user_input == "6":
            show_stats()
            continue

        # 对话
        with console.status("[bold green]思考中..."):
            result = get_ai_response(user_input)

        console.print(f"AI: {result}\n", style="green")

if __name__ == "__main__":
    main()
