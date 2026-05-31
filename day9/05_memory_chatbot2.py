"""
Day 9 - Memory 记忆：带记忆的聊天机器人（增强版）

在原版基础上新增第四种记忆模式：摘要+窗口组合记忆
其他功能保持不变。

四种记忆模式：
1. 完整记忆 - 保留所有对话
2. 窗口记忆 - 只保留最近5轮
3. 摘要记忆 - 压缩为摘要
4. 摘要+窗口组合记忆 - 短期用窗口保留最近对话，长期用摘要保留整体概要
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
buffer_memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history",
)

# 模式2：窗口记忆（保留最近5轮）
window_memory = ConversationBufferWindowMemory(
    k=5,
    return_messages=True,
    memory_key="chat_history",
)

# 模式3：摘要记忆（压缩为摘要）
summary_memory = ConversationSummaryMemory(
    llm=llm,
    return_messages=True,
    memory_key="chat_history",
)

# 模式4：摘要+窗口组合记忆
# 短期记忆：保留最近3轮的详细对话
short_memory = ConversationBufferWindowMemory(
    k=3,
    return_messages=True,
    memory_key="short_history",
)
# 长期记忆：保留所有对话的摘要
long_memory = ConversationSummaryMemory(
    llm=llm,
    return_messages=True,
    memory_key="long_history",
)
# 组合两种记忆
combined_memory = CombinedMemory(
    memories=[short_memory, long_memory]
)

# 记忆模式映射
memory_modes = {
    "1": ("完整记忆", buffer_memory),
    "2": ("窗口记忆(k=5)", window_memory),
    "3": ("摘要记忆", summary_memory),
    "4": ("摘要+窗口组合", combined_memory),
}

# 当前使用的记忆（默认完整记忆）
current_mode = "1"
current_memory = buffer_memory

# ==============================
# 提示词模板
# ==============================

# 模式1/2/3 用的提示词（单个 chat_history）
prompt_single = ChatPromptTemplate.from_messages([
    ("system",
     "你是一个友好的AI助手。你会记住用户说过的信息。\n"
     "如果用户问你之前说过什么，根据记忆如实回答。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

# 模式4 用的提示词（两个占位符：短期 + 长期）
prompt_combined = ChatPromptTemplate.from_messages([
    ("system",
     "你是一个友好的AI助手。\n"
     "以下是最近的对话记录（短期记忆）：\n"
     "{short_history}\n"
     "以下是之前的对话摘要（长期记忆）：\n"
     "{long_history}\n"
     "请根据以上记忆回答用户的问题。"),
    ("human", "{input}"),
])

# 根据模式选择对应的提示词和 Chain
def get_chain():
    if current_mode == "4":
        return prompt_combined | llm | parser
    return prompt_single | llm | parser

# ==============================
# 辅助函数
# ==============================

def show_menu():
    """显示功能菜单"""
    table = Table(title="Day 9 带记忆的聊天机器人（增强版）", show_header=True)
    table.add_column("编号", style="cyan", width=6)
    table.add_column("功能", style="green", width=14)
    table.add_column("说明", style="white")

    table.add_row("1", "完整记忆", "保留所有对话")
    table.add_row("2", "窗口记忆", "保留最近5轮")
    table.add_row("3", "摘要记忆", "压缩为摘要")
    table.add_row("4", "摘要+窗口组合", "短期窗口+长期摘要")
    table.add_row("look", "查看记忆", "显示当前记忆内容")
    table.add_row("clear", "清空记忆", "清除所有对话历史")
    table.add_row("q", "退出", "退出程序")

    console.print(table)

def get_response(user_input):
    """获取 AI 回复"""
    chain = get_chain()

    if current_mode == "4":
        # 组合记忆模式：需要加载两个记忆
        short_hist = short_memory.load_memory_variables({})["short_history"]
        long_hist = long_memory.load_memory_variables({})["long_history"]
        result = chain.invoke({
            "short_history": short_hist,
            "long_history": long_hist,
            "input": user_input,
        })
        # 保存到两个记忆中
        short_memory.chat_memory.add_user_message(user_input)
        short_memory.chat_memory.add_ai_message(result)
        long_memory.chat_memory.add_user_message(user_input)
        long_memory.chat_memory.add_ai_message(result)
    else:
        # 普通模式：加载单个记忆
        chat_history = current_memory.load_memory_variables({})["chat_history"]
        result = chain.invoke({
            "chat_history": chat_history,
            "input": user_input,
        })
        current_memory.chat_memory.add_user_message(user_input)
        current_memory.chat_memory.add_ai_message(result)

    return result

def show_memory():
    """显示当前记忆内容"""
    if current_mode == "4":
        # 组合记忆模式：显示两个记忆
        short_msgs = short_memory.load_memory_variables({})["short_history"]
        long_msgs = long_memory.load_memory_variables({})["long_history"]

        console.print("\n当前记忆 - 摘要+窗口组合", style="cyan")

        console.print("\n短期记忆（最近3轮）：", style="bold")
        if short_msgs:
            for i, msg in enumerate(short_msgs, 1):
                role = "用户" if msg.type == "human" else "AI"
                s = "bold" if msg.type == "human" else "green"
                console.print(f"  {i}. [{role}] {msg.content}", style=s)
        else:
            console.print("  (空)")

        console.print("\n长期记忆（摘要）：", style="bold")
        if long_msgs:
            console.print(f"  {long_msgs[0].content}", style="green")
        else:
            console.print("  (空)")
    else:
        # 普通模式：显示单个记忆
        messages = current_memory.load_memory_variables({})["chat_history"]
        if not messages:
            console.print("当前记忆为空", style="yellow")
            return
        mode_name = memory_modes[current_mode][0]
        console.print(f"\n当前记忆（{mode_name}）：", style="cyan")
        for i, msg in enumerate(messages, 1):
            role = "用户" if msg.type == "human" else "AI"
            s = "bold" if msg.type == "human" else "green"
            console.print(f"  {i}. [{role}] {msg.content}", style=s)

def clear_memory():
    """清空当前记忆"""
    if current_mode == "4":
        short_memory.clear()
        long_memory.clear()
    else:
        current_memory.clear()

# ==============================
# 主程序
# ==============================

def main():
    global current_mode, current_memory
    console.print(
        Panel.fit(
            "Day 9 - 带记忆的聊天机器人（增强版）\n"
            "支持四种记忆模式：完整 / 窗口 / 摘要 / 摘要+窗口组合",
            style="bold green"
        )
    )

    show_menu()
    mode_name = memory_modes[current_mode][0]
    console.print(f"\n当前记忆模式: [cyan]{mode_name}[/cyan]\n")

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
        if user_input == "look":
            show_memory()
            continue

        # 清空记忆
        if user_input == "clear":
            clear_memory()
            console.print("记忆已清空", style="bold yellow")
            continue

        # 正常对话
        with console.status("[bold green]思考中..."):
            result = get_response(user_input)

        console.print(f"AI: {result}\n", style="green")

if __name__ == "__main__":
    main()
