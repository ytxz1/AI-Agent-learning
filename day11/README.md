# Day 11 - Agents 代理：构建真正的智能体

> **学习目标：** 掌握 LangChain 的 Agent 系统，将 LLM + Tools + Memory 整合，构建能自主决策的智能体。
>
> **预计阅读时间：** 30+ 分钟

---

## 目录

1. 什么是 Agent
2. Agent 的核心架构
3. Agent 与 Chain 的区别
4. ReAct 推理模式
5. 工具增强 Agent
6. 带记忆的 Agent
7. 多工具综合 Agent
8. Agent 的工作流程详解
9. 综合实践项目
10. 最佳实践
11. 常见问题
12. 知识总结
13. 练习题

---

## 1. 什么是 Agent

### 1.1 一句话解释

**Agent 就是拥有超能力的 AI** -- 它不仅能思考，还能使用工具、记住对话、自主决策。

### 1.2 生活中的类比

想象你是一个项目经理：

- **没有 Agent 的 AI** 就像一个只会纸上谈兵的顾问：
  - 你：帮我查一下北京天气
  - AI：我没有联网能力，无法查询...

- **有 Agent 的 AI** 就像一个能力全面的助理：
  - 你：帮我查一下北京天气
  - AI：[调用天气工具] 北京今天 25 度，晴天
  - 你：那帮我算一下气温的两倍是多少
  - AI：[记住上一步的 25，调用计算器] 50 度

### 1.3 Agent 的官方定义

**Agent = LLM + Tools + Memory + Reasoning**

| 组件 | 作用 | 类比 |
|------|------|------|
| LLM（大脑） | 理解问题、推理决策 | 人的思考能力 |
| Tools（工具） | 执行具体操作 | 人的手脚和工具箱 |
| Memory（记忆） | 记住对话历史 | 人的短期/长期记忆 |
| Reasoning（推理） | 分析问题、制定计划 | 人的逻辑思维 |

### 1.4 Agent 能做什么

| 场景 | 没有 Agent | 有 Agent |
|------|-----------|---------|
| 数学计算 | AI 猜测，不精确 | 调用计算器，精确计算 |
| 天气查询 | AI 说我不知道 | 调用天气 API，实时数据 |
| 多步任务 | 需要多次手动操作 | Agent 自动分解执行 |
| 记住上下文 | 每次对话都是新的 | 记住之前的对话内容 |
| 错误处理 | 流程中断 | Agent 可以重试或换方案 |

---

## 2. Agent 的核心架构

### 2.1 架构图

```
                    +--------------------------+
                    |     用户输入问题           |
                    +------------+-------------+
                                 |
                                 v
                    +--------------------------+
                    |    Agent（智能体核心）      |
                    |                          |
                    |  +--------------------+  |
                    |  |   LLM（大脑）        |  |
                    |  |   理解 + 推理 + 决策  |  |
                    |  +---------+----------+  |
                    |           |              |
                    |  +--------+---------+   |
                    |  |  Memory（记忆）    |   |
                    |  |  对话历史 + 上下文  |   |
                    |  +-------------------+   |
                    +------------+-------------+
                                 |
                    +------------+-------------+
                    |     Tools（工具集）        |
                    |                          |
                    |  +-----+ +-----+ +----+ |
                    |  |计算 | |天气 | |搜索| |
                    |  +-----+ +-----+ +----+ |
                    |  +-----+ +-----+ +----+ |
                    |  |时间 | |文本 | |换算| |
                    |  +-----+ +-----+ +----+ |
                    +--------------------------+
```

### 2.2 数据流向

```
用户: 北京天气怎么样？把气温转换成华氏度
    |
    +-> LLM 分析：需要先查天气，再做单位换算
    |
    +-> 调用 get_weather(北京)
    |   +-> 返回：北京天气：晴天，气温25C
    |
    +-> LLM 分析：气温是 25C，需要转华氏度
    |
    +-> 调用 unit_convert(25, 摄氏度, 华氏度)
    |   +-> 返回：25 摄氏度 = 77.0 华氏度
    |
    +-> LLM 组织最终答案
        +-> 北京今天晴天，气温25C（77F）
```

