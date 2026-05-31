# Day 13 - LangChain 综合实战

> 目标：把前面学到的 LLM、Prompt、Memory、Tools、Agent 和输出解析整合成一个完整、可运行、可讲解的 AI 助手项目。  
> 这一版的核心主题已经从旧的文档问答主题改成了“输出解析”，也就是把自然语言整理成结构化 JSON。

---

## 1. Day 13 的定位

Day 13 是一个综合实战日，它不是再讲一个孤立概念，而是把前面几天的能力串起来：

- Day 8：LLM 调用基础
- Day 9：Memory 对话记忆
- Day 10：Tools 工具调用
- Day 11：Agent 自主决策
- Day 12：输出解析与结构化输出

如果说前面的内容是“单点练习”，那么 Day 13 就是“把多个能力拼成一个完整应用”。

这份项目的最终形态可以理解为一个命令行版 AI 助手，它支持：

- 普通聊天
- 工具调用
- 输出解析
- 查看历史
- 手动切换模式
- 自动判断问题应该交给哪种能力处理

---

## 2. 本日学习目标

完成 Day 13 之后，你应该能理解并掌握：

1. 一个完整 AI 助手项目通常怎么分层。
2. Memory、Tools、输出解析、Agent 各自负责什么。
3. 为什么要把不同功能拆成不同模块。
4. 怎么让 Agent 在不同模式之间切换。
5. 怎么把自然语言整理成结构化 JSON。
6. 怎么通过命令行界面把这些能力串起来。

---

## 3. 项目整体说明

这个 Day 13 项目是一个“综合 AI 助手”：

- 用户可以直接和它聊天。
- 用户可以让它计算、查天气、查知识、查时间。
- 用户可以让它把一段话整理成 JSON。
- 用户可以查看历史对话。
- 用户可以切换不同工作模式。

从结构上看，它不是一个“只有一个功能的小脚本”，而是一个真正的“分层项目”。

---

## 4. 目录结构总览

```text
day13/
├── README.md
├── main.py
├── config.py
├── requirements.txt
├── documents/
├── modules/
│   ├── __init__.py
│   ├── agent.py
│   ├── memory.py
│   ├── output_parser.py
│   └── tools.py
├── 01_project_architecture.py
├── 02_tools_module.py
├── 03_memory_module.py
├── 04_output_parser_module.py
├── 05_agent_module.py
├── 06_chat_interface.py
├── exercise1_add_tool.py
├── exercise2_agent_modes.py
├── exercise3_persist_memory.py
├── exercise4_web_search.py
└── exercise5_full_app.py
```

下面我会按文件逐个解释。

---

## 5. 核心文件详细说明

### 5.1 `main.py`

文件路径：
- [day13/main.py](/D:/vscode项目/学习/day13/main.py)

#### 作用

`main.py` 是整个项目的统一入口。你运行：

```bash
python main.py
```

本质上就是启动 `06_chat_interface.py`。

#### 为什么要单独有这个文件

这样做的好处是：

1. 用户只需要记住一个入口。
2. 真正的交互逻辑可以单独放在界面文件中。
3. 后续如果想改成 Web、桌面应用或者别的启动方式，入口可以很容易替换。

#### 你可以把它理解成什么

它就像“总开关”：

- 不负责业务逻辑
- 不负责模型推理
- 不负责工具调用
- 只负责把项目启动起来

---

### 5.2 `config.py`

文件路径：
- [day13/config.py](/D:/vscode项目/学习/day13/config.py)

#### 作用

这个文件负责统一管理配置项，例如：

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `MODEL_NAME`
- `EMBEDDING_MODEL`

#### 为什么要单独放

因为配置通常会变：

- 你可能会换模型
- 你可能会换接口地址
- 你可能会换环境变量

如果把配置直接写死在代码里，会很难维护。

#### 学习重点

你要理解的是：  
**配置和业务逻辑分离** 是做项目的基本原则。

---

### 5.3 `requirements.txt`

文件路径：
- [day13/requirements.txt](/D:/vscode项目/学习/day13/requirements.txt)

#### 作用

这个文件记录项目依赖。安装时只需要：

```bash
pip install -r requirements.txt
```

