"""
Day 8 - LangChain 入门：PromptTemplate 提示词模板

PromptTemplate 允许你定义可复用的提示词模板，
通过填充变量来生成不同的提示词，避免硬编码。

知识点：
1. PromptTemplate - 纯文本模板
2. ChatPromptTemplate - 对话消息模板
3. Few-shot 示例模板
4. 模板的动态组合
"""

# ==============================
# 导入所需模块
# ==============================

# ChatPromptTemplate: 对话专用模板，生成消息列表（适合 Chat 模型）
# PromptTemplate: 纯文本模板，生成单个字符串（适合普通 LLM）
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

# 从配置文件导入 API 相关变量
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

# ChatOpenAI: LangChain 对 Chat 模型的封装
from langchain_openai import ChatOpenAI

# 创建 LLM 实例，后续示例都会用到
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,       # API 密钥
    base_url=OPENAI_BASE_URL,     # DeepSeek API 地址
    model=MODEL_NAME,             # 模型名称
    temperature=0.7,              # 温度参数
)

# 打印标题
print("=" * 50)
print("Day 8 - PromptTemplate 提示词模板")
print("=" * 50)

# ==============================
# 1. 基本的 PromptTemplate（纯文本）
# ==============================

# PromptTemplate 是最基础的模板类
# template 参数：模板字符串，用 {变量名} 作为占位符
# input_variables 参数：列出所有变量名，用于校验和文档
# format() 方法：填充变量，返回最终字符串
print("\n--- 1. 基本 PromptTemplate ---")
template = PromptTemplate(
    template="请用{language}写一首关于{topic}的诗",  # 模板内容
    input_variables=["language", "topic"],             # 声明变量列表
)

# format 方法把变量填入模板
# 等价于：f"请用{language}写一首关于{topic}的诗"
prompt = template.format(language="中文", topic="春天")
print(f"生成的提示词:\n{prompt}\n")
# 输出: 请用中文写一首关于春天的诗

# 把生成的提示词传给 LLM
# llm.invoke() 接受字符串，LangChain 会自动转成 HumanMessage
response = llm.invoke(prompt)
print(f"AI 回答:\n{response.content}")

# ==============================
# 2. ChatPromptTemplate（对话模板）
# ==============================

# ChatPromptTemplate 专门为 Chat 模型（如 GPT、DeepSeek）设计
# 它生成的是消息列表（而不是单个字符串）
# 每个消息有角色：system（系统设定）、human（用户）、ai（助手）
# from_messages() 是最常用的创建方式
print("\n--- 2. ChatPromptTemplate ---")
chat_template = ChatPromptTemplate.from_messages([
    # 系统消息：设定 AI 的角色和行为
    # {role} 和 {style} 是变量占位符
    ("system", "你是一个{role}，用{style}的语气回答问题。"),
    # 用户消息：{question} 是变量占位符
    ("human", "{question}"),
])

# format_messages() 填充变量，返回 AIMessage / HumanMessage / SystemMessage 列表
# 注意：format() 返回字符串，format_messages() 返回消息对象列表
messages = chat_template.format_messages(
    role="英语老师",       # 填充 {role}
    style="幽默风趣",      # 填充 {style}
    question="如何提高英语口语？"  # 填充 {question}
)

# 打印生成的消息，验证格式
print("生成的消息:")
for msg in messages:
    print(f"  [{msg.type}] {msg.content}")
    # msg.type 可以是 "system"、"human"、"ai"

# 用生成的消息列表调用 LLM
response = llm.invoke(messages)
print(f"\nAI 回答:\n{response.content}")

# ==============================
# 3. Few-shot 示例模板
# ==============================

# Few-shot（少样本）是 Prompt Engineering 的重要技巧
# 在提示词中给几个「输入→输出」示例，引导模型学会你想要的格式
# 比如：翻译任务，先给一个 "你好→Hello" 的示例
print("\n--- 3. Few-shot 模板 ---")
few_shot_template = ChatPromptTemplate.from_messages([
    # 系统消息：定义任务
    ("system", "你是一个翻译助手。请将中文翻译成英文。"),
    # 第1组示例：输入
    ("human", "{chinese}"),
    # 第1组示例：输出（让模型看到参考答案）
    ("ai", "{english}"),
    # 真正的用户输入（模型会模仿上面的示例来翻译）
    ("human", "{input_chinese}"),
])

# 填充示例和实际输入
# 模型看到 "你好→Hello" 的示例后，会按照同样模式翻译 "谢谢"
messages = few_shot_template.format_messages(
    chinese="你好",         # 示例输入
    english="Hello",        # 示例输出
    input_chinese="谢谢"    # 真正的输入
)

response = llm.invoke(messages)
print(f"AI 翻译: {response.content}")
# 期望输出: Thank you

# ==============================
# 4. 模板的组合使用
# ==============================

# 有时候需要把多个模板拼接在一起
# 比如先生成一个"角色设定"，再拼到"问题模板"里
print("\n--- 4. 动态模板组合 ---")

# 模板1：角色设定模板
base_prompt = PromptTemplate(
    template="你是一个{domain}领域的专家。",
    input_variables=["domain"]
)

# 模板2：问题模板，其中 {base} 用来接收模板1的结果
user_prompt = PromptTemplate(
    template="{base}\n请回答：{question}",
    input_variables=["base", "question"]
)

# 手动组合：先填充模板1，再把结果传给模板2
base = base_prompt.format(domain="人工智能")
# base = "你是一个人工智能领域的专家。"

final_prompt = user_prompt.format(
    base=base,                    # 填充角色设定
    question="什么是大语言模型？"  # 填充问题
)
# final_prompt = "你是一个人工智能领域的专家。\n请回答：什么是大语言模型？"
print(f"组合后的提示词:\n{final_prompt}\n")

# 用组合后的提示词调用 LLM
response = llm.invoke(final_prompt)
print(f"AI 回答:\n{response.content}")

# 演示完成
print("\n✅ PromptTemplate 演示完成！")