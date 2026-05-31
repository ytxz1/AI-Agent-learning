"""
Day 8 - LangChain 入门：综合实践

这是一个综合示例，将今天学到的所有 LangChain 概念整合到一个完整应用中。
功能：一个智能问答助手，支持多种任务模式。

知识点回顾：
- PromptTemplate / ChatPromptTemplate：提示词模板
- LLM（ChatOpenAI）：大模型调用
- OutputParser（StrOutputParser / JsonOutputParser）：输出解析
- Chain（| 管道操作符）：链式调用
- Rich：终端美化输出

运行方式：
    python main.py
"""

# ==============================
# 导入所需模块
# ==============================

# ChatOpenAI: LangChain 的 Chat 模型封装
from langchain_openai import ChatOpenAI

# ChatPromptTemplate: 对话提示词模板
from langchain_core.prompts import ChatPromptTemplate

# StrOutputParser: 字符串解析器，把 AIMessage 转为纯文本
# JsonOutputParser: JSON 解析器，把 LLM 输出转为 Python 字典
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# 配置变量：API Key、API 地址、模型名称
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

# Rich: 终端美化输出库
from rich.console import Console    # 控制台对象
from rich.panel import Panel        # 面板组件，给文本加边框
from rich.table import Table        # 表格组件，用于显示菜单

# ==============================
# 初始化
# ==============================

# 创建 LLM 实例（全局复用，所有链共用同一个实例）
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,       # 从 .env 读取的 API 密钥
    base_url=OPENAI_BASE_URL,     # DeepSeek API 地址
    model=MODEL_NAME,             # 模型名称：deepseek-chat
    temperature=0.7,              # 温度参数
)

# 创建字符串解析器（全局复用）
parser = StrOutputParser()

# 创建 Rich 控制台对象
console = Console()

# ==============================
# 定义不同的任务链
# ==============================

# 每条链都是一个完整的 Prompt → LLM → Parser 流水线
# 通过不同的提示词实现不同功能

# 链1：通用问答
# 接收 {question} 变量，返回回答文本
qa_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "你是一个知识渊博的助手。用简洁清晰的语言回答问题。"),
        ("human", "{question}")  # 用户问题
    ])
    | llm          # 调用 LLM
    | parser       # 解析为字符串
)

# 链2：代码解释
# 接收 {language}（编程语言）和 {code}（代码内容）两个变量
code_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "你是一个编程老师。请解释以下代码的功能，逐行分析。用中文回答。"),
        # 用 Markdown 代码块包裹代码，让 LLM 更好理解
        ("human", "```{language}\n{code}\n```")
    ])
    | llm
    | parser
)

# 链3：文本摘要
# 接收 {text} 变量，返回 100 字以内的摘要
summary_chain = (
    ChatPromptTemplate.from_template(
        "请对以下文本进行摘要，提取关键信息，控制在100字以内：\n\n{text}"
    )
    | llm
    | parser
)

# 链4：头脑风暴
# 接收 {topic}（主题）和 {count}（数量）两个变量
brainstorm_chain = (
    ChatPromptTemplate.from_template(
        "关于「{topic}」，请给出{count}个创意想法，每个用一句话描述。"
    )
    | llm
    | parser
)

# 链5：格式转换（JSON 输出）
# 使用 JsonOutputParser，输出 Python 字典而不是字符串
# 接收 {topic} 变量，返回 {"title": ..., "description": ..., "feasibility": ...} 格式
json_chain = (
    ChatPromptTemplate.from_messages([
        ("system",
         "你是一个创意顾问。请以 JSON 格式输出创意，包含 title、description、feasibility 三个字段。"
         "只输出 JSON，不要其他内容。"),
        ("human", "关于{topic}的创意")
    ])
    | llm               # 调用 LLM
    | JsonOutputParser() # 解析为字典
)

# ==============================
# 任务路由
# ==============================