#### 为什么重要

这样可以保证：

- 别人能复现你的环境
- 你自己换电脑后也能快速恢复项目
- 项目依赖更清晰

---

### 5.4 `documents/`

文件路径：
- [day13/documents/](/D:/vscode项目/学习/day13/documents)

#### 作用

这个目录存放示例文档或参考资料。  
在当前版本里，它更多是作为项目素材目录存在。

#### 学习意义

你可以把它理解成“示例数据区”：

- 有些项目会把文档、文本、样例数据放在这里
- 后续如果继续扩展，还可以放更多用于演示的内容

---

### 5.5 `modules/tools.py`

文件路径：
- [day13/modules/tools.py](/D:/vscode项目/学习/day13/modules/tools.py)

#### 作用

这个文件定义了 Agent 可以调用的工具。

当前包含这些工具：

- `calculator`
- `get_weather`
- `search_knowledge`
- `get_current_time`
- `unit_convert`

#### 每个工具的意义

`calculator`
- 负责数学计算
- 适合处理算术、幂运算、三角函数等

`get_weather`
- 负责返回一个城市的天气示例
- 适合演示“工具调用”怎么工作

`search_knowledge`
- 从一个简易知识库里检索信息
- 这里已经把知识点改成了输出解析、结构化输出、JSON 相关内容

`get_current_time`
- 返回当前时间
- 是最简单的实用工具之一

`unit_convert`
- 进行单位换算
- 演示参数传递和工具返回值处理

#### 为什么工具要单独放在一个模块里

因为工具本质上就是“Agent 能调用的外部能力”。

把工具和 Agent 分开有两个好处：

1. 工具可以单独测试。
2. 以后添加新工具时，不需要重写整个 Agent。

---

### 5.6 `modules/memory.py`

文件路径：
- [day13/modules/memory.py](/D:/vscode项目/学习/day13/modules/memory.py)

#### 作用

Memory 模块负责保存对话历史。

它通常保存：

- 系统提示词
- 用户输入
- 助手回复

#### 为什么它很重要

如果没有 Memory，模型每次对话都会像“失忆”一样，只看当前这一句。  
有了 Memory 以后，系统才能：

- 记住上下文
- 继承前文
- 做多轮对话

#### 在 Day 13 里的位置

Memory 是整套系统的“上下文底座”。  
不管是聊天、工具调用，还是输出解析，都会依赖它保存对话历史。

---

### 5.7 `modules/output_parser.py`

文件路径：
- [day13/modules/output_parser.py](/D:/vscode项目/学习/day13/modules/output_parser.py)

#### 作用

这是 Day 13 的新重点模块。  
它负责把自然语言整理成结构化结果。

你可以把它理解为：

- 先读懂用户的话
- 再提取关键信息
- 最后整理成 JSON

#### 主要功能

- 解析原始输入
- 判断意图分类
- 提取关键词
- 提取实体
- 判断是否需要工具
- 输出建议动作
- 给出置信度

#### 为什么需要输出解析

很多时候，模型不是只要“回答一句话”就够了，而是要把内容整理成机器更容易处理的格式，例如：

- JSON
- 表格
- 字段列表
- 标准化摘要

这就是输出解析的价值。

#### 这个模块的设计思路

1. 如果 LLM 可用，就尝试让模型直接输出 JSON。
2. 如果模型输出不规范，就尝试提取 JSON 片段。
3. 如果还是失败，就使用规则兜底。

这样设计的好处是：

- 更稳
- 更容易调试
- 更适合学习“结构化输出”这个概念

---

### 5.8 `modules/agent.py`

文件路径：
- [day13/modules/agent.py](/D:/vscode项目/学习/day13/modules/agent.py)

#### 作用

这是一个兼容包装文件。

它的作用很简单：

- 让其他文件可以通过 `from modules.agent import SmartAgent` 进行导入
- 实际的 `SmartAgent` 仍然来自 `05_agent_module.py`

#### 为什么要这样做

因为项目里主实现文件名带数字前缀，直接按模块名导入不方便。  
这个包装文件就是为了让导入路径更稳定、更清晰。

---

### 5.9 `modules/__init__.py`

