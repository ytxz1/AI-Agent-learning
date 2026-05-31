# Day 10 - Tools 工具：让 AI 拥有超能力

> 学习目标：掌握 LangChain 的 Tools 系统，让 AI 能够调用外部工具。
> 预计阅读时间：30+ 分钟

---

## 目录

1. 什么是 Tools
2. 为什么需要 Tools
3. 工具的三要素
4. 自定义工具
5. LLM 工具调用原理
6. 工具调用完整流程
7. 多工具协作
8. 工具代理 Agent
9. 综合实践项目
10. 最佳实践
11. 常见问题
12. 知识总结
13. 练习题

---

## 1. 什么是 Tools

### 1.1 一句话解释

**Tools 就是 AI 的超能力**——让 AI 能够执行它本身做不到的事情。

### 1.2 生活中的类比

没有工具的 AI：
- 你: 北京天气怎么样？
- AI: 我不知道...我没有联网...
- 你: 帮我算 123 * 456
- AI: 嗯...大概是几万？我不确定...

有工具的 AI：
- 你: 北京天气怎么样？
- AI: [调用天气工具] 北京25度，晴天！
- 你: 帮我算 123 * 456
- AI: [调用计算器] 56088！

### 1.3 AI 本身能做什么 vs 需要工具

| AI 本身能做的 | 需要工具才能做的 |
|--------------|----------------|
| 回答知识性问题 | 精确数学计算 |
| 文本生成/翻译 | 查询实时信息 |
| 代码生成 | 搜索互联网 |
| 文本摘要/分析 | 读写文件 |
| 对话聊天 | 发送邮件/消息 |

---

## 2. 为什么需要 Tools

### 2.1 LLM 的局限性

1. **不能做精确计算**
   - 问: 123456 * 789012 = ?
   - AI: 大约是 970 亿？（不精确！）
   - 原因: LLM 是预测下一个词，不是计算器

2. **没有实时信息**
   - 问: 今天天气怎么样？
   - AI: 我不知道今天天气...（没有联网）
   - 原因: LLM 的知识截止到训练日期

3. **不能执行代码**
   - 问: 帮我运行这段 Python 代码
   - AI: 我可以生成代码，但不能运行...
   - 原因: LLM 只能生成文本，不能执行

### 2.2 Tools 如何解决这些问题

| LLM 的局限性 | Tools 的解决方案 |
|-------------|----------------|
| 不能精确计算 | calculator 工具 |
| 没有实时信息 | weather/search 工具 |
| 不能执行代码 | code_executer 工具 |
| 不能访问外部 | api_caller 工具 |

原理：LLM 不直接做这些事，而是指挥工具去做
就像老板不亲自干活，而是分配任务给员工

### 2.3 Agent 的核心思想

**Agent = LLM + Tools + 推理**

```
用户问题
    |
    v
+--------+
|  LLM   |  <-- 大脑：决定用哪个工具
+----+---+
     |
     +---> calculator（计算）
     +---> weather（天气）
     +---> search（搜索）
     |
     v
最终答案
```

---

## 3. 工具的三要素

每个工具都需要三个关键信息：

| 要素 | 作用 |
|------|------|
| 名称 | AI 通过名称来识别和调用工具 |
| 描述 | AI 据此判断何时应该调用这个工具 |
| 参数 | AI 从用户问题中提取参数值 |
| 返回值 | 工具执行后的结果，反馈给 AI |

### 示例：天气工具

```python
@tool
def get_weather(city: str) -> str:
    """获取城市天气信息。当用户问天气时使用此工具。"""
    # 函数名 = 工具名 ("get_weather")
    # docstring = 工具描述
    # 参数 city: str = 输入参数
    # 返回值 str = 执行结果
    return f"{city}今天25度，晴天"
```

### AI 如何决定调用哪个工具

用户: "北京天气怎么样？"

LLM 看到所有可用工具的描述：
  1. calculator: "执行数学计算..."
  2. get_weather: "获取城市天气..."  <-- 匹配！
  3. translate: "翻译文本..."

LLM 判断: 问题包含"天气"，匹配 get_weather
LLM 提取参数: city = "北京"

