"""
Day 8 - LangChain 入门：现代 Chain API（Runnable 接口）

LangChain 0.2+ 使用 Runnable 接口统一了所有组件。
每个 Runnable 都有 invoke / stream / batch / ainvoke 方法。
这是 LangChain 最新的设计范式。

知识点：
1. RunnableSequence - 显式创建链
2. RunnablePassthrough - 透传数据
3. RunnableLambda - 自定义函数处理
4. 缓存链的实现
5. 调试技巧
"""

# ==============================
# 导入所需模块
# ==============================

# ChatOpenAI: Chat 模型封装
from langchain_openai import ChatOpenAI

# ChatPromptTemplate: 对话提示词模板
from langchain_core.prompts import ChatPromptTemplate

# StrOutputParser: 字符串解析器
# JsonOutputParser: JSON 解析器（本文件未使用，但导入备用）
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# RunnablePassthrough: 透传数据，原样传递输入不做处理
# RunnableLambda: 把普通 Python 函数包装成 Runnable（可执行组件）
# RunnableParallel: 并行执行多个链
# RunnableSequence: 显式创建顺序执行的链（和 | 操作符等价）
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel,
    RunnableSequence,
)

# 配置变量
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

# Rich 控制台，用于美化终端输出
from rich.console import Console

# 创建 LLM 实例
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,       # API 密钥
    base_url=OPENAI_BASE_URL,     # DeepSeek API 地址
    model=MODEL_NAME,             # 模型名称
    temperature=0.7,              # 温度参数
)

# 创建 Rich 控制台
console = Console()

# 打印标题
print("=" * 50)
print("Day 8 - 现代 Chain API（Runnable 接口）")
print("=" * 50)

# ==============================
# 1. RunnableSequence - 显式创建链
# ==============================

# RunnableSequence 是链的底层实现
# prompt | llm | parser 其实就是 RunnableSequence(prompt, llm, parser)
# 两种写法完全等价，但 | 操作符更简洁直观
console.print("\n[bold]1. RunnableSequence[/bold]", style="cyan")

# 创建提示词模板
prompt = ChatPromptTemplate.from_template("用一句话解释{concept}")
# 创建字符串解析器
parser = StrOutputParser()

# 方式一：用 | 操作符（推荐，更简洁）
chain = prompt | llm | parser

# 方式二：用 RunnableSequence 显式创建（等价）
# chain = RunnableSequence(prompt, llm, parser)

# 调用链
result = chain.invoke({"concept": "面向对象编程"})
console.print(f"结果: {result}\n", style="green")

# ==============================
# 2. RunnablePassthrough - 透传数据
# ==============================

# RunnablePassthrough 把输入原样传递给下一个组件
# 作用：在并行链中保留原始输入，不影响其他路径的处理
# 类比：你传什么给它，它就原封不动地传给下一个人
console.print("[bold]2. RunnablePassthrough[/bold]", style="cyan")

# 解释提示词：输入 topic，输出详细解释
explain_prompt = ChatPromptTemplate.from_template(
    "用一段话解释{topic}"
)
# 摘要提示词：输入 topic（实际是一段文本），输出压缩后的一句话
summary_prompt = ChatPromptTemplate.from_template(
    "把以下内容压缩成一句话：{explanation}"
)

# 链的结构：
# 第一层：并行执行
#   - explanation 路径：topic → 解释 → LLM → 输出详细解释
#   - original 路径：topic → 直接透传（保留原始输入）
# 第二层：字典映射
#   - summary 路径：用详细解释生成一句话摘要
#   - explanation 路径：用 lambda 从上一层结果中提取详细解释
chain = (
    RunnableParallel(
        explanation=explain_prompt | llm | parser,  # 路径1：生成详细解释
        original=RunnablePassthrough(),              # 路径2：透传原始输入
    )
    | {
        "summary": summary_prompt | llm | parser,          # 用解释生成摘要
        "explanation": lambda x: x["explanation"],          # 提取详细解释
    }
)

