# Day 8 - LangChain 入门：LLM、Prompt、OutputParser 与 Chain

> **学习目标**：掌握 LangChain 框架基础，学会使用 LLM、PromptTemplate、OutputParser 和 Chain 构建应用。

---

## 目录

1. [什么是 LangChain](#1-什么是-langchain)
2. [环境准备](#2-环境准备)
3. [LLM 基础调用](#3-llm-基础调用)
4. [PromptTemplate 提示词模板](#4-prompttemplate-提示词模板)
5. [OutputParser 输出解析器](#5-outputparser-输出解析器)
6. [简单 Chain 链](#6-简单-chain-链)
7. [现代 Runnable API](#7-现代-runnable-api)
8. [综合实践项目](#8-综合实践项目)
9. [常见问题](#9-常见问题)
10. [知识总结](#10-知识总结)

---

## 1. 什么是 LangChain

### 1.1 概念介绍

**LangChain** 是一个用于构建大语言模型（LLM）应用的开源框架。它的核心思想是**将复杂的 LLM 应用拆解为可组合的模块**。

```
用户输入 → Prompt模板 → LLM模型 → 输出解析 → 结构化结果
```

### 1.2 为什么用 LangChain

直接调用 OpenAI/DeepSeek API 也可以做很多事，但随着项目复杂度增加：

| 问题 | 直接调 API | 用 LangChain |
|------|-----------|-------------|
| 提示词管理 | 硬编码在代码里 | 模板化，可复用 |
| 输出格式 | 手动解析字符串 | 内置多种 Parser |
| 链式调用 | 手动拼接逻辑 | `|` 管道操作符一行搞定 |
| 流式输出 | 需要自己写循环 | `.stream()` 一步到位 |
| 缓存/重试 | 自己实现 | 内置支持 |
| Agent/Tool | 从零写起 | 开箱即用 |

### 1.3 LangChain 的核心组件

```
┌─────────────────────────────────────────────────┐
│                  LangChain                       │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  LLM /   │  │  Prompt  │  │  Output  │      │
│  │ ChatModel│  │ Template │  │  Parser  │      │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘      │
│       │              │              │            │
│       └──────────────┼──────────────┘            │
│                      ▼                           │
│               ┌──────────┐                       │
│               │  Chain   │  (管道化组装)         │
│               └──────────┘                       │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Tools   │  │  Memory  │  │  Agent   │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│        (后续课程会学到)                           │
└─────────────────────────────────────────────────┘
```

本节课重点学习：**LLM、PromptTemplate、OutputParser、Chain** 四个核心组件。

---

## 2. 环境准备

### 2.1 创建虚拟环境（推荐）

```bash
cd day8
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2.2 安装依赖

```bash
pip install -r requirements.txt
```

`requirements.txt` 包含：

```
langchain>=0.2.0
langchain-openai>=0.1.0
langchain-community>=0.2.0
python-dotenv>=1.0.0
rich>=13.0.0
```

### 2.3 配置 API Key

创建 `.env` 文件：

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> 本项目使用 **DeepSeek API**（兼容 OpenAI 接口），在 `config.py` 中配置了 `base_url`。

---

## 3. LLM 基础调用

> 对应文件：`01_llm_basic.py`

### 3.1 核心概念

LangChain 用 `ChatOpenAI` 类封装了 OpenAI 兼容的 Chat 模型：

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com",  # DeepSeek API 地址
    model="deepseek-chat",                 # 模型名称
    temperature=0.7,                       # 温度参数
)
```

### 3.2 三种调用方式

#### 方式一：直接传字符串

```python
response = llm.invoke("用一句话介绍你自己")
print(response.content)  # response 是 AIMessage 对象
```

#### 方式二：使用消息列表

```python
from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="你是一个Python老师"),
    HumanMessage(content="什么是列表推导式？"),
]
response = llm.invoke(messages)
```

#### 方式三：流式输出

```python
for chunk in llm.stream("简述Python的三大特性"):
    print(chunk.content, end="", flush=True)
```

### 3.3 返回值结构

`llm.invoke()` 返回的是 `AIMessage` 对象：

```python
# response 对象结构
response.content    # str - 文本内容
response.response_metadata  # dict - 元数据（token数等）
response.usage_metadata     # dict - 用量信息
```

### 3.4 运行示例

```bash
python 01_llm_basic.py
```

输出示例：
```
==================================================
Day 8 - LangChain LLM 基础调用
==================================================

--- 方式一：直接传字符串 ---
AI: 我是一个由OpenAI训练的大型语言模型...

--- 方式二：使用消息列表 ---
AI: 列表推导式是Python中创建列表的简洁语法...
```

---

## 4. PromptTemplate 提示词模板

> 对应文件：`02_prompt_template.py`

### 4.1 为什么需要模板

在 Day 7 的 Function Calling 项目中，我们用 `"""` 多行字符串写 system prompt。
当提示词需要动态变量时，模板化更优雅：

```python
# 没有模板（硬编码）
prompt = f"你是一个{role}，回答关于{topic}的问题"

# 使用模板（可复用）
template = PromptTemplate(
    template="你是一个{role}，回答关于{topic}的问题",
    input_variables=["role", "topic"]
)
prompt = template.format(role="Python老师", topic="装饰器")
```

### 4.2 PromptTemplate（纯文本模板）

```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    template="请用{language}写一首关于{topic}的诗",
    input_variables=["language", "topic"],
)

# 填充变量
prompt = template.format(language="中文", topic="春天")
# 结果: "请用中文写一首关于春天的诗"
```

### 4.3 ChatPromptTemplate（对话模板）

专门为 Chat 模型设计，支持不同类型的消息：

```python
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，用{style}的语气回答问题。"),
    ("human", "{question}"),
])

# format_messages 生成消息对象列表
messages = template.format_messages(
    role="英语老师",
    style="幽默风趣",
    question="如何提高英语口语？"
)
# messages[0] = SystemMessage(content="你是一个英语老师...")
# messages[1] = HumanMessage(content="如何提高英语口语？")
```

### 4.4 Few-shot 模板

在提示词中加入示例，引导模型输出特定格式：

```python
template = ChatPromptTemplate.from_messages([
    ("system", "你是一个翻译助手。"),
    ("human", "{chinese}"),      # 示例输入
    ("ai", "{english}"),          # 示例输出
    ("human", "{input_chinese}"), # 真正的输入
])

messages = template.format_messages(
    chinese="你好",
    english="Hello",
    input_chinese="谢谢"        # 模型应该回答 "Thank you"
)
```

### 4.5 模板 vs 直接写提示词

| 对比项 | 直接写 | PromptTemplate |
|--------|--------|----------------|
| 变量化 | 需要 f-string | `{变量名}` 占位符 |
| 复用性 | 低 | 高 |
| 可视化 | 一般 | `.format()` 可预览 |
| 类型安全 | 无 | `input_variables` 检查 |
| LangChain 集成 | 需手动封装 | 直接与 Chain 连接 |

---

## 5. OutputParser 输出解析器

> 对应文件：`03_output_parser.py`

### 5.1 为什么需要 Parser

LLM 返回的是纯文本字符串，但我们的程序往往需要结构化数据：

```
LLM 输出: "Python, Java, JavaScript, Go, Rust"
     ↓ OutputParser
Python 列表: ["Python", "Java", "JavaScript", "Go", "Rust"]
```

### 5.2 四种常用 Parser

#### (1) StrOutputParser - 字符串

最简单，直接把 `AIMessage.content` 转为字符串：

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
result = parser.invoke(ai_message)
# result 是 str 类型
```

#### (2) CommaSeparatedListOutputParser - 逗号列表

让 LLM 输出逗号分隔的列表，自动解析为 Python list：

```python
from langchain_core.output_parsers import CommaSeparatedListOutputParser

parser = CommaSeparatedListOutputParser()

# 获取格式说明（告诉 LLM 怎么输出）
instructions = parser.get_format_instructions()
# 输出: "Your response should be a list of values separated by commas..."

# 组合使用
chain = prompt | llm | parser
result = chain.invoke({...})
# result 是 list 类型: ["Python", "Java", "JavaScript"]
```

#### (3) JsonOutputParser - JSON

让 LLM 输出 JSON 并自动解析为字典：

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()
instructions = parser.get_format_instructions()
# 输出: "The output should be formatted as a JSON instance..."

chain = prompt | llm | parser
result = chain.invoke({...})
# result 是 dict 类型: {"name": "Python", "year": 1991}
```

#### (4) PydanticOutputParser - 类型化 JSON

最严格的方式，用 Pydantic 模型定义输出结构：

```python
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class Language(BaseModel):
    name: str = Field(description="语言名称")
    year: int = Field(description="发布年份")

parser = PydanticOutputParser(pydantic_object=Language)
chain = prompt | llm | parser
result = chain.invoke({...})
# result 是 Language 对象: result.name, result.year
```

### 5.3 Parser 对比

| Parser | 输出类型 | 适用场景 | 严格程度 |
|--------|---------|---------|---------|
| StrOutputParser | str | 通用文本输出 | 无 |
| CommaSeparatedList | list | 标签、列表 | 中 |
| JsonOutputParser | dict | 结构化数据 | 高 |
| PydanticOutputParser | 对象 | 需要类型校验 | 最高 |

---

## 6. 简单 Chain 链

> 对应文件：`04_simple_chain.py`

### 6.1 什么是 Chain

**Chain（链）** 是 LangChain 的核心概念。它将多个组件用管道 `|` 串联：

```python
chain = prompt | llm | parser
```

就像 Unix 管道 `cat file | grep pattern | sort`，数据从左到右流动。

### 6.2 Chain 的执行流程

```
输入数据 → PromptTemplate(格式化) → LLM(生成) → Parser(解析) → 输出
```

```python
# 最简单的链
chain = (
    ChatPromptTemplate.from_template("解释{topic}")
    | llm
    | StrOutputParser()
)

result = chain.invoke({"topic": "递归"})
# "递归是函数调用自身的编程技巧..."
```

### 6.3 多步 Chain（链式组合）

上一步的输出可以作为下一步的输入：

```python
# 第一步：生成大纲
outline_chain = (
    ChatPromptTemplate.from_template("为{topic}写大纲")
    | llm
    | StrOutputParser()
)

# 第二步：根据大纲写内容
write_chain = (
    ChatPromptTemplate.from_template("根据大纲写文章：{outline}")
    | llm
    | StrOutputParser()
)

# 组合成完整链
full_chain = (
    {"outline": outline_chain}  # 大纲链的结果作为 outline 变量
    | write_chain               # 传入写文章链
)

result = full_chain.invoke({"topic": "Python入门"})
```

### 6.4 RunnableLambda - 自定义处理

可以用 `RunnableLambda` 将任何 Python 函数加入链：

```python
from langchain_core.runnables import RunnableLambda

def word_count(text: str) -> str:
    return f"{text}\n\n字数: {len(text)}"

chain = (
    prompt
    | llm
    | StrOutputParser()
    | RunnableLambda(word_count)  # 自定义后处理
)
```

### 6.5 并行 Chain

同一个输入，同时走多条路径，最后合并：

```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    pros=pros_chain,     # 路径1：分析优点
    cons=cons_chain,     # 路径2：分析缺点
)

# 结果: {"pros": "...", "cons": "..."}
result = parallel.invoke({"language": "Java"})
```

---

## 7. 现代 Runnable API

> 对应文件：`05_runnable_chain.py`

### 7.1 Runnable 接口

LangChain 0.2+ 统一了所有组件的接口，都实现了 `Runnable` 协议：

```python
# 每个 Runnable 都支持这 4 个方法
chain.invoke(input)       # 同步调用（单个输入）
chain.stream(input)       # 流式输出
chain.batch([i1, i2])    # 批量调用
await chain.ainvoke(input) # 异步调用
```

### 7.2 管道操作符 `|`

`|` 是 LangChain 最优雅的设计，让链的构建像搭积木：

```python
# 链式连接
chain = prompt | llm | parser

# 并行组合
parallel = RunnableParallel(a=chain_a, b=chain_b)

# 透传数据
chain = RunnableParallel(
    result=main_chain,
    original=RunnablePassthrough()  # 保留原始输入
)
```

### 7.3 RunnablePassthrough

原样传递输入，常用于并行链中保留原始数据：

```python
chain = RunnableParallel(
    summary=summary_chain,      # 生成摘要
    original=RunnablePassthrough()  # 保留原文
)

result = chain.invoke({"text": "长篇文章..."})
# result["summary"] = "摘要..."
# result["original"] = "长篇文章..."
```

### 7.4 调试技巧

```python
# 查看中间结果
result = chain.invoke(input)
print(result)  # 查看最终输出

# 使用 LangSmith 追踪（推荐）
# 注册: https://smith.langchain.com
# 设置环境变量:
# export LANGCHAIN_TRACING_V2=true
# export LANGCHAIN_API_KEY=your-key
```

---

## 8. 综合实践项目

> 对应文件：`main.py`

### 8.1 功能说明

`main.py` 整合了今天所有知识点，构建了一个交互式智能助手：

| 功能 | 用到的组件 | 链名称 |
|------|-----------|--------|
| 通用问答 | PromptTemplate + LLM + Parser | `qa_chain` |
| 代码解释 | ChatPromptTemplate + LLM + Parser | `code_chain` |
| 文本摘要 | PromptTemplate + LLM + Parser | `summary_chain` |
| 头脑风暴 | PromptTemplate + LLM + Parser | `brainstorm_chain` |
| JSON输出 | ChatPromptTemplate + LLM + **JsonOutputParser** | `json_chain` |

### 8.2 架构设计

```
用户选择功能
    │
    ├── 1. 问答     → qa_chain
    ├── 2. 代码解释 → code_chain
    ├── 3. 文本摘要 → summary_chain
    ├── 4. 头脑风暴 → brainstorm_chain
    └── 5. JSON输出 → json_chain
    │
    ▼
route_task() → 返回结果 → Rich 格式化显示
```

### 8.3 运行示例

```bash
python main.py
```

```
╭───────────────────────────────╮
│   Day 8 LangChain 智能助手    │
├─────┬────────────┬────────────┤
│ 编号│ 功能       │ 说明       │
├─────┼────────────┼────────────┤
│ 1   │ 问答       │ 输入问题   │
│ 2   │ 代码解释   │ 粘贴代码   │
│ 3   │ 文本摘要   │ 输入文本   │
│ 4   │ 头脑风暴   │ 输入主题   │
│ 5   │ JSON输出   │ 结构化创意 │
│ q   │ 退出       │            │
╰─────┴────────────┴────────────╯

请选择功能 (1-5, q): 1
请输入问题: 什么是RAG？
[思考中...]
╭──── 回答 ────╮
│ RAG是检索增强 │
│ 生成的缩写... │
╰──────────────╯
```

---

## 9. 常见问题

### Q1: 报错 `ModuleNotFoundError: No module named 'langchain'`

```bash
pip install langchain langchain-openai
```

### Q2: 报错 `AuthenticationError`

检查 `.env` 文件中的 API Key 是否正确：

```bash
# 确认 key 存在且不为空
cat .env
```

### Q3: `JsonOutputParser` 输出不规范

LLM 有时会在 JSON 前后加文字。解决方法：
- 在 prompt 中强调"只输出 JSON，不要其他内容"
- 使用 `StrOutputParser` 先获取文本，再用 `json.loads()` 手动解析

### Q4: `|` 操作符报错

确保所有组件都实现了 `Runnable` 接口。`ChatPromptTemplate`、`ChatOpenAI`、所有 `OutputParser` 都支持。

### Q5: 如何切换回 OpenAI 官方 API？

修改 `config.py`：

```python
OPENAI_BASE_URL = "https://api.openai.com/v1"
MODEL_NAME = "gpt-4o"
```

---

## 10. 知识总结

### 10.1 今日学习路线

```
LLM调用 → Prompt模板 → 输出解析 → 链式组装
   │          │            │           │
   ▼          ▼            ▼           ▼
ChatOpenAI  Template    Parser     Chain |
```

### 10.2 核心代码模式

```python
# 这是 LangChain 最常见的代码模式，务必记住
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="deepseek-chat")
prompt = ChatPromptTemplate.from_template("回答：{question}")
parser = StrOutputParser()

chain = prompt | llm | parser
result = chain.invoke({"question": "什么是AI？"})
```

### 10.3 与 Day 7 的关系

| 对比项 | Day 7（Function Calling） | Day 8（LangChain） |
|--------|--------------------------|-------------------|
| 调用方式 | `openai.ChatCompletion` | `ChatOpenAI \|` |
| 提示词 | 字符串硬编码 | PromptTemplate 模板化 |
| 输出处理 | 手动 `json.loads` | OutputParser 自动解析 |
| 代码风格 | 命令式 | 声明式（管道流） |
| 适用场景 | 简单工具调用 | 复杂 LLM 应用 |

### 10.4 文件清单

```
day8/
├── config.py              # 配置文件（API Key、模型地址）
├── main.py                # 综合实践：智能问答助手
├── 01_llm_basic.py        # LLM 基础调用示例
├── 02_prompt_template.py  # PromptTemplate 模板示例
├── 03_output_parser.py    # OutputParser 解析器示例
├── 04_simple_chain.py     # Chain 链式调用示例
├── 05_runnable_chain.py   # 现代 Runnable API 示例
├── requirements.txt       # 依赖列表
├── .env                   # API Key（不提交到 git）
├── .gitignore             # Git 忽略文件
└── README.md              # 本文档
```

### 10.5 明天预告

**Day 9 - Memory 记忆**：让 AI 具备对话记忆能力，支持多轮对话上下文管理。

---

> 学习建议：按编号顺序运行每个 `.py` 文件，观察输出结果，尝试修改参数看看效果变化。