def route_task(task_type: str, **kwargs):
    """
    根据任务类型选择对应的链并执行

    参数：
        task_type: 任务类型，可选值：
            "qa"         - 通用问答
            "code"       - 代码解释
            "summary"    - 文本摘要
            "brainstorm" - 头脑风暴
            "json"       - JSON 输出
        **kwargs: 传递给链的变量（如 question、code 等）

    返回：
        链执行的结果（字符串或字典）
    """
    # 任务类型 → 链的映射表
    chains = {
        "qa": qa_chain,
        "code": code_chain,
        "summary": summary_chain,
        "brainstorm": brainstorm_chain,
        "json": json_chain,
    }
    chain = chains.get(task_type)  # 根据类型获取对应的链
    if chain:
        return chain.invoke(kwargs)  # 执行链并返回结果
    return "未知任务类型"

# ==============================
# 启动界面
# ==============================

def show_menu():
    """
    显示功能菜单
    使用 Rich 的 Table 组件，让菜单在终端里显示得更美观
    """
    # 创建表格
    table = Table(title="Day 8 LangChain 智能助手", show_header=True)
    table.add_column("编号", style="cyan", width=6)    # 第1列：编号
    table.add_column("功能", style="green", width=12)  # 第2列：功能名
    table.add_column("说明", style="white")            # 第3列：说明

    # 添加行
    table.add_row("1", "问答", "输入问题，获取回答")
    table.add_row("2", "代码解释", "粘贴代码，获取分析")
    table.add_row("3", "文本摘要", "输入长文本，获取摘要")
    table.add_row("4", "头脑风暴", "输入主题，获取创意")
    table.add_row("5", "JSON 输出", "输入主题，获取结构化创意")
    table.add_row("q", "退出", "退出程序")

    console.print(table)  # 打印表格

def main():
    """
    主函数：交互式智能问答助手
    循环显示菜单，接收用户选择，执行对应功能
    """
    # 显示欢迎面板
    console.print(
        Panel.fit(
            "Day 8 - LangChain 综合实践\n"
            "基于 LangChain 构建的智能问答助手",
            style="bold green"
        )
    )

    # 主循环：持续运行直到用户选择退出
    while True:
        show_menu()  # 显示菜单
        choice = input("\n请选择功能 (1-5, q): ").strip()  # 获取用户输入

        # 退出程序
        if choice == "q":
            console.print("\n再见！", style="bold red")
            break  # 跳出循环

        # 功能1：通用问答
        if choice == "1":
            question = input("请输入问题: ")  # 获取问题
            with console.status("[bold green]思考中..."):  # 显示加载动画
                result = route_task("qa", question=question)  # 调用问答链
            console.print(Panel(result, title="回答", border_style="green"))

        # 功能2：代码解释
        elif choice == "2":
            language = input("编程语言 (如 python): ")  # 获取编程语言
            code = input("请输入代码:\n")               # 获取代码内容
            with console.status("[bold green]分析中..."):
                result = route_task("code", language=language, code=code)
            console.print(Panel(result, title="代码分析", border_style="green"))

        # 功能3：文本摘要
        elif choice == "3":
            text = input("请输入文本:\n")  # 获取待摘要的文本
            with console.status("[bold green]摘要中..."):
                result = route_task("summary", text=text)
            console.print(Panel(result, title="摘要", border_style="green"))

        # 功能4：头脑风暴
        elif choice == "4":
            topic = input("请输入主题: ")                    # 获取主题
            count = input("需要几个想法 (默认5): ") or "5"   # 获取数量，默认5
            with console.status("[bold green]头脑风暴中..."):
                result = route_task("brainstorm", topic=topic, count=count)
            console.print(Panel(result, title="创意想法", border_style="green"))

        # 功能5：JSON 输出
        elif choice == "5":
            topic = input("请输入主题: ")  # 获取主题
            with console.status("[bold green]生成中..."):
                result = route_task("json", topic=topic)
            # result 是字典类型，用 str() 转为字符串显示
            console.print(Panel(str(result), title="结构化创意 (JSON)", border_style="green"))

        # 无效选择
        else:
            console.print("无效选择，请重新输入", style="red")

        print()  # 每次操作后空一行，提升可读性

# 程序入口
if __name__ == "__main__":
    main()