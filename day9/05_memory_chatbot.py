"""
Day 9 - Memory 记忆：带记忆的聊天机器人（综合实战）

整合所有记忆知识，构建一个完整的多轮对话聊天机器人。
功能：
1. 自动记住对话历史
2. 支持多种记忆模式切换
3. 显示记忆状态
4. 支持清空记忆

知识点综合运用：
- ConversationBufferMemory
- ConversationBufferWindowMemory
- ConversationSummaryMemory
- MessagesPlaceholder
- Chain 链式调用
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryMemory,
)
from langchain_core.output_parsers import StrOutputParser
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=MODEL_NAME,
    temperature=0.7,
)

parser = StrOutputParser()
console = Console()

# ==============================
# 创建不同类型的 Memory
# ==============================

# 模式1：完整记忆（保留所有对话）
# 这个不需要llm，因为它只是简单地保存对话历史，不进行任何处理。
buffer_memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history",
)

# 模式2：窗口记忆（保留最近5轮）
# 这个也不需要llm，因为它只是保留最近的对话历史，不进行任何处理。
window_memory = ConversationBufferWindowMemory(
    k=5,
    return_messages=True,
    memory_key="chat_history",
)

# 模式3：摘要记忆（压缩为摘要）
# 这个需要llm，因为它会根据对话历史生成摘要。
summary_memory = ConversationSummaryMemory(
    llm=llm,
    return_messages=True,
    memory_key="chat_history",
)

# 记忆模式映射
memory_modes = {
    "1": ("完整记忆", buffer_memory),
    "2": ("窗口记忆(k=5)", window_memory),
    "3": ("摘要记忆", summary_memory),
}

# 当前使用的记忆（默认完整记忆）
current_mode = "1"
current_memory = buffer_memory

# ==============================
# 提示词模板
# ==============================

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "你是一个友好的AI助手。你会记住用户说过的信息。\n"
     "如果用户问你之前说过什么，根据记忆如实回答。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

chain = prompt | llm | parser

# ==============================
# 辅助函数
# ==============================

def show_menu():
    """显示功能菜单"""
    table = Table(title="Day 9 带记忆的聊天机器人", show_header=True)
    table.add_column("编号", style="cyan", width=6)
    table.add_column("功能", style="green", width=14)
    table.add_column("说明", style="white")

    table.add_row("1-3", "切换记忆模式", "完整/窗口/摘要")
    table.add_row("4", "查看记忆", "显示当前记忆内容")
    table.add_row("5", "清空记忆", "清除所有对话历史")
    table.add_row("c", "继续对话", "直接输入内容开始聊天")
    table.add_row("q", "退出", "退出程序")

    console.print(table)

def get_response(user_input):
    """获取 AI 回复"""
    chat_history = current_memory.load_memory_variables({})["chat_history"]
    result = chain.invoke({
        "chat_history": chat_history,
        "input": user_input,
    })
    # 保存到记忆
    current_memory.chat_memory.add_user_message(user_input)
    current_memory.chat_memory.add_ai_message(result)
    return result

def show_memory():
    """显示当前记忆内容"""
    messages = current_memory.load_memory_variables({})["chat_history"]
    if not messages:
        console.print("当前记忆为空", style="yellow")
        return
    console.print(f"\n当前记忆（{memory_modes[current_mode][0]}）：", style="cyan")
    for i, msg in enumerate(messages, 1):
        role = "用户" if msg.type == "human" else "AI"
        style = "bold" if msg.type == "human" else "green"
        console.print(f"  {i}. [{role}] {msg.content}", style=style)

# ==============================
# 主程序
# ==============================

def main():
    global current_mode, current_memory
    console.print(
        Panel.fit(
            "Day 9 - 带记忆的聊天机器人\n"
            "支持三种记忆模式：完整记忆 / 窗口记忆 / 摘要记忆",
            style="bold green"
        )
    )

    # 显示当前模式
    mode_name = memory_modes[current_mode][0]
    console.print(f"当前记忆模式: [cyan]{mode_name}[/cyan]\n")

    while True:
        user_input = input("你: ").strip()

        if not user_input:
            continue

        # 退出
        if user_input.lower() == "q":
            console.print("\n再见！", style="bold red")
            break

        # 切换记忆模式
        if user_input in memory_modes:
            current_mode = user_input
            current_memory = memory_modes[current_mode][1]
            mode_name = memory_modes[current_mode][0]
            console.print(f"已切换到: [cyan]{mode_name}[/cyan]", style="bold yellow")
            continue

        # 查看记忆
        if user_input == "4":
            show_memory()
            continue

        # 清空记忆
        if user_input == "5":
            current_memory.clear()
            console.print("记忆已清空", style="bold yellow")
            continue

        # 正常对话
        with console.status("[bold green]思考中..."):
            result = get_response(user_input)

        console.print(f"AI: {result}\n", style="green")

if __name__ == "__main__":
    main()