### 2.3 Agent 的四大核心能力

| 能力 | 说明 | 实现方式 |
|------|------|---------|
| **理解** | 理解用户的自然语言 | LLM 的语言理解能力 |
| **推理** | 分析问题，制定解决方案 | ReAct 推理模式 |
| **行动** | 调用工具执行具体操作 | Tool Calling 机制 |
| **记忆** | 记住对话历史和上下文 | Memory 系统 |

---

## 3. Agent 与 Chain 的区别

### 3.1 核心区别

| 对比项 | Chain（链） | Agent（代理） |
|--------|------------|--------------|
| **流程** | 固定顺序：A -> B -> C | 动态决策：根据情况选择 |
| **决策** | 开发者预先决定 | AI 运行时自主决定 |
| **工具使用** | 固定的工具调用 | AI 选择用哪个工具 |
| **循环** | 通常无循环 | 推理-行动循环 |
| **灵活性** | 低（改代码才能变） | 高（AI 自适应） |
| **适用场景** | 明确流程的任务 | 开放性、探索性任务 |
| **错误处理** | 流程中断 | AI 可以重试或换方案 |
| **透明度** | 黑盒 | 推理过程可见 |

### 3.2 代码对比

**Chain 的方式（固定流程）：**

```python
# Chain：开发者预先决定流程
chain = prompt | llm | output_parser
# 每次都是：prompt -> LLM -> 解析输出
result = chain.invoke({"topic": "Python"})
```

**Agent 的方式（动态决策）：**

```python
# Agent：AI 自主决定使用哪个工具
agent = create_react_agent(llm, tools, prompt)
# AI 会根据问题动态选择工具
result = agent.invoke({"input": "北京天气怎么样？"})
```

---

## 4. ReAct 推理模式

### 4.1 什么是 ReAct

**ReAct = Re(asoning) + Act(ing)**，即 **推理 + 行动**。

这是 Agent 最核心的工作模式，每一步都包含三个阶段：

```
+-------------------------------------+
|  Thought（思考）                      |
|  用户问的是天气，我需要调用天气工具    |
+-------------------------------------+
|  Action（行动）                       |
|  调用 get_weather(北京)               |
+-------------------------------------+
|  Observation（观察）                   |
|  北京：25C，晴天                      |
+--------------+----------------------+
               |
               +--> 回到 Thought，继续循环
```

### 4.2 ReAct 的完整示例

用户问题：**北京天气怎么样？把气温转换成华氏度**

```
Thought 1: 用户问了两个问题：查天气和单位换算。先查天气。
Action 1:  get_weather(北京)
Observation 1: 北京天气：晴天，气温25C

Thought 2: 现在知道北京气温是25C，需要转换成华氏度。
Action 2:  unit_convert(25, 摄氏度, 华氏度)
Observation 2: 25 摄氏度 = 77.0 华氏度

Thought 3: 现在有了所有信息，可以回答了。
Answer:    北京今天晴天，气温25C（77F）。
```

### 4.3 ReAct vs 普通 Chain

| 对比项 | 普通 Chain | ReAct Agent |
|--------|-----------|-------------|
| 推理过程 | 黑盒，用户看不到 | 每步都有思考过程 |
| 工具调用 | 开发者预先编排 | AI 自主决定 |
| 错误处理 | 流程中断 | AI 可以重试或换方案 |
| 透明度 | 低 | 高（可以看到推理链） |
| 灵活性 | 固定流程 | 动态适应 |

---

## 5. 工具增强 Agent

### 5.1 为什么需要多种工具

| 工具 | 功能 | 使用场景 |
|------|------|---------|
| calculator | 数学计算 | 帮我算一下 2 的 10 次方 |
| get_weather | 天气查询 | 北京天气怎么样？ |
| search_knowledge | 知识搜索 | 什么是机器学习？ |
| get_current_time | 获取时间 | 现在几点了？ |
| analyze_text | 文本分析 | 这段话有多少个字？ |
| unit_convert | 单位换算 | 25C 转华氏度 |

### 5.2 工具的定义规范

