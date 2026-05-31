# Day 12 - 输出解析项目说明

> 目标：让模型输出从“能看懂的自然语言”升级成“程序能直接使用的结构化数据”。
>
> 这一节的重点不是让模型说得更多，而是让模型说得更规范、更稳定、更容易解析。

---

## 1. Day 12 在整条学习路线里的位置

Day 12 的主题是 **输出解析**。

它在整条 AI Agent 学习路线里非常关键，因为后面的很多能力都依赖它：

- Tool Calling 需要结构化参数
- Agent 需要稳定识别模型意图
- RAG 需要把答案和引用整理成固定格式
- 工单系统、表单系统、信息抽取系统都需要结构化输出

你可以把 Day 12 理解成一句话：

> 从“让模型回答问题”，进阶到“让模型按固定格式输出结果”。

---

## 2. 这一天到底要学什么

完成 Day 12 后，你应该能理解并掌握下面这些内容：

1. 什么是结构化输出。
2. 什么是 JSON 输出。
3. 为什么自然语言不适合直接交给程序处理。
4. 什么是 Output Parser。
5. 什么是 schema。
6. 如何验证字段是否完整。
7. 如何处理 JSON 格式错误。
8. 如何在解析失败时重试。

如果你把这些内容学透了，后面的工具调用、Agent、信息抽取都会顺很多。

---

## 3. 本项目的整体思路

这个 Day 12 项目分成 4 层：

1. **schema 层**
2. **解析层**
3. **校验层**
4. **演示层**

它们的关系是：

```text
用户输入
  ↓
选择 schema
  ↓
生成提示词
  ↓
模拟模型输出 JSON
  ↓
解析 JSON
  ↓
校验字段
  ↓
如果失败则重试
  ↓
输出最终结果
```

---

## 4. 项目目录总览

```text
day12/
├── README.md
├── config.py
├── requirements.txt
├── .env.example
├── main.py
├── 01_basic_json.py
├── 02_field_extraction.py
├── 03_retry_parse.py
├── 04_multi_field_output.py
├── 05_full_demo.py
├── modules/
│   ├── __init__.py
│   ├── demo_workflow.py
│   └── mock_model.py
├── parsers/
│   ├── __init__.py
│   └── json_parser.py
├── schemas/
│   ├── __init__.py
│   └── output_schema.py
└── tools/
    ├── __init__.py
    └── response_validator.py
```

下面我会按文件逐个解释。

---

## 5. 每一个文件的详细说明

### 5.1 `config.py`

文件路径：

- [day12/config.py](/D:/vscode项目/学习/day12/config.py)

#### 这个文件是做什么的

`config.py` 负责读取配置参数，例如：

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `MODEL_NAME`
- `MAX_RETRY`

在这个 Day 12 项目里，模型部分我们主要用了模拟模型，所以即使你暂时不填 API，也能先把流程跑起来。

#### 这个文件里的内容

- 从 `.env` 读取环境变量
- 定义默认配置
- 统一管理后续模块会用到的参数

#### 为什么要单独放一个配置文件

这样做的好处是：

- 配置和代码分离
- 改模型参数时不用改业务代码
- 后续接真实 API 时更方便

#### 你在这个文件里应该关注什么

- `MAX_RETRY` 决定解析失败时最多重试几次
- `MODEL_NAME` 是后面如果接真实模型时会用到的名字

---

### 5.2 `requirements.txt`

文件路径：

- [day12/requirements.txt](/D:/vscode项目/学习/day12/requirements.txt)

#### 这个文件是做什么的

它记录项目需要安装的依赖。

#### 当前包含哪些依赖

- `python-dotenv`
- `rich`

#### 为什么这里依赖不多

因为 Day 12 主要是讲“输出解析”的思想，不是重点讲大模型接入。
所以这里先保持一个轻量、易跑的版本。

---

### 5.3 `.env.example`

文件路径：

- [day12/.env.example](/D:/vscode项目/学习/day12/.env.example)

#### 这个文件是做什么的

它是环境变量示例文件，告诉你 `.env` 应该怎么写。

#### 文件里展示的内容

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `MODEL_NAME`
- `MAX_RETRY`

#### 为什么要有这个文件

因为真实项目里，密钥和配置通常不直接写进代码。

这样做的好处：

- 更安全
- 更清晰
- 更容易切换环境

---

### 5.4 `main.py`

文件路径：

- [day12/main.py](/D:/vscode项目/学习/day12/main.py)

#### 这个文件是做什么的

它是 Day 12 的主入口。

你运行：

```bash
python day12/main.py
```

就会启动一个命令行交互界面。

#### 这个文件的主要职责

- 展示欢迎信息
- 展示命令菜单
- 接收用户输入
- 调用 `StructuredOutputWorkflow`
- 把结果以中文打印出来

