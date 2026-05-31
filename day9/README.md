# Day 9 - Memory 记忆：让 AI 拥有对话记忆能力

> **学习目标**：掌握 LangChain 的 Memory 系统，让 AI 能够记住对话历史，实现真正的多轮对话。
> **预计阅读时间**：15-20 分钟

---

## 目录

1. [什么是 Memory](#1)
2. [没有 Memory vs 有 Memory](#2)
3. [Memory 的工作原理](#3)
4. [ConversationBufferMemory](#4)
5. [ConversationSummaryMemory](#5)
6. [ConversationBufferWindowMemory](#6)
7. [三种记忆类型对比](#7)
8. [CombinedMemory](#8)
9. [自定义 Memory](#9)
10. [Memory 持久化](#10)
11. [Memory + Chain](#11)
12. [综合实践项目](#12)
13. [最佳实践](#13)
14. [常见问题](#14)
15. [知识总结](#15)
16. [练习题](#16)

---

## 1. 什么是 Memory

### 1.1 一句话解释

**Memory 就是 AI 的"记事本"**——让 AI 能记住你之前说过的话。

### 1.2 生活中的类比

想象你和朋友聊天：

```
没有记忆的朋友：
┌─────────────────────────────────────────┐
│  你: 我叫小明                            │
│  朋友: 你好小明！                         │
│  （过了10分钟）                           │
│  你: 我叫什么？                           │
│  朋友: 嗯...你是谁来着？  ← 失忆了！      │
└─────────────────────────────────────────┘

有记忆的朋友：
┌─────────────────────────────────────────┐
│  你: 我叫小明                            │
│  朋友: 你好小明！                         │
│  （过了10分钟）                           │
│  你: 我叫什么？                           │
│  朋友: 你叫小明啊！  ← 记得清清楚楚       │
└─────────────────────────────────────────┘
```

### 1.3 技术角度的理解

LLM本身是**无状态的**——每次调用都是一张白纸。

```
LLM 的工作方式：
第1次调用: [用户说: 你好] → AI生成回复 → 连接断开
第2次调用: [用户说: 我叫什么] → AI完全不知道之前说过什么
就像每次打电话都换一个人接！
```

**Memory 的作用**就是在本地保存对话历史，让每次调用 LLM 时都能带上之前的对话。

---

## 2. 没有 Memory vs 有 Memory

### 2.1 对比图

```
═══════════════════════════════════════
          没有 Memory 的情况
═══════════════════════════════════════
用户输入          LLM              回复
"我叫小明"  →  [无上下文]  →  "你好小明！"
  ↓                                ↓
（记忆为空）                    （没有保存）
"我叫什么？"→  [无上下文]  →  "我不知道..."
  ↓                                ↓
（还是空的）                   （完全失忆）

═══════════════════════════════════════
          有 Memory 的情况
═══════════════════════════════════════
用户输入          LLM              回复
"我叫小明"  →  [无上下文]  →  "你好小明！"
  ↓              ↑                  ↓
（保存到Memory）（读取Memory）   （保存到Memory）
Memory: [用户:我叫小明, AI:你好小明！]
"我叫什么？"→[带上Memory]→"你叫小明啊！"
  ↓              ↑                  ↓
（更新Memory）（读取Memory）   （更新Memory）
```

### 2.2 代码对比

```python
# 没有 Memory（Day 8 的写法）
chain = prompt | llm | parser
result1 = chain.invoke({"input": "我叫小明"})
result2 = chain.invoke({"input": "我叫什么"})  # AI 不知道！

# 有 Memory（Day 9 的写法）
memory = ConversationBufferMemory(return_messages=True)
history = memory.load_memory_variables({})["chat_history"]
result1 = chain.invoke({"chat_history": history, "input": "我叫小明"})
memory.chat_memory.add_user_message("我叫小明")
memory.chat_memory.add_ai_message(result1)
history = memory.load_memory_variables({})["chat_history"]
result2 = chain.invoke({"chat_history": history, "input": "我叫什么"})
# AI: 你叫小明啊！
```

---

## 3. Memory 的工作原理

### 3.1 一轮对话的完整流程

```
Step 1: 用户说话
┌─────────────┐
│  用户输入    │  "你还记得我叫什么吗？"
└──────┬──────┘
       ▼
Step 2: 从 Memory 加载对话历史
┌───────────────────────────────────────┐
│  Memory:                              │
│  msg1: "你好，我叫小明"                │
│  msg2: "你好小明！"                    │
│  msg3: "我在学Python"                  │
│  msg4: "Python很棒！"                  │
│  load_memory_variables({})            │
│       ↓                               │
│  返回: [msg1, msg2, msg3, msg4]       │
└───────────────────┬───────────────────┘
                    ▼
Step 3: 构建完整提示词
┌───────────────────────────────────────┐
│  系统: "你是一个助手"                   │
│  ──────────────────                    │
│  用户(历史): "你好，我叫小明" ←Memory   │
│  AI(历史): "你好小明！"     ←Memory     │
│  用户(历史): "我在学Python"  ←Memory    │
│  AI(历史): "Python很棒！"   ←Memory     │
│  ──────────────────                    │
│  用户(当前): "你还记得我叫什么吗？"      │
└───────────────────┬───────────────────┘
                    ▼
Step 4: LLM 生成回复
┌───────────────────────────────────────┐
│  "你叫小明啊！你之前告诉过我的。"       │
└───────────────────┬───────────────────┘
                    ▼
Step 5: 保存到 Memory
┌───────────────────────────────────────┐
│  Memory 更新：                        │
│  msg1~msg4: (之前的内容)              │
│  msg5: "你还记得我叫什么吗？" ←新增    │
│  msg6: "你叫小明啊！"         ←新增    │
└───────────────────────────────────────┘
```

### 3.2 MessagesPlaceholder 的作用

```
普通变量 {input}:
  填入: "你好"  →  一条 HumanMessage

MessagesPlaceholder {chat_history}:
  填入: [msg1, msg2, msg3]  →  展开成 3 条消息！
```

---

## 4. ConversationBufferMemory 完整记忆

> 对应文件：`01_conversation_buffer.py`

### 4.1 什么是 BufferMemory

**ConversationBufferMemory** = 完整的笔记本，每句话都逐字记下来。

```
你说: "我叫小明"     → 记录: [我叫小明]
你说: "我在学Python" → 记录: [我叫小明, 我在学Python]
你说: "我住北京"     → 记录: [我叫小明, 我在学Python, 我住北京]
所有内容都完整保留，一个字都不丢！
```

### 4.2 优缺点

```
┌─────────────────────┬───────────────────────┐
│      优点           │        缺点            │
├─────────────────────┼───────────────────────┤
│ 信息100%完整保留    │ Token消耗随对话增长    │
│ 不需要额外API调用   │ 长对话会超出上下文限制  │
│ 实现简单            │ 占用内存大             │
│ 完全精确            │                       │
└─────────────────────┴───────────────────────┘
```

### 4.3 Token 消耗增长

```
Token数
  ^
  │                              ╱ BufferMemory
30K│                          ╱   (线性增长)
  │                       ╱
20K│                   ╱
  │               ╱
10K│           ╱
  │       ╱
  │   ╱
  │╱
  └───────────────────────────→ 对话轮数
  0    50   100   150   200   300
  超过模型上下文窗口（如64K）就会报错！
```

---

## 5. ConversationSummaryMemory 摘要记忆

> 对应文件：`02_conversation_summary.py`

### 5.1 什么是 SummaryMemory

**ConversationSummaryMemory** = 会总结的笔记本，不逐字记录，而是概括。

```
你说: "我叫小明"  → 摘要: "用户说他叫小明。"
你说: "我是程序员" → 摘要: "用户叫小明，是程序员。"
你说: "在学Python" → 摘要: "用户叫小明，是程序员，学Python。"
每轮对话后摘要更新，但长度增长很慢！
```

### 5.2 优缺点

```
┌─────────────────────┬───────────────────────┐
│      优点           │        缺点            │
├─────────────────────┼───────────────────────┤
│ Token消耗基本恒定   │ 可能丢失对话细节       │
│ 理论上能记无限对话   │ 每次更新要额外调LLM    │
│ 适合长对话          │ 无法精确引用原话        │
└─────────────────────┴───────────────────────┘
```

---

## 6. ConversationBufferWindowMemory 窗口记忆

> 对应文件：`03_conversation_window.py`

### 6.1 什么是 WindowMemory

**ConversationBufferWindowMemory** = 只有K页的笔记本，写满就擦掉最早的。

```
WindowMemory (k=3):
第1轮: [msg1]
第2轮: [msg1, msg2]
第3轮: [msg1, msg2, msg3]
第4轮: [msg2, msg3, msg4]     ← msg1 被擦掉
第5轮: [msg3, msg4, msg5]     ← msg2 被擦掉
第6轮: [msg4, msg5, msg6]     ← msg3 被擦掉
始终保持最近 3 轮！
```

### 6.2 k 值选择

```
k值    │ 保留轮数 │ 适用场景
───────┼─────────┼─────────────────
k=1    │ 1轮     │ 简单问答
k=3    │ 3轮     │ 简单聊天机器人
k=5    │ 5轮     │ 大多数场景（推荐）
k=10   │ 10轮    │ 需要较多上下文
k=20   │ 20轮    │ 专业领域对话
```

---

## 7. 三种记忆类型对比

### 7.1 一张图看懂

```
BufferMemory（完整记忆）:
📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝
   所有消息都保留，越来越多...

SummaryMemory（摘要记忆）:
📝 → 📝 → 📝 → 📝 → 📝 → 📝 → 📝 → 📝
   每次压缩，始终只有一段摘要

WindowMemory（窗口记忆 k=5）:
[📝📝📝📝📝] → [📝📝📝📝📝] → [📝📝📝📝📝]
   始终只保留最近5条
```

### 7.2 详细对比表

| 特性 | BufferMemory | SummaryMemory | WindowMemory |
|------|-------------|---------------|-------------|
| 保存策略 | 全部保存 | 压缩为摘要 | 只保留最近K轮 |
| 信息完整度 | 100% | ~70-80% | 最近K轮100% |
| Token消耗 | 线性增长 | 基本恒定 | 恒定 |
| 额外API调用 | 无 | 每次更新1次 | 无 |
| 额外费用 | 无 | 有 | 无 |
| 响应延迟 | 无 | 有（等摘要） | 无 |
| 最大容量 | 受上下文限制 | 理论无限 | 受K值限制 |
| 适合场景 | 短对话 | 长对话 | 中等对话 |

### 7.3 如何选择

```
对话通常有多少轮？
    │
    ├── < 20 轮  → BufferMemory
    ├── 20~100轮 → WindowMemory(k=10)
    └── > 100轮  → SummaryMemory
```

---

## 8. CombinedMemory 组合记忆

> 对应文件：`04_custom_memory.py`

同时使用多种记忆，取长补短：

```
短期记忆 (WindowMemory k=5):
  → 让 AI 知道"刚才聊了什么"
长期记忆 (SummaryMemory):
  → 让 AI 知道"整体聊过什么"
两者结合:
  → AI 既知道最近的细节，也知道整体脉络！
```

---

## 9. 自定义 Memory

### 9.1 用户画像记忆

```python
class UserProfileMemory:
    def __init__(self):
        self.profile = {}
    def update(self, key, value):
        self.profile[key] = value
    def get_string(self):
        return "\n".join(f"{k}: {v}" for k, v in self.profile.items())

mem = UserProfileMemory()
mem.update("姓名", "小明")
mem.update("职业", "程序员")
print(mem.get_string())
# 姓名: 小明
# 职业: 程序员
```

---

## 10. Memory 持久化

### 10.1 为什么需要持久化

```
没有持久化：
  程序启动 → Memory在内存中 → 程序关闭 → Memory消失 → 失忆！
有持久化：
  程序启动 → 从文件加载Memory → 程序关闭 → Memory保存在文件
  再次启动 → 重新加载Memory → 记忆恢复！
```

### 10.2 方案对比

| 方案 | 适用场景 | 复杂度 | 性能 |
|------|---------|--------|------|
| JSON文件 | 开发测试 | 低 | 中 |
| SQLite | 单机应用 | 中 | 高 |
| Redis | 生产环境 | 高 | 很高 |

---

## 11. Memory + Chain 完整流程

### 11.1 标准代码模板（必背）

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser

# 1. 创建组件
llm = ChatOpenAI(model="deepseek-chat")
memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")

# 2. 提示词（必须包含 MessagesPlaceholder！）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个助手"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

# 3. 创建 Chain
chain = prompt | llm | StrOutputParser()

# 4. 对话循环
while True:
    user_input = input("你: ")
    history = memory.load_memory_variables({})["chat_history"]
    result = chain.invoke({"chat_history": history, "input": user_input})
    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(result)
    print(f"AI: {result}")
```

### 11.2 常见错误

```
错误1: 忘记 MessagesPlaceholder → 记忆无法注入
错误2: memory_key 和 variable_name 不一致 → 找不到记忆
错误3: 忘记保存对话 → 下次调用记忆不更新
错误4: load_memory_variables 传了参数 → 应该传 {}
```

---

## 12. 综合实践项目

> 对应文件：`main.py`

### 12.1 项目功能

```
┌────────────────────────────────────────┐
│       Day 9 智能记忆助手                │
├────────────────────────────────────────┤
│  1    完整记忆   所有对话保留            │
│  2    窗口记忆   保留最近5轮             │
│  3    摘要记忆   压缩为摘要              │
│  4    查看记忆   显示对话历史            │
│  5    清空记忆   重置历史                │
│  6    查看统计   对话轮数等              │
│  q    退出                               │
│  直接输入内容 → 和 AI 聊天              │
└────────────────────────────────────────┘
```

---

## 13. 最佳实践

```
1. 选择合适的记忆类型
   - 短对话(<10轮) → BufferMemory
   - 长对话(>10轮) → SummaryMemory 或 WindowMemory
2. 设置合理的 memory_key
   - 统一用 "chat_history"
   - 和 MessagesPlaceholder 变量名一致
3. 注意 token 预算
   - 每条消息约 50~200 tokens
   - 预留空间给系统提示词和用户输入
4. 定期清理
   - 长时间运行要定期 clear()
   - 或用 WindowMemory 自动限制
5. 持久化存储
   - 生产环境用 Redis / 数据库
   - 开发环境用文件存储
```

---

## 14. 常见问题

### Q1: 报错 KeyError: chat_history

提示词缺少 MessagesPlaceholder，或名称不匹配。

### Q2: AI 还是"失忆"

检查是否每次对话后都调用了 add_user_message / add_ai_message。

### Q3: Token 超出限制

用 WindowMemory 或 SummaryMemory 限制历史长度。

---

## 15. 知识总结

### 15.1 学习路线

```
Day 8: LangChain入门
          │
          ▼
Day 9: Memory记忆
  → BufferMemory (完整记忆)
  → SummaryMemory (摘要记忆)
  → WindowMemory (窗口记忆)
  → CombinedMemory (组合记忆)
  → 自定义Memory + 持久化
          │
          ▼
Day 10: Tools工具 → Agent
```

### 15.2 文件清单

```
day9/
├── config.py                    # 配置文件
├── main.py                      # 综合实践
├── 01_conversation_buffer.py    # BufferMemory 示例
├── 02_conversation_summary.py   # SummaryMemory 示例
├── 03_conversation_window.py    # WindowMemory 示例
├── 04_custom_memory.py          # 自定义Memory
├── 05_memory_chatbot.py         # 带记忆的聊天机器人
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 16. 练习题

### 练习 1：基础（必做）

运行 `01_conversation_buffer.py`，修改对话内容，测试 AI 能否正确回忆。

### 练习 2：中等（推荐）

修改 `05_memory_chatbot.py`，添加第四种记忆模式：**摘要+窗口组合记忆**。

### 练习 3：进阶

用 `FileMemory` 实现持久化聊天机器人。

### 练习 4：挑战

设计"学习助手"，同时使用三种记忆类型。

---

> **明天预告**：Day 10 - Tools 工具，让 AI 能够调用外部工具（计算器、天气、搜索等），为构建 Agent 做准备。