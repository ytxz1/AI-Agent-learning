"""
Day 8 - LangChain 入门：简单 Chain（链）

Chain 是 LangChain 的核心概念。
它将 Prompt → LLM → OutputParser 串联成一条流水线。
你可以把多个处理步骤像管道一样连接起来。

知识点：
1. 基本 Chain（管道操作符 |）
2. 多步 Chain（链式组合）
3. RunnableLambda（自定义处理）
4. RunnableParallel（并行执行）
5. 翻译链实战
"""

# ==============================
# 导入所需模块
# ==============================

# ChatOpenAI: LangChain 的 Chat 模型封装
from langchain_openai import ChatOpenAI

# ChatPromptTemplate: 对话提示词模板
from langchain_core.prompts import ChatPromptTemplate

# StrOutputParser: 字符串解析器，把 AIMessage 转为纯文本
# JsonOutputParser: JSON 解析器，把 LLM 输出转为字典
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# RunnablePassthrough: 透传数据（原样传递输入，不做任何处理）
# RunnableLambda: 将普通 Python 函数包装成 Runnable，可以放入链中
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# 配置变量
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

# Rich: 终端美化输出库，让控制台输出更好看
from rich.console import Console    # 控制台对象
from rich.panel import Panel        # 面板组件，给输出加边框
from rich.markdown import Markdown  # Markdown 渲染，让输出支持 Markdown 格式

# 创建 LLM 实例
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,       # API 密钥
    base_url=OPENAI_BASE_URL,     # DeepSeek API 地址
    model=MODEL_NAME,             # 模型名称
    temperature=0.7,              # 温度参数
)

# 创建 Rich 控制台对象，用于美化终端输出
console = Console()

# 打印标题
print("=" * 50)
print("Day 8 - 简单 Chain 链")
print("=" * 50)

# ==============================
# 1. 最简单的 Chain
# ==============================

# Chain 就是用 | 管道操作符把多个组件连接起来
# 数据从左到右流动，就像 Unix 管道：cat file | grep pattern | sort
# 这里：输入 → prompt格式化 → LLM生成 → parser解析 → 字符串输出
console.print("\n[bold]1. 最简单的 Chain[/bold]", style="cyan")

# 创建提示词模板
simple_prompt = ChatPromptTemplate.from_template(
    "请用{style}的风格写一段关于{topic}的描述，100字以内。"
)

# 用 | 连接三个组件，形成一条链
# prompt → LLM → StrOutputParser（把 AIMessage 转为 str）
simple_chain = simple_prompt | llm | StrOutputParser()

# 调用链，传入变量
# invoke() 会依次执行：格式化prompt → 调用LLM → 解析输出
result = simple_chain.invoke({"style": "幽默", "topic": "Python编程"})
# result 是字符串类型
console.print(Panel(result, title="幽默风格", border_style="green"))

# ==============================
# 2. 多步 Chain（链式组合）
# ==============================

# 核心思想：上一步的输出，可以作为下一步的输入
# 这里演示：先生成大纲，再根据大纲写文章
console.print("\n[bold]2. 多步 Chain（链式组合）[/bold]", style="cyan")

# 第一步的提示词：生成大纲
outline_prompt = ChatPromptTemplate.from_template(
    "为以下主题生成一个简短的文章大纲（3-5个要点）：{topic}"
)

# 第二步的提示词：根据大纲写内容
# {outline} 变量接收第一步的输出
write_prompt = ChatPromptTemplate.from_template(
    "根据以下大纲，写一篇简短的文章：\n\n{outline}"
)

# 分别构建两条独立的链
outline_chain = outline_prompt | llm | StrOutputParser()  # 大纲链
write_chain = write_prompt | llm | StrOutputParser()      # 写作链

# 组合成完整链：
# {"outline": outline_chain} 意思是：
#   1. 先执行 outline_chain，结果存入 "outline" 变量
#   2. 再把 "outline" 传给 write_chain
# 这是 LangChain 的"扇出"（fan-out）语法
full_chain = (
    {"outline": outline_chain}  # 第一步：生成大纲
    | write_chain               # 第二步：根据大纲写内容
)

# 调用完整链
result = full_chain.invoke({"topic": "为什么Python适合初学者"})
# result 是最终的文章文本（Markdown 渲染显示）
console.print(Panel(Markdown(result), title="链式输出结果", border_style="green"))

