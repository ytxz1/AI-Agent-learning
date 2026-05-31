# 🚀 1个月 AI Agent 实习学习计划

> **目标**：1个月内掌握 AI Agent 核心技能，完成 4 个项目，拿到暑期实习 Offer

---

## 📋 目录

- [核心技能栈](#-核心技能栈)
- [学习路线总览](#-学习路线总览)
- [第1周：基础铺垫（Python + API 入门）](#-第1周基础铺垫python--api-入门)
- [第2周：Agent 基础（LangChain 入门）](#-第2周agent-基础langchain-入门)
- [第3周：进阶应用（RAG 与项目实战）](#-第3周进阶应用rag-与项目实战)
- [第4周：工程化与求职准备](#-第4周工程化与求职准备)
- [项目产出](#-项目产出)
- [学习建议](#-学习建议)
- [推荐资源](#-推荐资源)
- [常见面试题](#-常见面试题)

---

## 🛠 核心技能栈

| 技能                   | 说明                                                      | 用途                               |
| ---------------------- | --------------------------------------------------------- | ---------------------------------- |
| **Python**       | 编程基础，语法、数据结构、面向对象、标准库                | 所有 AI Agent 开发的基础语言       |
| **OpenAI API**   | Chat Completions、Function Calling、Streaming、Embeddings | 与大模型交互的核心接口             |
| **LangChain**    | LLM 编排框架：Chain、Memory、Tool、Agent、RAG             | 快速构建 Agent 应用的核心框架      |
| **RAG**          | 检索增强生成：Embedding、向量数据库、文档检索             | 让 Agent 掌握私有知识/最新信息     |
| **FastAPI**      | 高性能 Web 框架：路由、异步、自动文档                     | 将 Agent 项目接口化，对外提供服务  |
| **Playwright**   | 浏览器自动化工具                                          | 构建 Coding Agent 时用于自动化操作 |
| **Git & Docker** | 版本控制\& 容器化部署                                     | 项目管理和上线部署                 |

---

## 📅 学习路线总览

`第1周 ── Python 基础 → API 调用 → Function Calling → 聊天机器人 ✅ 第2周 ── LangChain → Memory → Tool → Agent → 工具调用 Agent ✅ 第3周 ── RAG → 向量数据库 → 文档处理 → RAG问答系统 + Coding Agent ✅ 第4周 ── FastAPI → Docker部署 → 简历优化 → 投递面试 🎯`

# 🚀 1个月 AI Agent 实习学习计划

> **目标**：1个月内掌握 AI Agent 核心技能，完成 4 个项目，拿到暑期实习 Offer

---

## 📋 目录

- [核心技能栈](#-核心技能栈)
- [学习路线总览](#-学习路线总览)
- [第1周：基础铺垫（Python + API 入门）](#-第1周基础铺垫python--api-入门)
- [第2周：Agent 基础（LangChain 入门）](#-第2周agent-基础langchain-入门)
- [第3周：进阶应用（RAG 与项目实战）](#-第3周进阶应用rag-与项目实战)
- [第4周：工程化与求职准备](#-第4周工程化与求职准备)
- [项目产出](#-项目产出)
- [学习建议](#-学习建议)
- [推荐资源](#-推荐资源)
- [常见面试题](#-常见面试题)

---

## 🛠 核心技能栈

| 技能                   | 说明                                                      | 用途                               |
| ---------------------- | --------------------------------------------------------- | ---------------------------------- |
| **Python**       | 编程基础，语法、数据结构、面向对象、标准库                | 所有 AI Agent 开发的基础语言       |
| **OpenAI API**   | Chat Completions、Function Calling、Streaming、Embeddings | 与大模型交互的核心接口             |
| **LangChain**    | LLM 编排框架：Chain、Memory、Tool、Agent、RAG             | 快速构建 Agent 应用的核心框架      |
| **RAG**          | 检索增强生成：Embedding、向量数据库、文档检索             | 让 Agent 掌握私有知识/最新信息     |
| **FastAPI**      | 高性能 Web 框架：路由、异步、自动文档                     | 将 Agent 项目接口化，对外提供服务  |
| **Playwright**   | 浏览器自动化工具                                          | 构建 Coding Agent 时用于自动化操作 |
| **Git & Docker** | 版本控制 & 容器化部署                                     | 项目管理和上线部署                 |

---

## 📅 学习路线总览

```
第1周 ── Python 基础 → API 调用 → Function Calling → 聊天机器人 ✅
第2周 ── LangChain → Memory → Tool → Agent → 工具调用 Agent ✅
第3周 ── RAG → 向量数据库 → 文档处理 → RAG问答系统 + Coding Agent ✅
第4周 ── FastAPI → Docker部署 → 简历优化 → 投递面试 🎯
```

---

## 📖 第1周：基础铺垫（Python + API 入门）

> **学习目标**：熟练 Python 基础，掌握 API 调用，能与大模型对话
> **最终产出**：一个支持对话记忆和流式输出的聊天机器人

---

### Day 1：Python 基础

#### 学习内容

**1. 变量与数据类型**

Python 是动态类型语言，变量不需要声明类型。

```python
# 基本数据类型
name = "Alice"           # str（字符串）
age = 25                 # int（整数）
height = 1.75            # float（浮点数）
is_student = True        # bool（布尔值）

# 类型可以动态变化
x = 10       # 此时 x 是 int
x = "hello"  # 此时 x 变成了 str
```

**2. 条件与循环**

```python
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"

for i in range(5):
    print(i)

count = 0
while count < 5:
    print(count)
    count += 1

squares = [x**2 for x in range(10)]
```

**3. 函数**

```python
def greet(name, greeting="Hello"):
    """生成问候语"""
    return f"{greeting}, {name}!"

print(greet("Alice"))     # Hello, Alice!
print(greet("Bob", "Hi")) # Hi, Bob!
```

**4. 文件操作**

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\\n")

with open("notes.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

#### 为什么这很重要

Python 是 AI Agent 开发的首选语言。几乎所有 AI 框架（LangChain、LlamaIndex）、
AI SDK（OpenAI Python SDK）以及 Web 框架（FastAPI）都是基于 Python 的。

---

### Day 2：Python 进阶

#### 学习内容

**1. 列表、字典、集合**

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")
fruits[0]  # "apple"
fruits[1:3]  # ["banana", "cherry"]

student = {"name": "Alice", "age": 20}
student["grade"] = "A"
student.get("name")  # 安全获取

unique_nums = {1, 2, 3, 3, 2, 1}  # {1, 2, 3}
set_a = {1, 2, 3}
set_b = {3, 4, 5}
set_a & set_b  # 交集 {3}
```

**2. 类和对象**

```python
class ChatBot:
    def __init__(self, name: str):
        self.name = name
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

bot = ChatBot("助手")
bot.add_message("user", "你好")
```

**3. 异常处理**

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"除零错误：{e}")
except Exception as e:
    print(f"未知错误：{e}")
finally:
    print("总会执行")
```

**4. 常用标准库**

```python
import requests
import json
import os
from typing import List, Dict, Optional

response = requests.get("https://api.example.com/data")
data = response.json()

current_dir = os.getcwd()
api_key = os.environ.get("OPENAI_API_KEY")
```

#### 为什么要学这些

- 列表/字典/集合：AI Agent 中大量用于管理消息历史、配置参数、工具定义
- 类与对象：LangChain 等框架大量使用面向对象设计
- 异常处理：API 调用经常失败，必须优雅处理
- 常用库：requests 用于 API 通信，json 用于数据交换，os 用于环境变量

---

### Day 3：API 调用入门

#### 学习内容

**1. 什么是 API**

API（应用程序编程接口）是不同软件组件之间的通信协议。在 AI Agent 中，
我们主要调用 OpenAI 等大模型的 HTTP API。

API 调用流程：

```
你的代码 → 构造 HTTP 请求 → 发送到 API 端点 → 服务器处理 → 返回响应
```

**2. 注册与密钥获取**

1. 访问 OpenAI Platform (https://platform.openai.com)
2. 注册账号并创建 API Key
3. 将密钥保存在环境变量中（不要硬编码在代码里！）

```bash
$env:OPENAI_API_KEY = "sk-your-key-here"  # Windows PowerShell
```

**3. Chat Completions API 基础**

```python
from openai import OpenAI
import os

client = OpenAI()  # 自动读取环境变量

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "请用中文介绍 AI Agent 是什么？"}
    ]
)

reply = response.choices[0].message.content
print(reply)
```

**4. 解析 API 响应**

```python
print(response.id)              # 请求 ID
print(response.model)           # 使用的模型
print(response.usage.total_tokens)  # 总 token 数
```

#### 实践：多轮对话

```python
def chat_with_history():
    client = OpenAI()
    messages = [
        {"role": "system", "content": "你是一个友好的助手。"}
    ]

    while True:
        user_input = input("你：")
        if user_input.lower() == "quit": break

        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages
        )
        assistant_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_reply})
        print(f"助手：{assistant_reply}")
```

---

### Day 4：流式输出与参数控制

#### 核心参数详解

| 参数        | 作用              | 推荐值                   | 说明                    |
| ----------- | ----------------- | ------------------------ | ----------------------- |
| temperature | 输出随机性（0-2） | 0.7（创意）/ 0.1（精确） | 越低越确定              |
| max_tokens  | 限制输出长度      | 视任务而定               | 到达上限自动截断        |
| top_p       | 核采样（0-1）     | 0.9                      | 与 temperature 配合使用 |
| stream      | 流式输出          | True/False               | True 实时展示生成过程   |

#### 流式输出实现

```python
def stream_chat():
    client = OpenAI()
    messages = [
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "请写一段介绍 AI Agent 的文字。"}
    ]

    stream = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages,
        stream=True, temperature=0.7, max_tokens=500
    )

    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content
    return full_response
```

#### 流式输出的优势

- 用户体验更好：无需等待全部内容生成
- 延迟感知更低：首 token 到达后立即显示
- 适合长时间生成任务

---

### Day 5：Prompt Engineering（提示词工程）

#### 1. 提示词基本原则

- **清晰具体**：告诉模型你想要的精确格式和内容
- **提供上下文**：让模型了解背景信息
- **分步指导**：复杂任务需要拆解步骤
- **指定角色**：通过 System Prompt 设定角色

#### 2. Zero-shot Prompt（零样本提示）

直接给出任务描述，不提供示例。

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "你是一个情感分析专家。"},
        {"role": "user", "content": "这个产品太棒了！"}
    ]
)
```

#### 3. Few-shot Prompt（少样本提示）

提供几个示例来引导模型理解任务模式。

```python
messages = [
    {"role": "system", "content": "请将问题分类：技术、生活、学习"},
    {"role": "user", "content": "怎么用 Python 读取 CSV？"},
    {"role": "assistant", "content": "技术"},
    {"role": "user", "content": "今天天气怎么样？"},
    {"role": "assistant", "content": "生活"},
    {"role": "user", "content": "高三怎么规划复习？"},
    # 模型应该推理出输出 "学习"
]
```

#### 4. Chain of Thought（思维链）

引导模型逐步推理，输出中间步骤。

```python
messages = [
    {"role": "system", "content": "请一步步推理，最后给出答案。\\n步骤1：...\\n步骤2：...\\n答案：..."},
    {"role": "user", "content": "商店有15个苹果，卖了7个，又进了10个，现在有多少？"}
]
# 模型会输出：\\n步骤1：初始15个\\n步骤2：15-7=8\\n步骤3：8+10=18\\n答案：18
```

#### 5. System Prompt 最佳实践

一个好的 System Prompt 应该明确：角色、行为准则、输出格式、知识边界。
它决定了模型的整体行为风格，是 Prompt Engineering 中最重要的一环。

---

### Day 6：Function Calling 基础

#### 什么是 Function Calling

Function Calling 是让大模型能够调用你定义的函数的能力。
模型不会真的执行函数，而是输出结构化调用请求，你在代码中解析并执行。

核心流程：

```
用户问题 → 模型识别意图 → 返回函数调用 → 执行函数 → 结果返回模型 → 模型给出最终回复
```

#### 定义工具

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["city"]
        }
    }
}]
```

#### 完整调用流程

```python
import json
from openai import OpenAI
client = OpenAI()

def get_weather(city, unit="celsius"):
    data = {"北京": "晴 22C", "上海": "多云 26C"}
    return json.dumps(data.get(city, {"temp": 20}))

available_functions = {"get_weather": get_weather}

def function_calling_chat(user_message):
    messages = [{"role": "user", "content": user_message}]
    response = client.chat.completions.create(
        model="gpt-4o", messages=messages, tools=tools, tool_choice="auto"
    )
    msg = response.choices[0].message

    if msg.tool_calls:
        for tc in msg.tool_calls:
            fn = tc.function.name
            args = json.loads(tc.function.arguments)
            result = available_functions[fn](**args)
            messages.append(msg)
            messages.append({
                "tool_call_id": tc.id, "role": "tool",
                "name": fn, "content": result
            })
        second = client.chat.completions.create(model="gpt-4o", messages=messages)
        return second.choices[0].message.content
    return msg.content
```

#### 高级用法

```python
# 强制调用某个函数
tool_choice = {"type": "function", "function": {"name": "get_weather"}}

# 并行函数调用（一次返回多个函数调用）
# 模型可能会返回多个 tool_calls，处理方式类似
```

---

### Day 7：项目0——聊天机器人

#### 项目说明

将前6天内容整合成一个完整的聊天机器人项目。这是你第一个可展示的作品。

#### 功能需求

1. **对话记忆**：记住上下文进行多轮对话
2. **流式输出**：实时展示回复产生过程
3. **Function Calling**：支持调用外部工具
4. **友好界面**：命令行交互界面

#### 项目结构

```
chatbot/
├── main.py              # 主程序入口
├── chatbot.py           # 聊天机器人核心逻辑
├── tools.py             # 工具函数定义
├── config.py            # 配置文件
├── requirements.txt     # 依赖清单
└── README.md            # 项目说明
```

#### 核心代码

```python
# config.py
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0.7
MAX_TOKENS = 1000
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# tools.py
def get_current_time():
    from datetime import datetime
    return json.dumps({"time": datetime.now().strftime("%H:%M")})

def calculate(expression):
    try: return json.dumps({"result": eval(expression)})
    except: return json.dumps({"error": str(e)})
```

#### 项目总结

这是你第一个完整的 AI Agent 项目，涵盖了：

- OpenAI API 调用
- 流式输出
- Function Calling
- 对话记忆管理
  虽然简单，但已具备实际 AI Agent 应用的骨架。

---

## 📖 第2周：Agent 基础（LangChain 入门）

> **学习目标**：掌握 LangChain 框架，构建能调用工具的 Agent
> **最终产出**：一个支持天气查询、计算器、翻译等功能的工具调用 Agent

---

### Day 8：LangChain 入门

#### 什么是 LangChain

LangChain 是一个用于构建基于大语言模型（LLM）应用的开发框架。
它提供抽象和工具来快速构建：Chain（串联组件）、Memory（记忆管理）、
Tool（工具定义）、Agent（智能代理）、RAG（检索增强生成）。

安装：``bash pip install langchain langchain-openai langchain-community``

#### 核心概念

**1. LLM 封装**

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
result = llm.invoke("你好")
print(result.content)
```

**2. Prompt 模板**

```python
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}专家。"),
    ("human", "{question}")
])
formatted = prompt.format_messages(role="Python", question="什么是装饰器？")
```

**3. Output Parser**

```python
from langchain_core.output_parsers import CommaSeparatedListOutputParser
parser = CommaSeparatedListOutputParser()
chain = prompt | llm | parser
```

**4. 简单 Chain（管道操作符 |）**

```python
chain = ChatPromptTemplate.from_messages([
    ("system", "将{src}翻译成{tgt}"),
    ("human", "{text}")
]) | ChatOpenAI() | StrOutputParser()

result = chain.invoke({"src": "英文", "tgt": "中文", "text": "Hello"})
```

数据流：输入 → PromptTemplate → ChatOpenAI → StrOutputParser → 输出

---

### Day 9：Memory 记忆

#### 为什么需要 Memory

大模型本身无状态，每次调用都是独立的。Memory 让 Agent 记住对话历史。

**ConversationBufferMemory**：记录完整对话历史

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()
conversation = ConversationChain(llm=ChatOpenAI(), memory=memory)
conversation.predict(input="我叫小明")
conversation.predict(input="我叫什么？")  # 还记得叫小明
```

**BufferWindowMemory**：只保留最近K轮对话，防止上下文过长

```python
from langchain.memory import ConversationBufferWindowMemory
window_memory = ConversationBufferWindowMemory(k=2)
```

**SummaryMemory**：对历史对话进行摘要，保留关键信息

```python
from langchain.memory import ConversationSummaryMemory
summary_memory = ConversationSummaryMemory(llm=ChatOpenAI())
```

#### 为什么记忆很重要

- **上下文理解**：基于之前对话做出正确回应
- **多轮交互**：用户可连续提问而不用重复上下文
- **任务跟踪**：Agent 记住进行中的任务状态
- **个性化**：记住用户偏好，提供个性化服务

---

### Day 10：Tools 工具

#### 什么是 Tool

Tool 是 Agent 可以调用的外部能力。每个 Tool 包含：name（模型索引）、
description（模型判断何时使用）、args_schema（参数模式）、func（实际函数）。

#### 自定义工具

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气。输入城市名，返回天气。"""
    data = {"北京": "晴 22C", "上海": "多云 26C"}
    return data.get(city, "无数据")

@tool
def calculate(expression: str) -> str:
    """计算数学表达式。输入如 2+3*4。"""
    return str(eval(expression))
```

#### 工具描述的重要性

工具描述是 Agent 选择工具的关键。好的描述应说明：

1. 工具的用途（什么时候该用）
2. 输入格式（输入应该什么样）
3. 输出内容（返回什么信息）

工具调用原理：

```
用户提问 → Agent 查看所有工具的 name/description → 决定是否使用工具
→ 输出工具名称和参数 → LangChain 调用实际函数 → 结果返回给 Agent → 生成回答
```

---

### Day 11：Agents 代理

#### 什么是 Agent

Agent 是 LangChain 最核心的概念。它利用 LLM 的推理能力，自主决定：

1. 当前应该做什么
2. 是否需要调用工具
3. 调用哪个工具
4. 工具返回后如何继续

**Agent vs Chain**：Chain 是固定序列 A→B→C，Agent 是动态决策流程。

#### ReAct Agent（Reasoning + Acting）

工作循环：思考(Thought) → 行动(Action) → 观察(Observation) → 循环...

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain_openai import ChatOpenAI

@tool
def get_weather(city):
    """获取天气"""
    return f"{city}：晴 22C"

tools = [get_weather]
llm = ChatOpenAI(model="gpt-4o", temperature=0)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke({"input": "北京天气怎么样？"})
```

#### 实际运行过程（verbose=True 可以看到完整推理链）

```
Thought: 用户问了北京天气，我需要查天气工具。
Action: get_weather
Action Input: 北京
Observation: 北京：晴 22C
Thought: 我现在可以回答用户了。
Final Answer: 北京今天天气晴朗，气温22C。
```

#### Agent Executor 参数

```python
AgentExecutor(
    agent=agent, tools=tools, verbose=True,
    max_iterations=15,        # 防止无限循环
    max_execution_time=30,    # 最大执行时间（秒）
    handle_parsing_errors=True,  # 处理LLM输出解析错误
    return_intermediate_steps=True,  # 返回中间步骤
)
```

#### Agent 类型对比

| 类型             | 适用场景       | 特点                      |
| ---------------- | -------------- | ------------------------- |
| ReAct            | 大多数场景     | 推理+行动循环，通用性强   |
| OpenAI Functions | 配合OpenAI模型 | 原生支持 Function Calling |
| Structured Chat  | 结构化输出     | 适合格式化输出场景        |
| Plan & Execute   | 复杂任务       | 先规划再执行              |

---

### Day 12：输出解析

#### 为什么需要输出解析

LLM 的输出是自然语言，而大多数应用需要结构化数据。OutputParser 将文本转换为 Python 对象。

#### 常用输出解析器

**StrOutputParser**：直接返回字符串

```python
from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()
chain = prompt | llm | parser
```

**CommaSeparatedListOutputParser**：逗号分隔文本转列表

```python
parser = CommaSeparatedListOutputParser()
chain = prompt | llm | parser  # 返回 ["Django", "Flask", ...]
```

**JsonOutputParser**：JSON 输出

```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

class Analysis(BaseModel):
    sentiment: str = Field(description="情感极性")
    confidence: float = Field(description="置信度")

parser = JsonOutputParser(pydantic_object=Analysis)
chain = prompt | llm | parser
```

#### 最佳实践

1. 总是使用 format_instructions 让 LLM 知道输出格式
2. 提供示例输出进行 few-shot 示范
3. 启用错误处理（LLM 有时会输出不符合格式的内容）
4. Pydantic 校验自动验证数据类型

---

### Day 13：LangChain 综合实战

整合 Memory、Tools、Agent 构建完整智能助手。

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

@tool
def get_weather(city: str) -> str:
    """获取天气"""
    return f"{city}：晴 22C"

@tool
def calculate(expr: str) -> str:
    """计算表达式"""
    return str(eval(expr))

tools = [get_weather, calculate]
llm = ChatOpenAI(model="gpt-4o", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能助手，可以使用工具帮助用户。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_openai_functions_agent(llm, tools, prompt)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_executor = AgentExecutor(
    agent=agent, tools=tools, memory=memory, verbose=True
)
```

#### 性能优化技巧

- 减少 verbose：生产环境关闭 verbose
- 缓存 LLM 调用：相同输入不重复调用
- 控制迭代次数：设置合理的 max_iterations
- 异步执行：使用 ainvoke() 替代 invoke()

---

### Day 14：项目1——工具调用 Agent

#### 功能需求

1. **天气查询**：查询任意城市实时天气
2. **计算器**：执行数学计算
3. **翻译功能**：多语言翻译
4. **时间查询**：获取当前时间

#### 项目结构

```
agent_project/
├── main.py           # 主程序
├── agent.py          # Agent 核心
├── tools/
│   ├── weather.py    # 天气工具
│   ├── calculator.py # 计算器
│   └── translator.py # 翻译工具
├── config.py         # 配置
└── requirements.txt  # 依赖
```

#### 项目亮点

- **多工具协作**：Agent 能根据问题自动选择工具
- **多轮推理**：能进行复杂的多步推理
- **错误处理**：优雅处理工具调用失败
- **记忆功能**：记住对话上下文

```txt
# requirements.txt
langchain>=0.1.0
langchain-openai>=0.1.0
langchain-community>=0.1.0
openai>=1.0.0
```

---

## 📖 第3周：进阶应用（RAG 与项目实战）

> **学习目标**：掌握 RAG 技术，完成 RAG 问答系统和 Coding Agent
> **最终产出**：本地知识库问答系统 + 自动刷题 Agent

---

### Day 15：RAG 基础

#### 什么是 RAG

RAG = Retrieval-Augmented Generation（检索增强生成）。

**为什么需要 RAG？** 大模型的局限性：

- 知识截止日期：GPT-4 知识只到 2023 年
- 无法访问私有数据：模型没有训练你的公司数据
- 幻觉问题：模型可能编造信息
- 无法引用来源：不知道回答依据

**RAG 的解决方案**：用户提问 → 检索相关文档 → 文档作为上下文 → LLM 基于上下文回答

#### RAG 完整流程

```
原始文档 → 文档切分(Chunking) → Embedding向量化 → 向量数据库存储
                                                          ↑
用户问题 → Embedding向量化 → 向量检索(相似度搜索) → LLM生成回答
```

#### Embedding 概念

Embedding 是将文本转换为向量（数字数组）的技术。语义相近的文本，向量也相近。

```python
from openai import OpenAI
client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=["什么是 AI Agent？"]
)
vector = response.data[0].embedding  # 1536维向量
```

---

### Day 16：向量数据库

**FAISS**（Meta开发的向量检索库，适合中小规模）：

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
documents = [Document(page_content="AI Agent 是自主执行任务的智能程序。")]
vectorstore = FAISS.from_documents(documents, embeddings)
results = vectorstore.similarity_search("什么是 AI Agent？", k=3)
vectorstore.save_local("faiss_index")
```

**Chroma**（轻量级开源向量数据库）：

```python
from langchain_chroma import Chroma

vectorstore = Chroma(
    collection_name="my_knowledge",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./chroma_db"
)
vectorstore.add_documents(documents)
results = vectorstore.similarity_search_with_score("AI Agent", k=5)
```

#### 高级检索

MMR（最大边际相关性）- 提高结果多样性：

```python
results = vectorstore.max_marginal_relevance_search("AI Agent", k=5, fetch_k=20)
```

带过滤的检索：

```python
results = vectorstore.similarity_search("Python", filter={"source": "doc.md"})
```

---

### Day 17：文档加载与切分

#### 文档加载

```python
from langchain_community.document_loaders import (
    TextLoader, PyPDFLoader, DirectoryLoader
)

text_loader = TextLoader("notes.txt", encoding="utf-8")
pdf_loader = PyPDFLoader("manual.pdf")
dir_loader = DirectoryLoader("data/", glob="**/*.txt", loader_cls=TextLoader)
```

#### 文本切分策略

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,         # 每块最大字符数
    chunk_overlap=50,       # 块之间的重叠字符数（非常重要！）
    separators=["\\n\\n", "\\n", "。", "！", "？", " ", ""],
)
chunks = text_splitter.split_documents(documents)
```

**为什么 chunk_overlap 重要？** 如果没有重叠，一个段落可能被切成两块，
导致语义断裂。重叠部分确保关键信息不会丢失。

#### 切分最佳实践

```
chunk_size 选择：
- 500-1000字符：一般问答场景，检索精度高
- 1000-2000字符：需要较长上下文的场景
- 2000+字符：需要全文理解的任务

chunk_overlap：chunk_size 的 10-20% 通常足够
```

---

### Day 18：RAG 检索链

#### 构建完整 RAG 问答链

```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. 加载文档
loader = TextLoader("knowledge.txt", encoding="utf-8")
docs = loader.load()

# 2. 切分
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 3. 向量数据库
vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 4. 提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "只使用提供的上下文回答问题。\\n上下文：{context}"),
    ("human", "{input}")
])

# 5. 创建链
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
doc_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, doc_chain)

# 6. 问答
response = rag_chain.invoke({"input": "什么是 RAG 技术？"})
print(response["answer"])
```

#### 优化检索效果

**MMR 检索（提高多样性）**：

```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 20, "lambda_mult": 0.5}
)
```

**Contextual Compression（压缩检索）**：

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)
```

---

### Day 19：项目2——RAG 问答系统

#### 功能需求

1. **文档上传**：支持 PDF/TXT 格式
2. **智能切分**：自动将文档切分成合适大小
3. **向量存储**：使用 Chroma 持久化存储
4. **智能问答**：基于检索结果生成回答
5. **来源引用**：在回答中标注信息来源

#### 项目结构

```
rag_qa_system/
├── main.py                 # 主程序
├── document_processor.py   # 文档处理
├── vector_store.py         # 向量数据库管理
├── qa_chain.py             # 问答链
├── web_ui.py               # Web 界面(Streamlit)
├── config.py               # 配置
└── requirements.txt        # 依赖
```

#### 核心代码 (qa_chain.py)

```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

def create_qa_chain(vectorstore):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "只基于提供的上下文回答问题。\\n引用来源格式：[来源，第X页]\\n\\n上下文：{context}"),
        ("human", "{input}")
    ])
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    doc_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(
        vectorstore.as_retriever(search_kwargs={"k": 4}), doc_chain
    )
    return retrieval_chain
```

#### Streamlit Web 界面

```python
import streamlit as st
st.set_page_config(page_title="RAG 知识库问答系统", page_icon="📚")
st.title("📚 RAG 知识库问答系统")

uploaded_file = st.file_uploader("上传文档（PDF/TXT）", type=["pdf", "txt"])
if uploaded_file:
    # 处理文档、构建向量库、创建问答链
    pass

question = st.text_input("请输入您的问题：")
if question:
    result = ask_question(qa_chain, question)
    st.write(result["answer"])
    with st.expander("引用来源"):
        for src in result["sources"]:
            st.text(src["excerpt"])
```

---

### Day 20：项目3——Coding Agent

#### 功能需求

1. **题目理解**：解析编程题目描述
2. **代码生成**：自动生成解题代码
3. **测试运行**：使用测试用例验证代码
4. **错误修复**：根据测试反馈修复 bug
5. **多轮迭代**：直到所有测试通过

#### 核心实现 (coding_agent.py)

```python
from openai import OpenAI
import re

class CodingAgent:
    def __init__(self):
        self.client = OpenAI()

    def extract_code(self, response):
        pattern = r"```(?:python)?\\n(.*?)```"
        match = re.search(pattern, response, re.DOTALL)
        return match.group(1).strip() if match else response.strip()

    def solve_problem(self, problem, max_iterations=5):
        # 初始生成代码
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": problem["prompt"]}]
        )
        code = self.extract_code(response.choices[0].message.content)

        # 迭代优化循环
        for i in range(max_iterations):
            test_result = self.run_tests(code, problem["tests"])
            if test_result["passed"]:
                return {"code": code, "iterations": i+1}

            # 将测试结果发给模型修复
            msg = f"代码运行结果：\\n{test_result}\\n请修复错误。"
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": msg}]
            )
            code = self.extract_code(response.choices[0].message.content)

        return {"code": code, "error": "达到最大迭代次数"}
```

---

### Day 21：项目优化与调试

#### 优化提示词

```python
def create_optimized_prompt(role, rules, output_format):
    return f"""你是一个{role}。请遵循以下准则：

## 行为规则
{"\\n".join(f"- {r}" for r in rules)}

## 输出要求
{output_format}
"""
```

#### 性能优化清单

**1. 缓存相同问题结果**

```python
from functools import lru_cache
@lru_cache(maxsize=100)
def cached_ask(question):
    return agent_executor.invoke({"input": question})
```

**2. 优化向量检索**

```python
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3, "filter": {"category": "technical"}}
)
```

**3. 异步并行处理**

```python
import asyncio
async def batch_process(questions):
    tasks = [agent_executor.ainvoke({"input": q}) for q in questions]
    return await asyncio.gather(*tasks)
```

#### 调试技巧

1. 设置 verbose=True 查看 Agent 内部推理过程
2. 保存中间步骤：response.get("intermediate_steps", [])
3. 使用 LangSmith 可视化追踪
4. 手动测试每个工具是否正常工作

---

## 📖 第4周：工程化与求职准备

> **学习目标**：掌握 FastAPI，项目部署上线，准备面试与投递
> **最终产出**：项目上线 + 高质量简历 + 面试准备

---

### Day 22：FastAPI 入门

#### 什么是 FastAPI

高性能 Python Web 框架，专为构建 API 设计：

- 高性能（与 Node.js/Go 相当）
- 自动生成 OpenAPI 文档
- 基于类型提示的请求验证
- 原生异步支持

安装：``bash pip install fastapi uvicorn``

#### 基础示例

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Agent API", version="1.0.0")

class ChatRequest(BaseModel):
    message: str
    temperature: float = 0.7

class ChatResponse(BaseModel):
    reply: str
    tokens_used: int

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = await process_chat(request.message)
    return ChatResponse(reply=result["reply"], tokens_used=result["tokens"])
```

访问 http://localhost:8000/docs 查看自动生成的 API 文档。

---

### Day 23：集成项目 API

#### 将 Agent 封装成 API

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json

app = FastAPI(title="AI Agent Service")

class AgentRequest(BaseModel):
    question: str
    session_id: str = None
    temperature: float = 0.7
    stream: bool = False

@app.post("/agent/chat")
async def agent_chat(request: AgentRequest):
    try:
        result = agent_executor.invoke(request.question)
        return {"answer": result["output"], "session_id": request.session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/chat/stream")
async def agent_chat_stream(request: AgentRequest):
    async def generate():
        async for chunk in agent_executor.astream(request.question):
            yield f"data: {json.dumps({"chunk": chunk})}\\n\\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

#### 跨域配置（CORS）

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
```

#### 启动脚本

```python
import uvicorn
uvicorn.run("agent_api:app", host="0.0.0.0", port=8000, reload=True)
```

---

### Day 24：部署上线

#### Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "agent_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml

```yaml
version: "3.8"
services:
  agent-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: unless-stopped
```

#### 构建与运行

```bash
docker build -t ai-agent-api .
docker run -d -p 8000:8000 -e OPENAI_API_KEY=sk-xxx ai-agent-api
docker-compose up -d
```

#### 推荐部署平台

- **Railway**：简单快速，免费额度
- **Render**：支持自动部署
- **阿里云/腾讯云**：国内用户推荐
- **AWS/GCP**：国外主流

---

### Day 25：前端界面（可选）

#### 使用 Streamlit 构建界面

```python
import streamlit as st
import requests

st.set_page_config(page_title="AI Agent 助手", page_icon="🤖")
st.title("🤖 AI Agent 智能助手")

# 侧边栏设置
api_url = st.sidebar.text_input("API 地址", "http://localhost:8000")
temperature = st.sidebar.slider("创造力", 0.0, 2.0, 0.7)

# 对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 输入
if prompt := st.chat_input("请输入问题..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = requests.post(f"{api_url}/agent/chat", json={"question": prompt})
        if response.status_code == 200:
            result = response.json()
            st.markdown(result["answer"])
            st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
```

运行：``bash streamlit run app.py``

---

### Day 26：GitHub 优化

#### 项目结构规范

```
ai-agent-project/
├── .github/workflows/ci.yml     # CI 配置
├── src/
│   ├── agent/                    # Agent 核心
│   ├── api/                      # API 服务
│   └── rag/                      # RAG 模块
├── tests/                        # 测试
├── examples/                     # 使用示例
├── docs/                         # 文档
├── config.py                     # 配置
├── requirements.txt              # 依赖
├── Dockerfile / docker-compose.yml
├── README.md                     # 项目说明
└── LICENSE                       # 开源许可证
```

#### README 最佳实践

- 项目名称和 Logo
- 功能特性列表（带 ✅/❌）
- 快速开始（前置要求 → 安装 → 运行）
- 项目截图/GIF（最重要！）
- 技术栈和项目结构
- 项目亮点（3-5个）
- License 信息

---

### Day 27：简历优化与面试准备

#### 项目经历撰写模板

```
**项目名称**：AI Agent 智能助手
**技术栈**：Python · LangChain · OpenAI API · FastAPI · ChromaDB

**项目描述**：
基于 LangChain 框架开发的 AI Agent 系统，支持多工具调用、
RAG 知识库问答，并提供 RESTful API 接口。

**核心职责**：
1. 设计并实现了基于 ReAct 模式的 Agent 推理引擎
2. 集成 Function Calling 能力，支持天气查询、计算器等工具
3. 构建基于 Chroma 向量数据库的 RAG 问答系统
4. 使用 FastAPI 封装 RESTful API，支持流式输出
5. 通过 Docker 实现容器化部署

**项目成果**：
- 工具调用准确率达到 95%+
- RAG 问答准确率提升 40%
- 端到端响应时间 < 3 秒
```

---

### Day 28-30：投递与冲刺

#### 投递渠道

| 平台      | 特点       | 建议      |
| --------- | ---------- | --------- |
| 实习僧    | 实习生专享 | 优先投递  |
| Boss 直聘 | 回复率较高 | 保持在线  |
| 牛客网    | 技术实习多 | 刷题+投递 |
| 拉勾网    | 互联网公司 | 定期刷新  |
| 内推      | 效果最好   | 找人推荐  |

#### 投递时间建议

- 上午 9:00-11:00（最佳）
- 下午 2:00-4:00
- 避开周五下午和周末

#### 面试准备清单

**技术面试**：

- [ ] Python 基础（数据结构、面向对象、装饰器、生成器）
- [ ] OpenAI API（Chat、Function Calling、Streaming）
- [ ] LangChain（Chain、Memory、Tool、Agent）
- [ ] RAG 原理与实现（Embedding、向量库、检索）
- [ ] FastAPI（路由、依赖注入、Pydantic）
- [ ] Git 基本操作
- [ ] Docker 基本操作

**项目面试**：

- [ ] 项目1：聊天机器人 - 核心功能和技术亮点
- [ ] 项目2：工具调用 Agent - 架构设计和技术细节
- [ ] 项目3：RAG 问答系统 - 优化策略和效果
- [ ] 项目4：Coding Agent - 多轮迭代机制

**行为面试**：

- [ ] 自我介绍（1-2分钟）
- [ ] 为什么选择 AI Agent 方向
- [ ] 遇到过什么技术困难，如何解决的
- [ ] 职业规划
- [ ] 为什么选择我们公司

---

## 💡 常见面试题

### 1. 什么是 AI Agent？和 RAG 有什么区别？

AI Agent 是能自主感知环境、做出决策并采取行动的智能程序。RAG 是检索增强生成技术，
侧重于知识检索。Agent 强调自主决策和工具调用，RAG 强调信息获取和上下文增强。
一个完整的 AI Agent 系统内部通常会使用 RAG 作为知识获取组件。

### 2. 什么是 Function Calling？如何实现？

Function Calling 是让大模型输出结构化函数调用请求的能力。实现步骤：

1. 定义函数及其参数描述
2. 将函数描述作为 tool 传给 API
3. 解析模型返回的 tool_calls
4. 执行对应的 Python 函数
5. 将函数结果返回给模型生成最终回复

### 3. LangChain 中 Agent 的工作流程？

用户输入 → LLM 推理（思考要做什么）→ 输出 Action（工具+参数）
→ LangChain 调用 Tool → Tool 返回 Observation → LLM 继续推理
→ 循环直到 LLM 认为可以给出最终答案

### 4. RAG 系统中如何优化检索效果？

- 分块策略：合适的 chunk_size 和 chunk_overlap
- 检索方式：MMR 提高多样性，带阈值过滤低质量结果
- 查询优化：HyDE、查询重写
- 混合检索：结合关键词检索和向量检索
- 重排序：用 Cross-encoder 对检索结果重排

### 5. 如何解决 LLM 的幻觉问题？

- RAG 约束：强制模型只能基于检索结果作答
- 提示词约束：明确要求"不知道就说不知道"
- 输出校验：对输出结果进行事实核查
- 引用来源：要求模型标注回答来源
- 温度控制：知识性任务使用低 temperature

### 6. FastAPI 和 Flask 的区别？

- 性能：FastAPI 基于 Starlette，性能远超 Flask
- 类型检查：FastAPI 基于 Pydantic 自动校验，Flask 需手动
- 文档：FastAPI 自动生成 OpenAPI 文档
- 异步：FastAPI 原生支持异步，Flask 需扩展
- 生产化：FastAPI 内置数据校验、序列化、文档

---

## 🎯 项目产出

### 项目0：聊天机器人

- **技术栈**：OpenAI API + Python
- **核心功能**：对话记忆、流式输出、Function Calling
- **学习重点**：API 调用、提示词工程、函数调用

### 项目1：工具调用 Agent

- **技术栈**：LangChain + OpenAI API + Python
- **核心功能**：天气查询、计算器、翻译、多轮推理
- **学习重点**：Agent 模式、工具定义、记忆管理

### 项目2：RAG 问答系统

- **技术栈**：LangChain + ChromaDB + OpenAI + Streamlit
- **核心功能**：文档上传、智能问答、来源引用
- **学习重点**：文档处理、向量检索、RAG 链

### 项目3：Coding Agent

- **技术栈**：OpenAI API + Python
- **核心功能**：题目理解、代码生成、测试运行、错误修复
- **学习重点**：多轮迭代、自动评测、代码执行

---

## 💡 学习建议

### 时间管理

1. **每天 6-8 小时**：上午（3h）+ 下午（3h）+ 晚上（2h）
2. **50% 实践**：一半时间动手写代码
3. **20% 理论**：理解概念和原理
4. **20% 调试**：解决问题和优化
5. **10% 总结**：写笔记和复盘

### 核心原则

✅ 动手实践 > 理论学习
✅ 完成项目 > 完成课程
✅ 真实应用 > 纸上谈兵
✅ 持续迭代 > 一次完成
✅ 坚持不懈 > 三天打鱼
✅ 主动沟通 > 闭门造车

### 避坑指南

- ❌ 不要花太多时间调 prompt，先把功能做出来
- ❌ 不要追求完美代码，先跑通再说
- ❌ 不要同时学太多框架，一个一个来
- ✅ 遇到 bug 优先查官方文档
- ✅ 多读开源项目的源码
- ✅ 保持代码整洁，养成好习惯

---

## 📚 推荐资源

### Python

- [菜鸟教程](https://www.runoob.com/python3/)
- [Python 官方文档](https://docs.python.org/zh-cn/3/)
- [Python 100 天](https://github.com/jackfrued/Python-100-Days)

### OpenAI API

- [OpenAI API 官方文档](https://platform.openai.com/docs)
- [OpenAI Cookbook](https://cookbook.openai.com)
- [Function Calling 指南](https://platform.openai.com/docs/guides/function-calling)

### LangChain

- [LangChain 官方文档](https://python.langchain.com/docs)
- [LangChain Cookbook](https://github.com/langchain-ai/langchain/tree/master/cookbook)

### RAG & 向量数据库

- [Chroma 文档](https://docs.trychroma.com)
- [FAISS](https://github.com/facebookresearch/faiss)
- [RAG 最佳实践](https://docs.llamaindex.ai/en/stable/understanding/rag.html)

### FastAPI

- [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)
- [FastAPI 最佳实践](https://github.com/zhanymkanov/fastapi-best-practices)

### Docker & 部署

- [Docker 入门教程](https://docs.docker.com/get-started/)
- [Railway](https://railway.app)

---

## 📅 30 天冲刺路线

```
第1周 🏗️   基础搭建
  Day 1-2:  Python 基础 → 菜鸟教程刷一遍
  Day 3-4:  OpenAI API → 实现基础对话
  Day 5-6:  Prompt + Function Calling
  Day 7:    📦 项目0：聊天机器人

第2周 🔧   Agent 入门
  Day 8-9:  LangChain → Chain + Memory
  Day 10-11: Tool + Agent
  Day 12-13: 输出解析 + 综合实战
  Day 14:   📦 项目1：工具调用 Agent

第3周 🚀   进阶实战
  Day 15-16: RAG 基础 + 向量数据库
  Day 17-18: 文档处理 + 检索链
  Day 19:   📦 项目2：RAG 问答系统
  Day 20-21: 📦 项目3：Coding Agent + 优化

第4周 🎯   工程化 + 求职
  Day 22-23: FastAPI + API 集成
  Day 24:   Docker 部署
  Day 25:   Streamlit 前端
  Day 26:   GitHub 整理
  Day 27:   简历 + 面试准备
  Day 28-30: 📮 投递冲刺
```

---

> **💪 加油！30天后，你就是一个有 4 个 AI Agent 项目经验的候选人！**
>
> **记住：面试官看重的不是你会多少，而是你做过什么。4 个项目的实战经验，已经超过 90% 的候选人！**
