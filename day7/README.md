# AI ChatBot - 智能聊天机器人

一个基于大语言模型的智能聊天机器人，支持多工具调用、对话记忆、流式输出等功能。

---

## 目录

1. [项目概述](#1-项目概述)
2. [项目结构](#2-项目结构)
3. [环境配置](#3-环境配置)
4. [文件详解](#4-文件详解)
   - [config.py - 配置文件](#41-configpy---配置文件)
   - [.env - 环境变量](#42-env---环境变量)
   - [.gitignore - Git 忽略配置](#43-gitignore---git-忽略配置)
   - [prompts.py - 提示词管理](#44-promptspy---提示词管理)
   - [memory.py - 对话记忆](#45-memorypy---对话记忆)
   - [tools.py - 工具函数](#46-toolspy---工具函数)
   - [main.py - 主程序](#47-mainpy---主程序)
5. [核心机制详解](#5-核心机制详解)
   - [Function Calling 工作流程](#51-function-calling-工作流程)
   - [对话记忆管理](#52-对话记忆管理)
   - [流式输出实现](#53-流式输出实现)
6. [运行效果](#6-运行效果)
7. [常见问题](#7-常见问题)
8. [扩展指南](#8-扩展指南)

---

## 1. 项目概述

这是一个功能完整的 AI 聊天机器人，具备以下特性：

| 功能 | 说明 |
|------|------|
| **多工具调用** | 支持天气查询、数学计算、文本翻译 |
| **对话记忆** | 记住之前的对话内容，支持多轮对话 |
| **流式输出** | 打字机效果，逐字显示回复 |
| **智能路由** | 根据用户意图自动选择合适的工具 |
| **记忆管理** | 自动限制对话长度，避免 token 浪费 |
| **美化界面** | 使用 rich 库美化终端输出 |

**技术栈：**
- Python 3.10+
- OpenAI SDK（兼容 DeepSeek API）
- Rich（终端美化）
- python-dotenv（环境变量管理）

---

## 2. 项目结构

```
day7/
├── main.py            # 主程序入口，包含完整的对话循环逻辑
├── config.py          # 配置文件，读取环境变量和 API 配置
├── prompts.py         # 提示词管理，存储系统提示词
├── memory.py          # 对话记忆管理类，负责存储和限制对话历史
├── tools.py           # 工具函数实现（天气、计算、翻译）
├── requirements.txt   # 依赖包列表
├── .env               # 环境变量（API Key 等敏感信息）
├── .gitignore         # Git 忽略配置
└── README.md          # 项目文档
```

**各文件职责：**
- `config.py` - 从 `.env` 文件读取配置，供其他模块使用
- `prompts.py` - 定义 AI 助手的行为和角色
- `memory.py` - 管理对话历史，支持添加、获取、清除、限制
- `tools.py` - 实现具体的工具功能
- `main.py` - 整合所有模块，运行主循环
- `.gitignore` - 告诉 Git 忽略哪些文件（如 `.env`、`__pycache__/`）

---

## 3. 环境配置

### 3.1 安装依赖

```bash
pip install -r requirements.txt
```

**依赖包说明：**
- `openai` - OpenAI SDK，用于调用大语言模型 API
- `python-dotenv` - 从 `.env` 文件读取环境变量
- `rich` - 终端美化库，提供彩色输出和面板显示

### 3.2 配置 API Key

在 `.env` 文件中配置你的 API Key：

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

**注意事项：**
- API Key 是敏感信息，不要提交到 Git 仓库
- `.env` 文件应该在 `.gitignore` 中
- 可以在 DeepSeek 官网获取 API Key：https://platform.deepseek.com/

### 3.3 运行程序

```bash
python main.py
```

---

## 4. 文件详解

### 4.1 config.py - 配置文件

**作用：** 集中管理所有配置，从 `.env` 文件读取敏感信息。

```python
from dotenv import load_dotenv
import os

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量读取 API Key
# 如果 .env 文件不存在或未设置，会返回 None
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# DeepSeek API 地址
# 这是 DeepSeek 官方提供的 API 地址
OPENAI_BASE_URL = "https://api.deepseek.com"

# 使用的模型名称
# deepseek-chat 是 DeepSeek 的对话模型
MODEL_NAME = "deepseek-chat"
```

**关键点：**
1. `load_dotenv()` - 加载 `.env` 文件中的变量到环境变量中
2. `os.getenv("OPENAI_API_KEY")` - 从环境变量中读取 API Key
3. `OPENAI_BASE_URL` - 指定 API 服务器地址（使用 DeepSeek 需要设置）

**为什么用 .env 文件？**
- 安全性：API Key 等敏感信息不直接写在代码中
- 灵活性：不同环境可以使用不同的配置
- 可维护性：配置集中管理，便于修改

---

### 4.2 .env - 环境变量

**作用：** 存储敏感配置信息，如 API Key。

```env
OPENAI_API_KEY=sk-0d4dbba6da8544c2abcd4338c87b6b55
```

**格式说明：**
- 每行一个变量，格式为 `KEY=VALUE`
- 不需要引号包裹值
- 支持注释（以 `#` 开头）
- 文件名必须是 `.env`

**安全提醒：**
- 永远不要将 `.env` 文件提交到 Git
- 在 `.gitignore` 中添加 `.env`
- 如果 Key 泄露，立即去官网重新生成

---

### 4.3 .gitignore - Git 忽略配置

**作用：** 告诉 Git 哪些文件不应该被提交到版本控制。

```gitignore
# ==============================
# 环境变量文件（敏感信息）
# ==============================
.env
.env.local
.env.*.local

# ==============================
# Python 相关
# ==============================
# 编译的 Python 文件
__pycache__/
*.py[cod]
*$py.class
*.pyo

# 虚拟环境
venv/
env/
.venv/
.env/

# 分发/打包
dist/
build/
*.egg-info/
*.egg

# ==============================
# IDE 相关
# ==============================
# VS Code
.vscode/
*.code-workspace

# JetBrains (PyCharm)
.idea/
*.iml

# ==============================
# 操作系统相关
# ==============================
# Windows
Thumbs.db
ehthumbs.db
Desktop.ini

# macOS
.DS_Store
.AppleDouble
.LSOverride

# Linux
*~

# ==============================
# 日志和临时文件
# ==============================
*.log
*.tmp
*.bak
*.swp
*.swo
```

**为什么需要 .gitignore？**

1. **保护敏感信息** - API Key、密码等不能提交到 Git
2. **避免垃圾文件** - 编译文件、日志文件不应该被跟踪
3. **减少仓库大小** - 忽略不必要的文件
4. **团队协作** - 确保每个人都有相同的配置

**常见忽略规则：**

| 规则 | 说明 |
|------|------|
| `.env` | 忽略环境变量文件 |
| `__pycache__/` | 忽略 Python 编译缓存 |
| `*.py[cod]` | 忽略 .pyc、.pyo、.pyd 文件 |
| `venv/` | 忽略虚拟环境目录 |
| `.vscode/` | 忽略 VS Code 配置 |
| `.idea/` | 忽略 PyCharm 配置 |
| `*.log` | 忽略所有日志文件 |

**如果 .env 已被 Git 跟踪：**

```bash
# 方法 1：从 Git 中移除（保留本地文件）
git rm --cached .env
git commit -m "从 Git 中移除 .env"

# 方法 2：同时从 Git 和本地删除
git rm .env
git commit -m "删除 .env"
```

**最佳实践：**
- 项目初始化时就创建 `.gitignore`
- 将 `.gitignore` 提交到 Git 仓库
- 在 `README.md` 中说明需要配置 `.env`
- 提供 `.env.example` 模板文件

---

### 4.4 prompts.py - 提示词管理

**作用：** 存储系统提示词，定义 AI 助手的行为和角色。

```python
SYSTEM_PROMPT = """
你是一个专业AI助手。

你的特点：
1. 回答简洁清晰
2. 优先使用工具
3. 数学问题调用计算器
4. 天气问题调用天气工具
5. 翻译问题调用翻译工具
6. 语气自然友好

请尽可能帮助用户。
"""
```

**系统提示词的作用：**
1. **定义角色** - 告诉模型它是"专业AI助手"
2. **设定行为** - 指导模型如何回答问题
3. **工具引导** - 告诉模型何时使用哪个工具
4. **语气设定** - 要求"语气自然友好"

**为什么单独放一个文件？**
- 便于修改和维护
- 可以快速调整 AI 的行为
- 不需要修改其他代码

---

### 4.5 memory.py - 对话记忆

**作用：** 管理对话历史，支持多轮对话。

```python
class Memory:

    def __init__(self):
        """初始化空的对话历史"""
        self.messages = []

    def add_message(self, role, content):
        """
        添加一条消息到对话历史

        Args:
            role: 角色（system/user/assistant/tool）
            content: 消息内容
        """
        self.messages.append({
            "role": role,
            "content": content
        })

    def get_messages(self):
        """获取完整的对话历史"""
        return self.messages

    def clear_memory(self):
        """清空对话历史"""
        self.messages = []

    def limit_memory(self, max_length=20):
        """
        限制对话历史长度

        Args:
            max_length: 最大消息数量，默认 20
        """
        if len(self.messages) > max_length:
            # 保留最近的 max_length 条消息
            self.messages = self.messages[-max_length:]
```

**消息角色说明：**
- `system` - 系统消息，定义 AI 的行为（始终在最前面）
- `user` - 用户消息
- `assistant` - AI 助手的回复
- `tool` - 工具调用的结果

**为什么需要限制记忆长度？**
- 大语言模型有 token 限制（上下文长度）
- 对话太长会消耗大量 token
- 保留最近的对话即可满足大部分需求
- 默认保留最近 20 条消息

---

### 4.6 tools.py - 工具函数

**作用：** 实现具体的工具功能（天气、计算、翻译）。

#### 4.5.1 天气工具

```python
def get_weather(city):
    """
    获取城市天气信息（模拟数据）

    Args:
        city: 城市名称

    Returns:
        天气信息字符串
    """
    weather_data = {
        "北京": "25°C，晴天",
        "上海": "28°C，多云",
        "广州": "32°C，暴雨",
        "深圳": "30°C，小雨",
        "杭州": "26°C，阴天"
    }
    return weather_data.get(city, "未找到该城市天气")
```

**说明：** 这是模拟数据，实际应用中可以调用真实天气 API（如 Open-Meteo）。

#### 4.5.2 计算器工具

```python
def calculator(expression):
    """
    执行数学计算

    Args:
        expression: 数学表达式，如 "2 + 3 * 4"

    Returns:
        计算结果字符串
    """
    try:
        # 使用 Python 的 eval() 执行表达式
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算错误：{e}"
```

**注意：** `eval()` 有安全风险，在生产环境中应该使用更安全的解析方式。

#### 4.5.3 翻译工具

```python
def translate(text, target_language):
    """
    文本翻译（模拟数据）

    Args:
        text: 待翻译文本
        target_language: 目标语言

    Returns:
        翻译结果字符串
    """
    translations = {
        ("你好", "英文"): "Hello",
        ("谢谢", "英文"): "Thank you",
        ("再见", "英文"): "Goodbye",
        ("hello", "中文"): "你好",
        ("thank you", "中文"): "谢谢",
        ("goodbye", "中文"): "再见"
    }
    return translations.get(
        (text.lower(), target_language),
        "暂时无法翻译"
    )
```

**说明：** 这是模拟数据，实际应用中可以调用翻译 API。

---

### 4.7 main.py - 主程序

**作用：** 整合所有模块，运行主循环。

#### 4.6.1 导入和初始化

```python
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
import json
import time

from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from prompts import SYSTEM_PROMPT
from memory import Memory
from tools import get_weather, calculator, translate

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

# 初始化 Rich 控制台（用于美化输出）
console = Console()

# 初始化对话记忆
memory = Memory()
```

#### 4.6.2 系统提示词设置

```python
# 将系统提示词添加到对话历史
memory.add_message("system", SYSTEM_PROMPT)
```

#### 4.6.3 工具描述定义

```python
# 定义可用工具的描述（告诉模型有哪些工具可用）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        }
    },
    # ... 其他工具
]
```

#### 4.6.4 主循环流程

```
┌─────────────────────────────────────────────────────────────┐
│                        主循环流程                             │
├─────────────────────────────────────────────────────────────┤
│  1. 获取用户输入                                              │
│       ↓                                                      │
│  2. 检查是否退出（quit）                                       │
│       ↓                                                      │
│  3. 保存用户消息到记忆                                         │
│       ↓                                                      │
│  4. 限制记忆长度                                              │
│       ↓                                                      │
│  5. 第一次 API 调用（带工具描述）                               │
│       ↓                                                      │
│  6. 检查是否有工具调用                                          │
│       ├── 有工具调用 ──→ 执行工具 ──→ 第二次 API 调用         │
│       └── 无工具调用 ──→ 直接流式输出                          │
│       ↓                                                      │
│  7. 保存 AI 回复到记忆                                         │
│       ↓                                                      │
│  8. 返回步骤 1                                                │
└─────────────────────────────────────────────────────────────┘
```

#### 4.6.5 工具调用处理

```python
if tool_calls:
    # 1. 解析工具调用
    tool_call = tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    # 2. 执行对应工具
    if function_name == "get_weather":
        result = get_weather(arguments["city"])
    elif function_name == "calculator":
        result = calculator(arguments["expression"])
    elif function_name == "translate":
        result = translate(arguments["text"], arguments["target_language"])

    # 3. 将工具结果添加到记忆
    memory.messages.append(response_message)  # 工具调用请求
    memory.messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    })

    # 4. 第二次 API 调用，让 AI 根据工具结果生成回复
    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=memory.get_messages(),
        stream=True
    )
```

---

## 5. 核心机制详解

### 5.1 Function Calling 工作流程

Function Calling 是让大语言模型调用外部工具的技术。

**完整流程：**

```
用户输入："北京天气怎么样？"
        ↓
┌─────────────────────────────────────────┐
│ 第一次 API 调用                          │
│                                         │
│ 输入：                                   │
│   messages: [用户消息]                   │
│   tools: [工具描述]                      │
│                                         │
│ 输出：                                   │
│   message.tool_calls = [{               │
│     function: "get_weather",            │
│     arguments: {"city": "北京"}          │
│   }]                                    │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ 执行工具                                 │
│                                         │
│ get_weather("北京")                      │
│ 返回："25°C，晴天"                        │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ 第二次 API 调用                          │
│                                         │
│ 输入：                                   │
│   messages: [用户消息, 工具调用, 工具结果] │
│                                         │
│ 输出：                                   │
│   "北京今天天气晴朗，温度 25°C，           │
│    适合出门活动。"                        │
└─────────────────────────────────────────┘
```

**为什么需要两次 API 调用？**
1. 第一次：让模型决定是否需要调用工具，以及调用哪个工具
2. 第二次：让模型根据工具结果生成自然语言回复

---

### 5.2 对话记忆管理

对话记忆是多轮对话的基础。

**消息存储结构：**

```python
memory.messages = [
    # 系统提示词（始终在最前面）
    {"role": "system", "content": "你是一个专业AI助手..."},

    # 用户消息
    {"role": "user", "content": "北京天气怎么样？"},

    # AI 回复（可能包含工具调用）
    {"role": "assistant", "content": null, "tool_calls": [...]},

    # 工具结果
    {"role": "tool", "tool_call_id": "call_xxx", "content": "25°C，晴天"},

    # AI 最终回复
    {"role": "assistant", "content": "北京今天天气晴朗..."},

    # 下一轮对话...
]
```

**记忆限制机制：**

```python
def limit_memory(self, max_length=20):
    if len(self.messages) > max_length:
        # 保留最近的 max_length 条消息
        self.messages = self.messages[-max_length:]
```

**示例：**
- 假设有 25 条消息，限制为 20 条
- 删除前 5 条，保留最近 20 条
- 系统提示词会在删除时丢失，需要重新添加

---

### 5.3 流式输出实现

流式输出让用户看到"打字机"效果。

**实现原理：**

```python
# 启用流式输出
stream = client.chat.completions.create(
    model=MODEL_NAME,
    messages=memory.get_messages(),
    stream=True  # 关键参数
)

# 逐个 chunk 处理
for chunk in stream:
    delta = chunk.choices[0].delta
    if delta.content:
        text = delta.content
        print(text, end="", flush=True)  # 逐字打印
        full_response += text  # 拼接完整回复
```

**参数说明：**
- `stream=True` - 启用流式输出
- `delta.content` - 当前 chunk 的文本内容
- `end=""` - 不换行
- `flush=True` - 立即刷新输出缓冲区

**流式输出 vs 普通输出：**

| 特性 | 流式输出 | 普通输出 |
|------|---------|---------|
| 响应速度 | 快（首字节快） | 慢（等全部生成） |
| 用户体验 | 好（打字机效果） | 差（长时间无响应） |
| 实现复杂度 | 高 | 低 |
| Token 消耗 | 相同 | 相同 |

---

## 6. 运行效果

**启动界面：**

```
╭───────────────────────╮
│ AI ChatBot 启动成功！ │
│ 输入 quit 退出        │
╰───────────────────────╯
```

**天气查询示例：**

```
你: 北京天气怎么样？

[调用工具] get_weather
[工具结果] 25°C，晴天

AI: 北京今天天气晴朗，温度 25°C，非常适合出门活动。建议做好防晒措施。
```

**数学计算示例：**

```
你: 计算 2 + 3 * 4

[调用工具] calculator
[工具结果] 计算结果：14

AI: 计算结果是 14。根据数学运算优先级，先算乘法 3 * 4 = 12，再算加法 2 + 12 = 14。
```

**翻译示例：**

```
你: 把 hello 翻译成中文

[调用工具] translate
[工具结果] 你好

AI: "hello" 的中文翻译是"你好"。
```

**普通聊天示例：**

```
你: 你好！

AI: 你好！我是你的 AI 助手，有什么可以帮你的吗？我可以帮你查询天气、做数学计算，或者翻译文本。
```

---

## 7. 常见问题

### 7.1 API Key 错误

**错误信息：**
```
openai.AuthenticationError: Error code: 401 - Incorrect API key
```

**解决方案：**
1. 检查 `.env` 文件中的 API Key 是否正确
2. 确认 API Key 是否过期或被撤销
3. 确认 `base_url` 是否正确指向 DeepSeek API

### 7.2 模型不调用工具

**问题描述：** 用户问天气问题，但 AI 没有调用天气工具。

**可能原因：**
1. 工具描述不够清晰
2. 系统提示词没有明确要求使用工具
3. 模型版本不支持 Function Calling

**解决方案：**
1. 完善工具的 `description` 字段
2. 在系统提示词中明确说明何时使用工具
3. 使用支持 Function Calling 的模型（如 deepseek-chat）

### 7.3 记忆丢失

**问题描述：** AI 忘记了之前的对话内容。

**可能原因：**
1. 对话历史超过 `max_length` 限制
2. 系统提示词被删除

**解决方案：**
1. 增大 `max_length` 参数
2. 在 `limit_memory` 中保留系统提示词

### 7.4 Token 消耗过多

**问题描述：** API 调用费用过高。

**解决方案：**
1. 减小 `max_length` 参数
2. 精简系统提示词
3. 使用更便宜的模型

---

## 8. 扩展指南

### 8.1 添加新工具

**步骤 1：在 tools.py 中实现函数**

```python
def search_web(query):
    """搜索网页"""
    # 调用搜索 API
    return f"搜索结果：{query}"
```

**步骤 2：在 main.py 中添加工具描述**

```python
tools.append({
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "搜索网页信息",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词"
                }
            },
            "required": ["query"]
        }
    }
})
```

**步骤 3：在 main.py 中处理工具调用**

```python
elif function_name == "search_web":
    result = search_web(arguments["query"])
```

### 8.2 使用真实天气 API

将 `tools.py` 中的 `get_weather` 函数替换为真实 API 调用：

```python
import requests

def get_weather(city):
    coords = {"北京": (39.9, 116.4), "上海": (31.2, 121.5)}
    if city not in coords:
        return f"暂不支持 {city}"

    lat, lon = coords[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    data = response.json()

    temp = data["current_weather"]["temperature"]
    code = data["current_weather"]["weathercode"]
    return f"{city}：{temp}°C"
```

### 8.3 添加数据库持久化

将对话历史保存到数据库，实现跨会话记忆：

```python
import sqlite3

class DatabaseMemory:
    def __init__(self, db_path="chat.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                role TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def add_message(self, role, content):
        self.conn.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)",
            (role, content)
        )
        self.conn.commit()
```

### 8.4 添加 Web 界面

使用 Flask 或 Gradio 创建 Web 界面：

```python
import gradio as gr

def chat(message, history):
    # 调用 AI 接口
    response = get_ai_response(message)
    return response

demo = gr.ChatInterface(
    fn=chat,
    title="AI ChatBot",
    description="智能聊天机器人"
)

demo.launch()
```

---

## 附录：API 调用示例

### 基本对话

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "你好"}
    ]
)
print(response.choices[0].message.content)
```

### 工具调用

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "北京天气"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取天气",
            "parameters": {"type": "object", "properties": {"city": {"type": "string"}}}
        }
    }]
)
```

### 流式输出

```python
stream = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "讲个故事"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

---

**最后更新：** 2024 年
