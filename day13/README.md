# Day 13 - 项目实战：综合 AI 助手

> **学习目标：** 综合运用 Day 8-12 所有知识，构建一个完整的 AI 助手应用。
>
> **预计阅读时间：** 30+ 分钟

---

## 目录

1. [项目概述](#1-项目概述)
2. [架构设计](#2-架构设计)
3. [模块说明](#3-模块说明)
4. [功能展示](#4-功能展示)
5. [运行指南](#5-运行指南)
6. [知识点回顾](#6-知识点回顾)
7. [最佳实践](#7-最佳实践)
8. [常见问题](#8-常见问题)
9. [知识总结](#9-知识总结)
10. [练习题](#10-练习题)

---

## 1. 项目概述

### 1.1 项目目标

构建一个**综合 AI 助手**，整合 5 天所学全部知识：

| Day | 主题 | 在本项目中的应用 |
|-----|------|-----------------|
| Day 8 | LangChain 入门 | 调用 LLM、使用 Prompt Template |
| Day 9 | Memory 记忆 | 管理对话历史、窗口裁剪 |
| Day 10 | Tools 工具 | 计算器、天气、搜索等工具 |
| Day 11 | Agents 代理 | ReAct 推理、工具选择 |
| Day 12 | RAG 检索增强 | 文档加载、向量检索、文档问答 |

### 1.2 项目功能

- **普通对话** -- 带记忆的智能聊天
- **工具增强** -- 计算、天气、搜索、时间、单位换算
- **文档问答** -- 基于本地文档的智能问答

---

## 2. 架构设计

### 2.1 模块架构

```
+--------------------------------------------------+
|              界面层 (06_chat_interface.py)         |
|   交互式命令行 + 功能菜单 + 模式切换                |
+------------------------+-------------------------+
                         |
+------------------------+-------------------------+
|               Agent 层 (05_agent_module.py)       |
|         ReAct 推理 + 模式分发 + 工具选择            |
+----+------------------+------------------+-------+
     |                  |                  |
+----+----+      +-----+-----+      +-----+-----+
|  Tools  |      |  Memory   |      |   RAG    |
| 工具模块 |      | 记忆模块   |      | 检索模块  |
+---------+      +-----------+      +----------+
     |                  |                  |
     v                  v                  v
  +-------+         +-------+         +--------+
  | LLM   |         | 历史   |         | 文档库  |
  | 模型   |         | 记录   |         | 向量库  |
  +-------+         +-------+         +--------+
```

### 2.2 数据流向

```
用户输入 -> 界面层 -> Agent 层
                         |
                    模式判断
                    /   |   \
                   /    |    \
            聊天模式  工具模式  文档模式
              |        |        |
              v        v        v
           Memory +  ReAct +   RAG +
            LLM     Tools     LLM
              |        |        |
              v        v        v
            回答      回答      回答
```

---

## 3. 模块说明

### 3.1 配置层 (config.py)

```python
# 加载 .env 文件，获取 API 密钥
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
```

### 3.2 工具模块 (modules/tools.py)

| 工具 | 功能 | 来源 |
|------|------|------|
| calculator | 数学计算 | Day 10 |
| get_weather | 天气查询 | Day 10 |
| search_knowledge | 知识搜索 | Day 10 |
| get_current_time | 获取时间 | Day 10 |
| unit_convert | 单位换算 | Day 10 |

### 3.3 记忆模块 (modules/memory.py)

| 功能 | 说明 | 来源 |
|------|------|------|
| 滑动窗口 | 只保留最近 N 轮对话 | Day 9 |
| 历史导出 | 格式化展示对话记录 | Day 9 |
| 自动裁剪 | 防止 Token 超限 | Day 9 |

### 3.4 RAG 模块 (modules/rag.py)

| 功能 | 说明 | 来源 |
|------|------|------|
| 文档加载 | 加载 txt 文档 | Day 12 |
| 文本分割 | RecursiveCharacterSplitter | Day 12 |
| 向量化存储 | ChromaDB | Day 12 |
| 检索问答 | 相似度搜索 + LLM 生成 | Day 12 |

### 3.5 Agent 模块 (modules/agent.py)

| 模式 | 说明 | 来源 |
|------|------|------|
| chat | 普通对话 + 记忆 | Day 9 |
| tool | ReAct 推理 + 工具选择 | Day 11 |
| rag | 文档检索 + 问答 | Day 12 |

### 3.6 界面层 (06_chat_interface.py)

| 命令 | 说明 |
|------|------|
| chat | 切换到普通对话模式 |
| tool | 切换到工具增强模式 |
| rag | 切换到文档问答模式 |
| mode | 查看当前模式 |
| history | 查看对话历史 |
| tools | 查看可用工具 |
| clear | 清空历史 |
| example | 示例问题 |
| q | 退出 |

---

## 4. 功能展示

### 4.1 普通对话模式

```
你：你好，我叫小明
你：我叫什么名字？  （测试记忆）
助手：你叫小明！  （记住了）
```

### 4.2 工具增强模式

```
你：北京天气怎么样？把气温转换成华氏度
  [工具] get_weather({"city": "北京"}) -> 25°C
  [工具] unit_convert({"value": 25, "from_unit": "摄氏度", "to_unit": "华氏度"}) -> 77°F
助手：北京今天 25°C（77°F），晴天
```

### 4.3 文档问答模式

```
你：Python 有什么特点？
  [RAG] 检索到 3 个相关文档
助手：根据文档，Python 是一种高级、解释型编程语言...
```

---

## 5. 运行指南

### 5.1 安装依赖

```bash
pip install chromadb tiktoken
```

### 5.2 运行程序

```bash
python main.py
```

### 5.3 学习路径

建议按以下顺序学习本项目的每个文件：

1. `01_project_architecture.py` -- 了解整体架构
2. `02_tools_module.py` -- 学习工具系统
3. `03_memory_module.py` -- 学习记忆管理
4. `04_rag_module.py` -- 学习文档问答
5. `05_agent_module.py` -- 学习 Agent 模式
6. `06_chat_interface.py` -- 学习界面交互
7. `main.py` -- 启动程序

---

## 6. 知识点回顾

### 6.1 Day 8-12 完整知识链

```
Day 8: LLM + Prompt + Chain
    |
Day 9: Memory（对话历史管理）
    |
Day 10: Tools（工具定义和调用）
    |
Day 11: Agents（ReAct 推理循环）
    |
Day 12: RAG（文档检索增强生成）
    |
Day 13: 项目实战（整合所有知识）
```

### 6.2 核心代码模式

```python
# Day 8: LLM 调用
llm = ChatOpenAI(model="deepseek-chat")

# Day 9: 记忆管理
memory = ConversationMemory(window_size=10)

# Day 10: 工具定义
@tool
def calculator(expression: str) -> str:
    """执行数学计算"""

# Day 11: Agent 推理
llm_with_tools = llm.bind_tools(tools)
response = llm_with_tools.invoke(messages)

# Day 12: RAG 检索
retriever = vectorstore.as_retriever()
docs = retriever.invoke(question)

# 综合集成
agent = SmartAgent()  # 整合一切
agent.tool_mode("北京天气怎么样？")
```

---

## 7. 最佳实践

1. **模块化设计** -- 功能解耦，各模块独立
2. **错误处理** -- 每个工具都要有 try/except
3. **记忆管理** -- 设置合理的 window_size
4. **Token 控制** -- 限制工具返回结果长度
5. **安全检查** -- 文件操作时路径验证
6. **用户反馈** -- 显示工具调用过程

---

## 8. 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| RAG 不可用 | 缺少 chromadb | pip install chromadb |
| 工具不调用 | 描述不清晰 | 优化 docstring |
| 记不住对话 | 窗口太小 | 增大 window_size |
| Token 超限 | 历史太长 | 减小窗口或裁剪 |
| API 错误 | 密钥问题 | 检查 .env 文件 |

---

## 9. 知识总结

### 9.1 文件清单

```
day13/
+-- config.py                    # 配置文件
+-- main.py                      # 入口
+-- 01_project_architecture.py   # 项目架构概览
+-- 02_tools_module.py           # 工具模块
+-- 03_memory_module.py          # 记忆模块
+-- 04_rag_module.py             # RAG 模块
+-- 05_agent_module.py           # Agent 模块
+-- 06_chat_interface.py         # 交互界面
+-- modules/                     # 模块包
|   +-- __init__.py
|   +-- tools.py
|   +-- memory.py
|   +-- rag.py
+-- documents/                   # 文档目录
+-- README.md
+-- exercise1_add_tool.py        # 练习1：添加工具
+-- exercise2_agent_modes.py     # 练习2：Agent 模式对比
+-- exercise3_persist_memory.py  # 练习3：持久化记忆
+-- exercise4_web_search.py      # 练习4：网络搜索
+-- exercise5_full_app.py        # 练习5：扩展应用
+-- .env / .gitignore / requirements.txt
```

### 9.2 学习成果

学完 Day 13，你应该能够：
1. 设计模块化的 AI 应用架构
2. 整合 LLM + Memory + Tools + Agent + RAG
3. 构建完整的交互式 AI 助手
4. 根据需求扩展功能

---

## 10. 练习题

### 练习 1：基础（10 分钟）
给 Agent 添加一个新工具（如获取随机数），并测试是否可用。

### 练习 2：中等（20 分钟）
对比三种模式（chat/tool/rag）在不同类型问题上的效果。

### 练习 3：进阶（30 分钟）
实现记忆的持久化保存和加载（保存到 JSON 文件）。

### 练习 4：挑战（60 分钟）
给 Agent 添加上网搜索功能（使用 requests 库搜索真实信息）。

### 练习 5：综合（90 分钟）
扩展主程序，添加更多模式（如翻译助手、代码助手）。

---

> **恭喜你完成所有课程！** 从 Day 8 到 Day 13，你学会了：
> LLM 调用 -> 记忆管理 -> 工具系统 -> Agent 代理 -> RAG 检索 -> 项目实战