#### 这个文件里有哪些核心部分

#### `OutputParseApp`

这是命令行应用类，负责整个交互流程。

#### `show_banner()`

显示顶部欢迎信息，告诉用户这个项目支持哪些命令。

#### `show_menu()`

把可用命令整理成表格显示出来。

#### `_render_result()`

把工作流返回的字典转成更好读的中文输出。

#### `run_demo()`

一次性跑几个示例，方便观察“意图识别 / 信息抽取 / 简历抽取”的效果。

#### `run()`

主循环，负责不断读取用户输入并执行对应任务。

#### 为什么这个文件重要

因为它是你和整个项目交互的入口。

如果你只想快速看效果，就运行它。

---

### 5.5 `modules/__init__.py`

文件路径：

- [day12/modules/__init__.py](/D:/vscode项目/学习/day12/modules/__init__.py)

#### 这个文件是做什么的

它负责把 `modules` 目录里的核心类导出来，方便别的文件直接引用。

#### 当前导出了什么

- `StructuredOutputWorkflow`
- `MockStructuredModel`

#### 为什么要有它

这样别的文件可以更简洁地导入模块，而不用记住很长的内部路径。

---

### 5.6 `modules/mock_model.py`

文件路径：

- [day12/modules/mock_model.py](/D:/vscode项目/学习/day12/modules/mock_model.py)

#### 这个文件是做什么的

它是一个“模拟模型”。

Day 12 这里没有强依赖真实 API，而是用一个假的模型来模拟结构化输出流程，这样你可以：

- 不联网也能跑
- 不用担心 API 配置问题
- 更专注理解“解析”和“校验”

#### 这个文件的核心职责

1. 根据不同 schema 生成不同结构的数据。
2. 随机加入一些格式噪声。
3. 模拟真实模型有时会“说多余的话”的情况。

#### 主要函数解释

#### `__init__()`

初始化随机数种子，保证结果更稳定。

#### `_extract_keywords()`

从文本中抽取关键词，用来模拟抽取类任务。

#### `_classification_payload()`

模拟“意图识别”场景，返回：

- `intent`
- `confidence`
- `entities`
- `need_tool`

#### `_extraction_payload()`

模拟信息抽取任务，返回：

- `title`
- `summary`
- `keywords`
- `category`

#### `_resume_payload()`

模拟简历抽取任务，返回：

- `name`
- `education`
- `skills`
- `experience_years`

#### `generate()`

这是最重要的方法。

它会根据 schema 选择不同的 payload，然后返回 JSON 字符串。

如果 `strict=True`，它就尽量只返回标准 JSON。

如果 `strict=False`，它会故意加一点多余文字或代码块标记，模拟真实模型输出不完全标准的情况。

#### 这个文件在整个项目里的作用

它是 Day 12 的“假模型”。

你可以把它理解成：

> 专门用来练习解析和修复流程的测试用输出源。

---

### 5.7 `modules/demo_workflow.py`

文件路径：

- [day12/modules/demo_workflow.py](/D:/vscode项目/学习/day12/modules/demo_workflow.py)

#### 这个文件是做什么的

它负责把整条结构化输出链路串起来。

换句话说，它是 Day 12 的“总调度器”。

#### 它做的事情

1. 选择 schema
2. 生成提示词
3. 调用模拟模型
4. 解析 JSON
5. 校验字段
6. 如果失败就重试

#### 主要函数解释

#### `__init__()`

初始化模拟模型、JSON 解析器和重试次数。

#### `_pick_schema()`

根据任务名选择不同 schema。

例如：

- `intent` -> 意图识别 schema
- `extract` -> 信息抽取 schema
- `resume` -> 简历抽取 schema

#### `run()`

这是整个工作流最核心的方法。

它会：

- 先让模型输出
- 再尝试解析
- 再做字段校验
- 失败后继续重试

最终返回一个完整的结果字典。

#### `_build_prompt()`

构建初始提示词，告诉模型：

- 你是谁
- 要输出什么格式
- 输入文本是什么

#### `_build_retry_prompt()`

构建重试提示词。

如果前一次输出有问题，它会告诉模型：

- 哪个地方错了
- 这次要严格按 schema 输出

#### 这个文件在整个项目里的作用

它是 Day 12 的“核心流程控制器”。

如果你想理解整个项目怎么跑，最应该先看它。

---

### 5.8 `parsers/__init__.py`

文件路径：

- [day12/parsers/__init__.py](/D:/vscode项目/学习/day12/parsers/__init__.py)

#### 这个文件是做什么的

它把解析器模块导出来，方便统一引用。

#### 当前导出的内容

- `JsonOutputParser`

---

### 5.9 `parsers/json_parser.py`

文件路径：