# ==============================
# 3. 带有中间处理的 Chain
# ==============================

# 有时候需要在链中加入自定义的 Python 逻辑
# 比如：统计字数、格式化文本、调用外部 API 等
# 用 RunnableLambda 可以把任何函数包装成 Runnable（可执行组件）
console.print("\n[bold]3. 带中间处理的 Chain[/bold]", style="cyan")

def word_counter(text: str) -> str:
    """
    自定义函数：统计字数并附加到文本末尾
    这个函数会在 LLM 输出之后执行
    """
    char_count = len(text)  # 统计字符数
    return f"{text}\n\n---\n📊 字数统计：共 {char_count} 个字符"

# 链：prompt → LLM → 字符串解析 → 字数统计
# RunnableLambda(word_counter) 把 word_counter 函数包装成链的一个节点
word_count_chain = simple_prompt | llm | StrOutputParser() | RunnableLambda(word_counter)

# 调用链
result = word_count_chain.invoke({"style": "学术", "topic": "深度学习"})
console.print(Panel(result, title="带字数统计", border_style="green"))

# ==============================
# 4. 并行 Chain（fan-out / fan-in）
# ==============================

# 核心思想：同一个输入，同时走多条路径，最后合并结果
# 类比：同时问两个人同一个问题，然后汇总他们的回答
console.print("\n[bold]4. 并行 Chain[/bold]", style="cyan")

# 创建两条独立的链：一条分析优点，一条分析缺点
pros_prompt = ChatPromptTemplate.from_template(
    "列出{language}的3个优点，用编号列表。"
)
cons_prompt = ChatPromptTemplate.from_template(
    "列出{language}的3个缺点，用编号列表。"
)

pros_chain = pros_prompt | llm | StrOutputParser()  # 优点链
cons_chain = cons_prompt | llm | StrOutputParser()  # 缺点链

def combine_pros_cons(pros_cons: dict) -> str:
    """
    合并函数：把并行执行的结果合并成一个字符串
    pros_cons 是一个字典，包含两条链的输出：
      pros_cons["pros"] = 优点分析结果
      pros_cons["cons"] = 缺点分析结果
    """
    return f"✅ 优点：\n{pros_cons['pros']}\n\n❌ 缺点：\n{pros_cons['cons']}"

# RunnableParallel: 同时执行多个链
# pros 和 cons 两个 key 对应的链会并行执行
# 结果会合并成 {"pros": "...", "cons": "..."} 字典
from langchain_core.runnables import RunnableParallel

# 完整链：并行执行 → 合并结果
parallel_chain = RunnableParallel(
    pros=pros_chain,      # 并行路径1：分析优点
    cons=cons_chain,      # 并行路径2：分析缺点
) | combine_pros_cons     # 合并两个结果

# 调用链
result = parallel_chain.invoke({"language": "Java"})
console.print(Panel(result, title="Java 优缺点分析", border_style="green"))

# ==============================
# 5. 实战：构建一个简单的翻译链
# ==============================

# 综合运用今天学到的知识，构建一个实用的翻译工具
console.print("\n[bold]5. 实战：翻译链[/bold]", style="cyan")

# 翻译提示词模板
translate_prompt = ChatPromptTemplate.from_messages([
    # 系统消息：设定翻译角色和规则
    ("system", "你是一个专业翻译。将用户输入翻译成{target_language}。只输出翻译结果，不要解释。"),
    # 用户消息：{text} 是待翻译的文本
    ("human", "{text}"),
])

# 翻译链：提示词 → LLM → 字符串解析
translate_chain = translate_prompt | llm | StrOutputParser()

# 测试数据：(原文, 目标语言)
texts = [
    ("你好，世界！", "英文"),           # 中→英
    ("Artificial Intelligence", "中文"),  # 英→中
    ("我喜欢编程", "日文"),             # 中→日
]

# 逐条翻译并输出
for text, lang in texts:
    result = translate_chain.invoke({
        "text": text,                  # 待翻译文本
        "target_language": lang        # 目标语言
    })
    console.print(f"  {text} → [{lang}] {result}")

# 演示完成
console.print("\n✅ Chain 链演示完成！", style="bold green")