# 调用链
result = chain.invoke({"topic": "递归算法"})
console.print(f"详细解释: {result['explanation']}", style="yellow")
console.print(f"一句话摘要: {result['summary']}\n", style="green")

# ==============================
# 3. RunnableLambda - 自定义处理
# ==============================

# RunnableLambda 可以把任何 Python 函数包装成 Runnable
# 这样自定义函数就可以和其他 LangChain 组件用 | 连接
# 适用场景：数据预处理、后处理、调用外部 API 等
console.print("[bold]3. RunnableLambda[/bold]", style="cyan")

def preprocess_input(text: str) -> dict:
    """
    预处理输入：去掉首尾空格，转小写
    输入：字符串 "  机器学习  "
    输出：字典 {"topic": "机器学习"}
    """
    return {"topic": text.strip().lower()}

def postprocess_output(text: str) -> str:
    """
    后处理输出：去掉换行符，去掉首尾空格
    输入：多行字符串
    输出：单行字符串
    """
    return text.replace("\n", " ").strip()

# 链的结构：
# 输入字符串 → 预处理 → 格式化prompt → LLM → 解析 → 后处理
# 每一步都是 Runnable，用 | 连接
chain = (
    RunnableLambda(preprocess_input)                                    # 预处理
    | ChatPromptTemplate.from_template("简单介绍{topic}")               # 格式化
    | llm                                                               # 调用 LLM
    | StrOutputParser()                                                 # 解析
    | RunnableLambda(postprocess_output)                                # 后处理
)

# 调用链
result = chain.invoke("  机器学习  ")  # 有前后空格
console.print(f"结果: {result}\n", style="green")

# ==============================
# 4. 带缓存的 Chain
# ==============================

# 缓存可以避免重复调用 API，节省时间和费用
# 原理：把相同输入的结果存入字典，下次直接返回
console.print("[bold]4. 带缓存的 Chain[/bold]", style="cyan")

# 缓存字典：key=问题, value=回答
cache = {}

def cached_llm(input_dict: dict) -> str:
    """
    带缓存的 LLM 调用函数
    参数 input_dict 示例: {"question": "Python是什么"}
    返回：LLM 的回答字符串
    """
    key = input_dict["question"]  # 用问题作为缓存 key

    # 检查缓存是否命中
    if key in cache:
        console.print("  [缓存命中]", style="yellow")
        return cache[key]  # 直接返回缓存结果，不调用 API

    # 缓存未命中，正常调用 LLM
    console.print("  [新请求]", style="cyan")
    chain = (
        ChatPromptTemplate.from_template("{question}")
        | llm
        | StrOutputParser()
    )
    result = chain.invoke(input_dict)
    cache[key] = result  # 存入缓存
    return result

# 第一次调用：缓存未命中，调用 API
result1 = cached_llm({"question": "Python是什么"})
console.print(f"第一次: {result1}\n", style="green")

# 第二次调用：缓存命中，直接返回
result2 = cached_llm({"question": "Python是什么"})
console.print(f"第二次: {result2}\n", style="green")

# ==============================
# 5. 调试 Chain
# ==============================

# LangChain 提供了多种调试方式
# 1. 打印中间结果
# 2. 使用 LangSmith 追踪平台（可视化查看每一步）
console.print("[bold]5. Chain 调试[/bold]", style="cyan")

# 一个简单的链
chain = (
    ChatPromptTemplate.from_template("用一句话介绍{topic}")
    | llm
    | StrOutputParser()
)

# 调试方法1：直接打印结果
result = chain.invoke({"topic": "RAG"})
console.print(f"结果: {result}\n", style="green")

# 调试方法2：使用 LangSmith（需要注册账号）
# LangSmith 可以可视化查看链的每一步输入输出，非常适合调试复杂链
console.print("💡 提示：使用 LangSmith 可以可视化查看每一步的输入输出", style="dim")
console.print("   注册地址: https://smith.langchain.com\n", style="dim")

# 演示完成
console.print("✅ 现代 Chain API 演示完成！", style="bold green")