- [day12/parsers/json_parser.py](/D:/vscode项目/学习/day12/parsers/json_parser.py)

#### 这个文件是做什么的

它负责把模型输出解析成真正的 Python 字典。

这是 Day 12 里非常核心的一步。

#### 为什么需要这个文件

因为模型输出不一定永远是标准 JSON。

它可能会出现：

- 多余解释文字
- ```json 代码块包裹
- 结尾多了逗号
- 格式不完整

这个解析器就是为了尽量把这些情况修回来。

#### 主要结构解释

#### `ParseResult`

统一表示一次解析结果。

字段包括：

- `ok`
- `data`
- `error`
- `raw`

#### `JsonOutputParser`

这是解析器主类。

#### `extract_json_block()`

尝试从整段文本中截取 `{ ... }` 部分。

#### `try_repair()`

对常见格式错误做轻量修复。

例如：

- 去掉代码块标记
- 去掉多余逗号
- 去掉包裹文字

#### `parse()`

这个方法是真正的入口。

它会依次尝试：

1. 原文直接解析
2. 提取 JSON 后解析
3. 修复后再解析

如果三次都失败，就返回失败结果。

#### 这个文件的作用

它负责把“看起来像 JSON 的文本”变成“程序能使用的字典”。

---

### 5.10 `schemas/__init__.py`

文件路径：

- [day12/schemas/__init__.py](/D:/vscode项目/学习/day12/schemas/__init__.py)

#### 这个文件是做什么的

它把 schema 定义导出来，方便别的文件直接用。

#### 当前导出的内容

- `OutputSchema`
- `SchemaField`

---

### 5.11 `schemas/output_schema.py`

文件路径：

- [day12/schemas/output_schema.py](/D:/vscode项目/学习/day12/schemas/output_schema.py)

#### 这个文件是做什么的

它负责定义“模型应该输出什么样的数据结构”。

这就是 Day 12 里的 schema。

#### 核心概念解释

#### `SchemaField`

表示一个字段。

字段里会定义：

- 名字
- 类型
- 是否必填
- 说明
- 默认值

#### `OutputSchema`

表示一整套输出规则。

里面会包含：

- schema 名称
- schema 描述
- 字段列表

#### `to_prompt_block()`

这个方法会把 schema 变成提示词文本。

这样模型就能知道：

- 要输出哪些字段
- 每个字段的类型是什么
- 哪些字段是必须的

#### `build_intent_schema()`

构建“意图识别” schema。

字段包括：

- `intent`
- `confidence`
- `entities`
- `need_tool`

#### `build_extraction_schema()`

构建“信息抽取” schema。

字段包括：

- `title`
- `summary`
- `keywords`
- `category`

#### `build_resume_schema()`

构建“简历抽取” schema。

字段包括：

- `name`
- `education`
- `skills`
- `experience_years`

#### 这个文件的重要性

它是“模型输出格式的标准定义”。

没有它，模型不知道应该输出什么结构。

---

### 5.12 `tools/__init__.py`

文件路径：

- [day12/tools/__init__.py](/D:/vscode项目/学习/day12/tools/__init__.py)

#### 这个文件是做什么的

它把校验工具导出来，方便别的模块直接调用。

#### 当前导出的内容

- `validate_payload`
- `ValidationResult`

---

### 5.13 `tools/response_validator.py`

文件路径：

- [day12/tools/response_validator.py](/D:/vscode项目/学习/day12/tools/response_validator.py)

#### 这个文件是做什么的

它负责校验模型解析后的结果是否符合 schema。

即使 JSON 能成功解析，也不代表内容一定正确。

例如：

- 字段缺失
- 字段类型不对
- 数组里不是字符串

这些都要校验。

#### 主要结构解释

#### `ValidationResult`

统一表示校验结果。

字段包括：

- `ok`
- `errors`

#### `_type_matches()`

检查值的类型是否符合 schema 要求。

例如：

- `string` 对应 Python 的 `str`
- `number` 对应 `int` 或 `float`
- `boolean` 对应 `bool`
- `array[string]` 对应字符串列表

#### `validate_payload()`

根据 schema 检查 payload。

它会检查：

- 必填字段是否缺失
- 字段类型是否正确

如果有问题，就返回错误列表。

#### 这个文件的重要性

它是结构化输出流程里的“质量控制器”。

---

### 5.14 `01_basic_json.py`

文件路径：

- [day12/01_basic_json.py](/D:/vscode项目/学习/day12/01_basic_json.py)

#### 这个文件是做什么的

这是练习 1，演示最基础的 JSON 输出。

#### 你运行它会看到什么

它会调用工作流，把一段英文文本做结构化抽取，然后打印完整结果。

#### 这个练习想让你理解什么

- JSON 输出长什么样
- 结构化输出最基本的形态是什么

---

### 5.15 `02_field_extraction.py`

文件路径：

- [day12/02_field_extraction.py](/D:/vscode项目/学习/day12/02_field_extraction.py)

#### 这个文件是做什么的

这是练习 2，演示字段抽取。

#### 你运行它会看到什么

它会让工作流从简历文本里抽取：

- 姓名
- 学历
- 技能
- 工作年限

#### 这个练习想让你理解什么

结构化输出不只是“分类”，也可以做“字段提取”。

---

### 5.16 `03_retry_parse.py`

文件路径：

- [day12/03_retry_parse.py](/D:/vscode项目/学习/day12/03_retry_parse.py)

#### 这个文件是做什么的

这是练习 3，演示重试解析。

#### 你运行它会看到什么

它会让工作流处理一个意图识别任务，并在解析失败时自动重试。

#### 这个练习想让你理解什么

- 解析失败是正常情况
- 失败后要有修复和重试机制

---

### 5.17 `04_multi_field_output.py`

文件路径：

- [day12/04_multi_field_output.py](/D:/vscode项目/学习/day12/04_multi_field_output.py)

#### 这个文件是做什么的

这是练习 4，演示多字段输出。

#### 你运行它会看到什么

它会处理一段文本，并输出：

- 标题
- 摘要
- 关键词
- 分类

#### 这个练习想让你理解什么

一个模型输出可以同时包含多个字段，而不是只给一句话。

---

### 5.18 `05_full_demo.py`

文件路径：

- [day12/05_full_demo.py](/D:/vscode项目/学习/day12/05_full_demo.py)

#### 这个文件是做什么的

这是练习 5，完整演示。

#### 你运行它会看到什么

它会依次测试：

- 意图识别
- 信息抽取
- 简历抽取

#### 这个练习想让你理解什么

它是在验证整个 Day 12 链路是不是都通了。

---

## 6. Day 12 的完整工作流

这个项目的运行流程可以理解成下面这样：

```text
用户输入文本
  ↓