文件路径：
- [day13/modules/__init__.py](/D:/vscode项目/学习/day13/modules/__init__.py)

#### 作用

这个文件用于把 `modules` 目录识别为包。  
在 Python 中，包结构会让导入更规范。

#### 你可以怎么理解

它本身通常不做复杂业务，只是让下面这些模块可以被更方便地引用：

- `memory`
- `tools`
- `output_parser`

---

### 5.10 `05_agent_module.py`

文件路径：
- [day13/05_agent_module.py](/D:/vscode项目/学习/day13/05_agent_module.py)

#### 作用

这是整个项目里最核心的文件之一。  
它负责把多个能力整合起来：

- 普通对话
- 工具调用
- 输出解析
- 自动模式判断

#### 它做了什么

`SmartAgent` 会维护三种模式：

- `chat`
- `tool`
- `parse`

然后根据用户输入或手动切换，决定走哪条逻辑。

#### 你应该重点理解什么

Agent 不是“直接回答问题”这么简单。  
Agent 的本质是：

1. 先判断当前任务是什么
2. 再决定要不要调用工具
3. 再决定要不要输出结构化结果
4. 最后再组织成用户能看懂的回答

#### 为什么这一层很重要

因为它把前面的能力真正串起来了。  
没有 Agent，工具、记忆、输出解析都只是“散落的能力”；  
有了 Agent，它们才变成一个完整的应用。

---

### 5.11 `06_chat_interface.py`

文件路径：
- [day13/06_chat_interface.py](/D:/vscode项目/学习/day13/06_chat_interface.py)

#### 作用

这是用户真正接触到的界面层。

它负责：

- 显示欢迎信息
- 显示菜单
- 接收命令
- 调用 Agent
- 展示结果

#### 为什么界面层要单独分离

因为界面层的职责和 Agent 不一样：

- 界面层负责“怎么跟用户说话”
- Agent 负责“怎么做决策和执行”

把两者分开，代码会更清晰，也更容易修改。

#### 你可以把它看成什么

它就像命令行版的前台接待：

- 用户问什么
- 先看用户想干什么
- 再把请求交给对应能力
- 最后把结果返回给用户

---

## 6. 练习文件详细说明

### 6.1 `01_project_architecture.py`

文件路径：
- [day13/01_project_architecture.py](/D:/vscode项目/学习/day13/01_project_architecture.py)

#### 作用

这个文件用于讲解整个项目架构。

你运行它时，会看到：

- 项目分层图
- 模块职责表
- 知识回顾映射
- 数据流向说明

#### 学习价值

它的目的不是跑功能，而是帮助你“看懂整个项目”。

---

### 6.2 `02_tools_module.py`

文件路径：
- [day13/02_tools_module.py](/D:/vscode项目/学习/day13/02_tools_module.py)

#### 作用

这个文件帮助你理解工具模块在项目中的意义。

它会强调：

- 什么是工具
- 为什么工具要拆成独立模块
- 为什么当前版本把知识库示例改成了输出解析相关内容

---

### 6.3 `03_memory_module.py`

文件路径：
- [day13/03_memory_module.py](/D:/vscode项目/学习/day13/03_memory_module.py)

#### 作用

这个文件用来理解 Memory 模块。

它帮助你看到：

- 历史消息怎么保存
- 系统提示词怎么插入
- 对话上下文怎么构建

---

### 6.4 `04_output_parser_module.py`

文件路径：
- [day13/04_output_parser_module.py](/D:/vscode项目/学习/day13/04_output_parser_module.py)

#### 作用

这个文件是输出解析主题的演示脚本。

它会演示：

- 如何把用户输入整理成 JSON
- 如何从文本中提取关键词和实体
- 如何得到一个结构化的输出结果

#### 为什么要有这个文件

因为 Day 13 不只是“把模块写出来”，还要“让你能单独运行、单独理解”。

---

### 6.5 `05_agent_module.py`

这个文件上面已经详细说明过了。  
在练习层面，你要重点观察它是如何把：

- Memory
- Tools
- Output Parser
- LLM

组合成一个完整智能体的。

---

### 6.6 `exercise1_add_tool.py`

这个文件帮助你练习如何新增一个工具。