```python
@tool
def get_weather(city: str) -> str:
    # 功能描述：获取城市天气信息
    # 何时使用：当用户问天气时使用此工具
    # 参数说明：city - 城市名称
    return f"{city}: 25C, 晴天"
```

**关键要素：**
1. **函数名**：清晰描述功能
2. **类型注解**：参数和返回值都有类型
3. **docstring**：详细描述功能、使用时机、参数含义
4. **返回值**：始终返回字符串

---

## 6. 带记忆的 Agent

### 6.1 为什么 Agent 需要记忆

```
没有记忆：
  你：北京天气怎么样？
  Agent：北京 25C，晴天
  你：那上海呢？
  Agent：??? 你在说什么？

有记忆：
  你：北京天气怎么样？
  Agent：北京 25C，晴天
  你：那上海呢？
  Agent：上海 28C，多云（理解你在问天气）
```

### 6.2 记忆的实现方式

| 方式 | 说明 | 适用场景 |
|------|------|---------|
| **手动管理** | 开发者自己维护消息列表 | 需要精细控制 |
| **BufferMemory** | 保存所有对话历史 | 短对话 |
| **WindowMemory** | 只保留最近 K 轮 | 中等长度对话 |
| **SummaryMemory** | 压缩历史为摘要 | 长对话 |

### 6.3 手动管理记忆

```python
class MemoryAgent:
    def __init__(self, max_history=20):
        self.max_history = max_history
        self.messages = [SystemMessage(content="你是一个有记忆的助手...")]

    def chat(self, user_input):
        self.messages.append(HumanMessage(content=user_input))
        response = self.llm.invoke(self.messages)
        self.messages.append(response)
        self._trim_history()
        return response.content

    def _trim_history(self):
        if len(self.messages) > self.max_history:
            self.messages = [self.messages[0]] + self.messages[-(self.max_history-1):]
```

---

## 7. 多工具综合 Agent

### 7.1 完整 Agent 的架构

```
+-----------------------------------------------+
|              MultiToolAgent                    |
|                                               |
|  +----------+    +----------+                |
|  |   LLM    |    |  Memory  |                |
|  | (大脑)    |    | (记忆)    |                |
|  +----+-----+    +----------+                |
|       |                                       |
|  +----+------------------------------------+  |
|  |           Tools（工具集）                 |  |
|  |  calculator  get_weather  search         |  |
|  |  get_time    analyze     unit_convert    |  |
|  +------------------------------------------+  |
|                                               |
|  +------------------------------------------+  |
|  |  ReAct: Thought -> Action -> Observation |  |
|  +------------------------------------------+  |
+-----------------------------------------------+
```

### 7.2 MultiToolAgent 类

```python
class MultiToolAgent:
    def __init__(self, max_history=30, max_rounds=5):
        self.max_history = max_history
        self.max_rounds = max_rounds
        self.messages = [SystemMessage(content="...")]
        self.llm = ChatOpenAI(...).bind_tools(all_tools)

    def chat(self, user_input):
        self.messages.append(HumanMessage(content=user_input))
        for _ in range(self.max_rounds):
            response = self.llm.invoke(self.messages)
            self.messages.append(response)
            if response.tool_calls:
                for tc in response.tool_calls:
                    result = tool_map[tc["name"]].invoke(tc["args"])
                    self.messages.append(ToolMessage(...))
            else:
                self._trim_history()
                return response.content
        return "达到最大推理轮数。"
```

---

## 8. Agent 的工作流程详解

### 8.1 完整工作流程图

```
用户输入
    |
    v
+------------------+
|  添加到消息历史   |
+--------+---------+
         |
         v
+------------------+
|  发送给 LLM      |
+--------+---------+
         |
         v
+------------------+
|  LLM 分析响应    |
+--------+---------+
         |
    +----+----+
    |         |
    v         v
 有工具调用？  无工具调用
    |         |
    v         v
 执行工具    输出最终答案
    |
    v
 结果返回 LLM（循环）
```

---

## 9. 综合实践项目

> 对应文件：main.py

### 9.1 项目功能