选择 schema
  ↓
生成提示词
  ↓
模拟模型输出 JSON
  ↓
JSON 解析器尝试解析
  ↓
如果格式不对，做轻量修复
  ↓
字段校验器检查字段
  ↓
如果仍然失败，工作流重试
  ↓
返回最终结果
```

你可以把它看成三道关卡：

1. 格式关
2. 结构关
3. 语义关

---

## 7. 为什么这个项目用模拟模型

这里没有强依赖真实 API，原因是：

1. 让你先理解结构化输出的核心思想。
2. 让项目可以离线运行。
3. 让你看到“模型输出不标准”时，解析器和校验器怎么工作。

这比一开始就接真实模型更适合学习。

---

## 8. 怎么运行这个项目

### 8.1 安装依赖

```bash
pip install -r day12/requirements.txt
```

### 8.2 运行主程序

```bash
python day12/main.py
```

### 8.3 运行练习脚本

```bash
python day12/01_basic_json.py
python day12/02_field_extraction.py
python day12/03_retry_parse.py
python day12/04_multi_field_output.py
python day12/05_full_demo.py
```

### 8.4 单独运行模块调试

你现在也可以直接运行：

```bash
python day12/modules/mock_model.py
python day12/modules/demo_workflow.py
```

因为我已经把这两个文件的导入路径问题修好了。

---

## 9. 常见问题

### 9.1 为什么有时输出不是标准 JSON

因为模拟模型会故意加入一点噪声，模拟真实模型不完全规范的情况。

### 9.2 为什么要做字段校验

因为 JSON 合法不等于内容正确。

### 9.3 为什么要重试

因为模型第一次输出不一定完全符合要求，重试可以提高稳定性。

### 9.4 为什么有些文件需要 `sys.path` 处理

因为你有时候会直接运行某个子模块，这时 Python 默认不会自动把项目根目录当作导入路径。

---

## 10. 你应该重点理解的几个地方

### 10.1 schema

schema 是“输出格式标准”。

### 10.2 parser

parser 是“把文本变成结构化对象”的工具。

### 10.3 validator

validator 是“检查结构是否符合要求”的工具。

### 10.4 workflow

workflow 是“把整个流程串起来”的调度层。

---

## 11. Day 12 的学习重点总结

如果你只记一句话，那就是：

> 让模型输出固定格式，并把它稳定地解析成程序可以使用的数据。

这就是 Day 12 的核心价值。

---

## 12. 最后总结

Day 12 虽然看起来不像一个很大的项目，但它非常重要。

因为后面你会反复用到这些能力：

- 工具调用前的参数抽取
- Agent 的结构化思考
- RAG 结果整理
- 自动化业务流程

如果说 Day 10 和 Day 11 是“会让模型做事”，那 Day 12 就是“让模型做事时输出规范结果”。

这一步非常关键。