你可以通过它理解：

- 工具是怎么定义的
- 工具是怎么注册到 Agent 的
- Agent 如何调用工具

---

### 6.7 `exercise2_agent_modes.py`

文件路径：
- [day13/exercise2_agent_modes.py](/D:/vscode项目/学习/day13/exercise2_agent_modes.py)

#### 作用

这个文件帮助你对比 Agent 的不同模式：

- chat：普通对话
- tool：工具调用
- parse：输出解析

#### 学习重点

你要通过这个文件理解：

1. 什么样的问题适合聊天。
2. 什么样的问题适合调用工具。
3. 什么样的问题适合做结构化整理。

---

### 6.8 `exercise3_persist_memory.py`

这个文件主要用于练习对话记忆和历史保存。

你可以通过它理解：

- 历史消息如何保存
- 为什么 Memory 会影响后续回答
- 如何查看记忆内容

---

### 6.9 `exercise4_web_search.py`

这个文件主要用于练习搜索类能力。

它可以帮助你理解：

- 当问题需要外部信息时怎么处理
- Agent 怎么配合工具查找信息

---

### 6.10 `exercise5_full_app.py`

这个文件一般用于把前面的能力整合成一个更完整的小应用。

它通常是一个“收官练习”：

- 把工具、记忆、输出解析和 Agent 都串起来
- 让你更接近真实项目的结构

---

## 7. 输出解析这一版的核心学习点

Day 13 当前的重点不是旧的文档问答主题，而是输出解析。  
你要重点理解这些概念：

### 7.1 为什么要做输出解析

因为很多实际场景里，用户需要的不是一段自然语言，而是：

- JSON
- 表格
- 字段结构
- 分类结果
- 摘要

### 7.2 输出解析和普通聊天的区别

普通聊天：
- 目标是自然交流

输出解析：
- 目标是把内容变成结构化数据

### 7.3 输出解析的常见用途

- 信息抽取
- 需求整理
- 意图识别
- 文本分类
- 生成可供程序继续处理的数据

### 7.4 为什么它适合放在 Day 13

因为 Day 13 本来就是综合实战。  
把输出解析放进 Agent 里，可以让你看到“一个真实助手”是怎么同时处理多种任务的。

---

## 8. 推荐运行顺序

建议你按这个顺序看：

1. 先看 `01_project_architecture.py`
2. 再看 `02_tools_module.py`
3. 再看 `03_memory_module.py`
4. 再看 `04_output_parser_module.py`
5. 再看 `05_agent_module.py`
6. 最后看 `06_chat_interface.py`
7. 之后直接运行 `main.py`

这样你会先建立整体概念，再去看细节，会更容易理解。

---

## 9. 如何运行

安装依赖：

```bash
pip install -r requirements.txt
```

启动项目：

```bash
python main.py
```

如果你想单独测试某个文件，也可以直接运行对应的练习脚本。

---

## 10. 常见问题

### 10.1 为什么我直接运行某些模块时会出现导入问题？

因为有些脚本默认是从项目根目录启动的。  
如果你从别的目录直接运行，Python 可能找不到 `modules` 或 `config`。

### 10.2 为什么输出解析有时候不是严格 JSON？

因为模型输出天然会有波动。  
所以代码里通常需要：

- 提示模型只输出 JSON
- 尝试解析 JSON
- 失败后做兜底修复

### 10.3 为什么要保留工具和记忆？

因为一个完整助手通常不只是“会聊天”，还要能：

- 记住上下文
- 处理外部任务
- 输出可结构化内容

---

## 11. 学习建议

1. 先把架构图看懂。
2. 再看工具、记忆和输出解析各自的职责。
3. 试着自己改一个工具。
4. 试着给输出解析模块加一个新字段。
5. 试着让 Agent 自动判断 mode。

---

## 12. 小结

Day 13 的核心不是单一功能，而是“整合”。

这一次你会看到：

- LLM 是大脑
- Memory 是记忆
- Tools 是执行器
- Output Parser 是结构化整理器
- Agent 是决策中心
- Interface 是用户入口

如果你把 Day 13 理解透了，后面继续扩展更复杂的 AI 应用会容易很多。