---

## 4. 自定义工具

> 对应文件: 02_custom_tool.py

### 4.1 使用 @tool 装饰器（推荐）

最简单的方式：给函数加上 @tool 装饰器。

```python
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """将两个整数相乘。

    参数:
        a: 第一个整数
        b: 第二个整数
    """
    return a * b

# 使用
result = multiply.invoke({"a": 6, "b": 7})
print(result)  # 42
```

### 4.2 使用 Pydantic 模型定义输入

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    """天气查询的输入参数"""
    city: str = Field(description="城市名称")
    unit: str = Field(default="celsius", description="温度单位")

@tool(args_schema=WeatherInput)
def get_weather(city: str, unit: str = "celsius") -> str:
    """查询城市天气信息。"""
    return f"{city}今天25度"
```

### 4.3 docstring 很重要

好的 docstring:
- """获取城市天气信息。当用户问天气时使用此工具。"""
- AI 知道：这个工具用来查天气

坏的 docstring:
- """工具"""
- AI 不知道：这个工具干什么？

建议：
1. 一句话描述功能
2. 说明什么时候使用
3. 列出参数的含义

---

## 5. LLM 工具调用原理

> 对应文件: 03_tool_calling.py

### 5.1 工具调用的三步流程

Step 1: bind_tools() - 把工具信息告诉 LLM
- llm_with_tools = llm.bind_tools(tools)
- 把所有工具的名称、描述、参数 schema 附加到 LLM
- 相当于给 LLM 一份工具说明书

Step 2: invoke() - LLM 分析问题并决定调用
- response = llm_with_tools.invoke(msgs)
- LLM 分析问题，判断是否需要调用工具
- 如果需要，选择工具并生成参数
- 输出: AIMessage(tool_calls=[...])

Step 3: 执行工具 - 程序调用工具获取结果
- for tool_call in response.tool_calls:
-     result = tool.invoke(tool_call)
-     messages.append(ToolMessage(...))

### 5.2 tool_calls 的结构

```python
response.tool_calls = [
    {
        "name": "get_weather",      # 工具名称
        "args": {"city": "北京"},   # 提取的参数
        "id": "call_abc123",        # 调用 ID
    }
]
```

---

## 6. 工具调用完整流程

### 6.1 完整代码模板（必背）

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

# 1. 定义工具
@tool
def get_weather(city: str) -> str:
    """获取城市天气信息。当用户问天气时使用。"""
    return f"{city}今天25度，晴天"

# 2. 创建 LLM 并绑定工具
llm = ChatOpenAI(model="deepseek-chat")
llm_with_tools = llm.bind_tools([get_weather])

# 3. 第一次调用：LLM 决定调用哪个工具
messages = [HumanMessage(content="北京天气怎么样？")]
response = llm_with_tools.invoke(messages)
messages.append(response)

# 4. 执行工具调用
if response.tool_calls:
    for tc in response.tool_calls:
        result = get_weather.invoke(tc["args"])
        messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))

# 5. 第二次调用：LLM 根据工具结果生成最终回复
final_response = llm_with_tools.invoke(messages)
print(final_response.content)
```

### 6.2 数据流图解

```
用户: "北京天气怎么样？"
    |
    v
[Step 1] LLM 分析问题
    |  --> 判断需要调用 get_weather 工具
    |  --> 提取参数: city = "北京"
    v
[Step 2] 返回 tool_calls
    |  --> [{name: "get_weather", args: {city: "北京"}}]
    v
[Step 3] 程序执行工具
    |  --> result = get_weather("北京") = "25度，晴天"
    v
[Step 4] 结果发回 LLM
    |  --> ToolMessage(content="25度，晴天")
    v
[Step 5] LLM 生成最终回复
    |  --> "北京今天25度，晴天，适合出门。"
    v
用户看到回复
```

---

## 7. 多工具协作

### 7.1 定义多个工具

```python
@tool
def calculator(expression: str) -> str:
    """执行数学计算。"""
    return str(eval(expression))

@tool
def get_weather(city: str) -> str:
    """获取城市天气。"""
    return f"{city}今天25度"

# 一次绑定所有工具
llm_with_tools = llm.bind_tools([calculator, get_weather])
```

