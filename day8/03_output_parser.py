"""
Day 8 - LangChain 入门：OutputParser 输出解析器

OutputParser 负责将 LLM 的文本输出转换为结构化的 Python 对象。
比如把 JSON 字符串转成字典、把分隔文本转成列表等。

知识点：
1. StrOutputParser - 字符串解析（最基础）
2. CommaSeparatedListOutputParser - 逗号分隔列表
3. JsonOutputParser - JSON 字典
4. PydanticOutputParser - 类型化 JSON（最严格）
"""

# ==============================
# 导入所需模块
# ==============================

from langchain_core.output_parsers import (
    StrOutputParser,                   # 字符串解析器
    JsonOutputParser,                  # JSON 解析器
    CommaSeparatedListOutputParser,   # 逗号分隔列表解析器
)

# ChatPromptTemplate: 对话模板，用于构建提示词
from langchain_core.prompts import ChatPromptTemplate

# BaseModel 和 Field: 用于定义 Pydantic 数据模型
# Pydantic 可以对输出进行严格的类型校验
from pydantic import BaseModel, Field

# ChatOpenAI: LangChain 对 Chat 模型的封装
from langchain_openai import ChatOpenAI

# 配置变量
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

# 创建 LLM 实例
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,       # API 密钥
    base_url=OPENAI_BASE_URL,     # DeepSeek API 地址
    model=MODEL_NAME,             # 模型名称
    temperature=0.7,              # 温度参数
)

# 打印标题
print("=" * 50)
print("Day 8 - OutputParser 输出解析器")
print("=" * 50)

# ==============================
# 1. StrOutputParser（字符串解析器）
# ==============================

# StrOutputParser 是最简单的解析器
# 它只做一件事：从 AIMessage 对象中提取 .content 字符串
# 适用场景：不需要结构化数据，只需要纯文本
print("\n--- 1. StrOutputParser ---")

# 创建一个简单的提示词模板
prompt = ChatPromptTemplate.from_template(
    "用一句话解释什么是{concept}"
)

# 使用 | 管道操作符连接三个组件，形成链（Chain）
# 数据流向：输入 → prompt(格式化) → llm(生成) → parser(解析) → 字符串
chain = prompt | llm | StrOutputParser()
# 等价于：prompt | llm | StrOutputParser()

# 调用链，传入变量
result = chain.invoke({"concept": "机器学习"})
print(f"输出类型: {type(result)}")  # <class 'str'>
print(f"输出内容: {result}")

# ==============================
# 2. CommaSeparatedListOutputParser（逗号分隔列表）
# ==============================

# 这个解析器要求 LLM 输出逗号分隔的文本
# 然后自动把它转成 Python 列表
# 适用场景：需要标签列表、候选答案等
print("\n--- 2. CommaSeparatedListOutputParser ---")
list_parser = CommaSeparatedListOutputParser()

# get_format_instructions() 返回格式说明文本
# 这段文本会告诉 LLM "请用逗号分隔输出多个值"
# 把它放进 prompt 里，LLM 就知道该怎么输出了
format_instructions = list_parser.get_format_instructions()
print(f"格式说明:\n{format_instructions}\n")

# 创建提示词模板
# system 消息中包含格式说明，确保 LLM 按要求输出
prompt = ChatPromptTemplate.from_messages([
    ("system", "列出{count}个{category}相关的概念。{format_instructions}"),
    ("human", "请给我列出{count}个{category}相关的概念"),
])

# 链：prompt → LLM → 列表解析器
chain = prompt | llm | list_parser

# 调用链
result = chain.invoke({
    "count": 5,                              # 要列出 5 个
    "category": "Python编程",                 # 分类：Python编程
    "format_instructions": format_instructions,  # 格式说明
})
print(f"输出类型: {type(result)}")  # <class 'list'>
print(f"输出内容: {result}")
# 期望结果类似: ["变量", "列表", "字典", "函数", "类"]
for i, item in enumerate(result, 1):
    print(f"  {i}. {item}")

# ==============================
# 3. JsonOutputParser（JSON 解析器）
# ==============================

# 这个解析器让 LLM 输出 JSON 格式的文本
# 然后自动解析成 Python 字典
# 适用场景：需要结构化数据，如用户信息、文章结构等
print("\n--- 3. JsonOutputParser ---")
json_parser = JsonOutputParser()

# 同样先获取格式说明，告诉 LLM 输出 JSON
format_instructions = json_parser.get_format_instructions()
print(f"格式说明:\n{format_instructions}\n")

# 提示词模板中包含 JSON 格式说明
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个编程助手。{format_instructions}"),
    ("human", "介绍Python的{count}个特点，包含name和description字段"),
])

# 链：prompt → LLM → JSON 解析器
chain = prompt | llm | json_parser

# 调用链
result = chain.invoke({
    "count": 3,                               # 介绍 3 个特点
    "format_instructions": format_instructions,
})
print(f"输出类型: {type(result)}")  # <class 'dict'>
print(f"输出内容:\n{result}")
# 期望结果类似: {"features": [{"name": "...", "description": "..."}, ...]}

# ==============================
# 4. PydanticOutputParser（结构化解析器）
# ==============================

# 这是最严格的解析器
# 先用 Pydantic 定义输出的字段和类型
# LLM 输出 JSON → 解析器自动校验类型 → 生成 Pydantic 对象
# 如果某个字段类型不对，会报错
# 适用场景：对输出格式要求很高的场景
print("\n--- 4. PydanticOutputParser ---")

# 导入 PydanticOutputParser
from langchain_core.output_parsers import PydanticOutputParser

# 定义输出的数据模型
# 每个字段用 Field() 描述，description 会作为格式说明的一部分
class ProgrammingLanguage(BaseModel):
    """编程语言信息 - 这个 docstring 也会出现在格式说明中"""
    name: str = Field(description="编程语言名称")
    year: int = Field(description="发布年份")
    use_cases: str = Field(description="主要用途")
    difficulty: str = Field(description="学习难度：简单/中等/困难")

# 创建解析器，指定 Pydantic 模型
pydantic_parser = PydanticOutputParser(pydantic_object=ProgrammingLanguage)

# 获取格式说明，里面包含了完整的 JSON Schema 定义
format_instructions = pydantic_parser.get_format_instructions()
print(f"格式说明:\n{format_instructions}\n")

# 提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个编程语言专家。{format_instructions}"),
    ("human", "请介绍{language}这门语言"),
])

# 链：prompt → LLM → Pydantic 解析器
chain = prompt | llm | pydantic_parser

# 调用链
result = chain.invoke({
    "language": "Python",
    "format_instructions": format_instructions,
})
# result 是 ProgrammingLanguage 类型的对象
print(f"输出类型: {type(result)}")  # <class 'ProgrammingLanguage'>
print(f"名称: {result.name}")       # 直接用属性访问
print(f"年份: {result.year}")
print(f"用途: {result.use_cases}")
print(f"难度: {result.difficulty}")

# 演示完成
print("\n✅ OutputParser 演示完成！")