交互式智能 Agent 助手，支持：
- 数学计算（三角函数、对数等）
- 天气查询（多城市）
- 知识搜索
- 时间查询
- 文本分析
- 单位换算
- 带记忆的连续对话

### 9.2 运行方式

```bash
python main.py
```

### 9.3 交互命令

| 命令 | 说明 |
|------|------|
| 直接输入 | 和 Agent 对话 |
| tools | 查看可用工具 |
| history | 查看对话历史 |
| clear | 清空历史 |
| example | 示例问题 |
| q | 退出 |

---

## 10. 最佳实践

### 10.1 工具设计

1. **命名清晰** - get_weather 而不是 tool1
2. **docstring 详细** - 描述功能、使用时机、参数
3. **类型注解** - city: str -> str
4. **返回字符串** - LLM 只能处理文本
5. **错误处理** - 返回错误信息而非抛异常
6. **数量适中** - 3~10 个工具

### 10.2 Agent 设计

1. **max_rounds** - 防止无限循环（3~5 轮）
2. **max_history** - 防止 Token 超限
3. **系统提示词** - 明确角色和能力
4. **显示过程** - 让用户知道 Agent 在做什么

---

## 11. 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 不调用工具 | docstring 不清晰 | 明确说明使用场景 |
| 调错工具 | 描述有歧义 | 避免功能重叠 |
| 无限循环 | 结果不明确 | 设置 max_rounds |
| Token 超限 | 历史太长 | 设置 max_history |
| 记不住对话 | 没有记忆系统 | 实现 MemoryAgent |

---

## 12. 知识总结

### 12.1 学习路线

```
Day 8: LangChain 入门
  |
Day 9: Memory 记忆
  |
Day 10: Tools 工具
  |
Day 11: Agents 代理 <- 你在这里
  |    +-- Agent 基础概念
  |    +-- ReAct 推理模式
  |    +-- 工具增强 Agent
  |    +-- 带记忆的 Agent
  |    +-- 多工具综合 Agent
  v
Day 12: RAG 检索增强生成
```

### 12.2 核心概念

| 概念 | 说明 | 关键代码 |
|------|------|---------|
| Agent | LLM+Tools+Memory+推理 | create_react_agent() |
| ReAct | Thought->Action->Observation | 推理循环 |
| Tool Calling | LLM 选择工具 | llm.bind_tools() |
| ToolMessage | 工具结果 | ToolMessage(content=result) |
| Memory | 对话历史 | messages 列表 |
| max_rounds | 最大轮数 | 防止无限循环 |
| max_history | 最大历史 | 防止 Token 超限 |

### 12.3 文件清单

```
day11/
+-- config.py              # 配置文件
+-- main.py                # 交互式 Agent 助手
+-- 01_agent_basics.py     # Agent 基础概念
+-- 02_react_agent.py      # ReAct 推理模式
+-- 03_tool_agent.py       # 工具增强 Agent
+-- 04_memory_agent.py     # 带记忆的 Agent
+-- 05_multi_tool_agent.py # 多工具综合 Agent
+-- tools/                 # 工具模块
+-- .env                   # 环境变量
+-- .gitignore
+-- requirements.txt
+-- README.md
```

---

## 13. 练习题

### 练习 1：基础（10 分钟）
运行 01_agent_basics.py，修改 max_rounds 参数观察效果。

### 练习 2：中等（20 分钟）
修改 03_tool_agent.py，添加新工具（如获取随机数）。

### 练习 3：进阶（30 分钟）
实现带窗口记忆的 Agent（只保留最近 10 轮对话）。

### 练习 4：挑战（60 分钟）
构建代码助手 Agent（生成、解释、运行、审查代码）。

### 练习 5：综合（90 分钟）
构建研究助手 Agent（搜索、总结、生成报告）。

---

## 附录：LangChain Agent API 速查

```python
# ReAct Agent
from langchain.agents import create_react_agent, AgentExecutor
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = executor.invoke({"input": "北京天气怎么样？"})

# OpenAI Tools Agent
from langchain.agents import create_openai_tools_agent
agent = create_openai_tools_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

---

> **明天预告：** Day 12 - RAG 检索增强生成，让 Agent 能够从文档中检索信息。