### 7.2 LLM 自动选择

| 用户问题 | LLM 选择的工具 |
|---------|--------------|
| "123 * 456" | calculator |
| "北京天气" | get_weather |
| "你好" | 不调用任何工具 |

---

## 8. 工具代理 Agent

> 对应文件: 04_tool_agent.py

### 8.1 什么是 Agent

**Agent = LLM + Tools + 循环推理**

普通 Chain: 输入 --> LLM --> 输出（一次调用）
Agent:      输入 --> LLM --> 工具 --> LLM --> 工具 --> ... --> 输出
            （可能多次调用，直到得到最终答案）

### 8.2 Agent 循环

```
用户输入
    |
    v
+--------+
|  LLM   | <---------+
+----+---+           |
     |               |
     +-- 需要工具？--是--> 执行工具 --> 结果发回 LLM
     |               |
     +-- 不需要？--是--> 输出最终答案
```

### 8.3 Agent 代码模板

```python
def run_agent(user_input, max_rounds=5):
    llm_with_tools = llm.bind_tools(tools)
    messages = [HumanMessage(content=user_input)]

    for _ in range(max_rounds):
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            for tc in response.tool_calls:
                result = find_tool(tc["name"]).invoke(tc["args"])
                messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
        else:
            return response.content

    return "达到最大轮数"
```

---

## 9. 综合实践项目

> 对应文件: main.py

### 9.1 项目功能

智能工具助手，支持4种工具：
- calculator: 数学计算
- get_weather: 天气查询
- translate: 翻译
- search: 知识搜索

AI 会自动选择合适的工具来回答你的问题。

---

## 10. 最佳实践

1. **工具命名要清晰**
   - 好: get_weather, calculate, search
   - 坏: tool1, func, do_something

2. **docstring 要详细**
   - 一句话描述功能
   - 说明什么时候使用
   - 列出参数含义

3. **参数要有类型注解**
   - 好: def get_weather(city: str) -> str:
   - 坏: def get_weather(city):

4. **返回值要是字符串**
   - LLM 只能处理文本

5. **错误处理要完善**
   - 工具应该返回错误信息，而不是抛出异常

6. **工具数量要适中**
   - 建议: 3~10 个工具

---

## 11. 常见问题

### Q1: LLM 不调用工具
检查 docstring 是否清晰，是否说明了什么时候使用。

### Q2: 工具参数提取错误
检查参数名和类型注解是否清晰。

### Q3: Agent 无限循环
设置 max_rounds 限制最大调用轮数。

---

## 12. 知识总结

### 12.1 学习路线

```
Day 8: LangChain入门
Day 9: Memory记忆
Day 10: Tools工具
  --> 工具的定义（@tool 装饰器）
  --> 工具的三要素（名称、描述、参数）
  --> bind_tools() 绑定工具
  --> tool_calls 解析
  --> ToolMessage 结果回传
  --> Agent 循环
          |
          v
Day 11: Agents代理 = Memory + Tools + 推理
```

### 12.2 文件清单

```
day10/
├── config.py              # 配置文件
├── main.py                # 综合实践
├── 01_tool_basics.py      # 工具基础概念
├── 02_custom_tool.py      # 自定义工具
├── 03_tool_calling.py     # LLM 工具调用
├── 04_tool_agent.py       # 工具代理
├── tools/                 # 工具模块
│   ├── __init__.py
│   ├── calculator.py
│   ├── weather.py
│   ├── translator.py
│   └── search.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 13. 练习题

### 练习 1: 基础
运行 02_custom_tool.py，添加一个新的工具（如获取当前时间）。

### 练习 2: 中等
修改 04_tool_agent.py，添加一个读取文件工具。

### 练习 3: 进阶
构建一个代码助手 Agent，支持代码生成、解释、运行。

### 练习 4: 挑战
构建一个研究助手 Agent，支持搜索、总结、生成报告。

---

> 明天预告: Day 11 - Agents 代理，将 Memory + Tools + 推理整合，构建真正的智能代理。