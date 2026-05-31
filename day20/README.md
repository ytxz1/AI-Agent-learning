# Day 20 - Coding Agent

> 目标：理解一个 Coding Agent 是怎样“读代码、出计划、生成草案、给验证建议”的。  
> 这一节不只是聊天，也不只是工具调用，而是把“看代码”和“改代码”串成一个完整的工作流。

---

## 1. Day 20 的定位

Day 20 是第三周里非常关键的一个项目日，主题是 **Coding Agent**。

在前面的学习里，你已经有了：

- LLM 基础
- Memory
- Tools
- Agent
- 输出解析
- 文档加载
- 切分
- 检索链

Day 20 要做的，是把这些能力往“真实开发协作”推进一步。

一个 Coding Agent 不应该只是“回答你问题”，而应该能：

1. 读懂需求。
2. 扫描工作区。
3. 找到可能受影响的文件。
4. 生成修改计划。
5. 生成代码草案。
6. 给出验证建议。
7. 让用户先审阅，再决定是否真正落盘。

---

## 2. 本日学习目标

完成 Day 20 后，你应该能够：

1. 说清楚 Coding Agent 和普通聊天助手的区别。
2. 理解为什么 Coding Agent 需要工作区扫描能力。
3. 理解为什么要先生成计划，再生成代码草案。
4. 知道怎样把“需求”拆成“可执行步骤”。
5. 知道怎么把“代码修改建议”结构化成 JSON。
6. 知道如何设计更安全的代码修改流程。

---

## 3. 项目整体说明

这个 Day 20 项目是一个教学版 Coding Agent。

它的核心不是“自动替你大规模改整个项目”，而是：

- 先扫描当前工作区
- 再分析需求
- 再生成结构化修改计划
- 再生成代码草案
- 再给验证建议

项目同时支持：

- 在线模型优先
- 没有 API Key 时本地兜底
- 命令行交互
- 文件预览
- 计划生成
- 代码草案生成
- 草案保存到 `output/`

---

## 4. 目录结构总览

```text
day20/
├── README.md
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── documents/
│   ├── 01_coding_agent_overview.txt
│   ├── 02_safety_rules.md
│   └── 03_prompt_guidelines.txt
├── modules/
│   ├── __init__.py
│   ├── workspace.py
│   ├── planner.py
│   ├── coder.py
│   └── coding_agent.py
├── 01_scan_workspace.py
├── 02_build_plan.py
├── 03_generate_change_set.py
├── 04_file_inspect.py
└── 05_full_coding_agent.py
```

下面我按文件详细解释。

---

## 5. 核心文件详细说明

### 5.1 `main.py`

文件路径：
- [day20/main.py](/D:/vscode项目/学习/day20/main.py)

#### 作用

这是整个项目的统一入口。

你运行：

```bash
python main.py
```

实际上会启动 `05_full_coding_agent.py` 的交互界面。

#### 为什么单独保留入口

这样做的好处是：

- 用户只需要记住一个启动方式
- 以后如果想换成 Web 或 GUI，入口可以单独替换
- 主逻辑仍然保留在模块里，结构更清晰

---

### 5.2 `config.py`

文件路径：
- [day20/config.py](/D:/vscode项目/学习/day20/config.py)

#### 作用

这里集中管理 Coding Agent 所需的配置。

包括：

- 工作区目录
- API Key
- 模型名称
- 温度
- 文件预览长度
- 默认展示数量

#### 为什么它重要

Coding Agent 本身会涉及很多“调参”：

- 模型选择
- 提示词长度
- 文件预览条数
- 预览字数

这些都适合放在配置文件里，而不是散落在代码中。

---

### 5.3 `requirements.txt`

文件路径：
- [day20/requirements.txt](/D:/vscode项目/学习/day20/requirements.txt)

#### 作用

记录项目依赖。

安装方式：

```bash
pip install -r requirements.txt
```

#### 依赖说明

- `python-dotenv`：读取环境变量
- `rich`：美化 CLI 输出
- `langchain-openai`：在线模型调用
- `langchain-core`：消息、提示词等基础能力

---

### 5.4 `.env.example`

文件路径：
- [day20/.env.example](/D:/vscode项目/学习/day20/.env.example)

#### 作用

提供默认配置样例。

你可以直接复制成 `.env` 再填写真实值。

#### 包含哪些参数

- `WORKSPACE_DIR`
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `PLAN_MODEL`
- `CODE_MODEL`
- `TEMPERATURE`
- `MAX_FILES_PREVIEW`
- `MAX_FILE_PREVIEW_CHARS`
- `DEFAULT_TOP_N`

#### 为什么要有 API Key

因为 Day 20 的核心是“生成计划”和“生成代码草案”。  
这些步骤更适合让在线模型来做，因此 API 是这节课里最有价值的能力之一。

---

### 5.5 `documents/`

文件路径：
- [day20/documents/](/D:/vscode项目/学习/day20/documents)

#### 作用

这里放的是关于 Coding Agent 的教学材料。

包括：

- `01_coding_agent_overview.txt`
- `02_safety_rules.md`
- `03_prompt_guidelines.txt`

#### 这些文档有什么用

它们帮助你理解：

- Coding Agent 的目标是什么
- 为什么要加安全规则
- 怎样给 Agent 下更清楚的指令

---

### 5.6 `modules/workspace.py`

文件路径：
- [day20/modules/workspace.py](/D:/vscode项目/学习/day20/modules/workspace.py)

#### 作用

这个模块负责和工作区打交道。

它主要做：

- 安全定位路径
- 扫描文件树
- 读取文件内容
- 生成文件预览
- 统计工作区信息

#### 为什么它很重要

Coding Agent 如果看不懂工作区结构，就没法知道该改哪些文件。

所以“先扫描工作区”是第一步。

#### 你应该重点关注什么

- `resolve_path`
- `list_files`
- `tree_lines`
- `read_text`
- `file_preview`
- `stats`

这些函数就是“Agent 的眼睛”。

---

### 5.7 `modules/planner.py`

文件路径：
- [day20/modules/planner.py](/D:/vscode项目/学习/day20/modules/planner.py)

#### 作用

这个模块负责把自然语言需求转换成结构化计划。

也就是：

**用户说一句话 -> Agent 输出一份计划**

#### 计划里通常有什么

- `objective`：目标
- `mode`：当前处理模式
- `assumptions`：假设前提
- `steps`：修改步骤
- `validation`：验证方式
- `risks`：风险提醒

#### 为什么要先做计划

因为代码修改最怕“直接冲进去改”。

先出计划可以：

- 明确思路
- 确认范围
- 减少误改
- 让用户先审阅

#### 在线和本地的区别

如果配置了 `OPENAI_API_KEY`：

- `planner.py` 会优先调用在线模型生成计划

如果没有：

- 就使用本地规则生成一个保守但可读的计划

---

### 5.8 `modules/coder.py`

文件路径：
- [day20/modules/coder.py](/D:/vscode项目/学习/day20/modules/coder.py)

#### 作用

这个模块负责把计划转成“代码草案”。

它不是直接改文件，而是输出一个结构化 `change set`，方便审阅。

#### change set 通常包含什么

- `objective`
- `mode`
- `summary`
- `files`
- `tests`
- `notes`

其中 `files` 里会记录：

- 要改哪个文件
- 动作是 `create` / `update` / `delete` / `review`
- 为什么要这么改
- 草案内容是什么

#### 为什么不直接改文件

因为 Coding Agent 最重要的一点是“可控”。

先输出草案，让人看一遍，会更安全。

---

### 5.9 `modules/coding_agent.py`

文件路径：
- [day20/modules/coding_agent.py](/D:/vscode项目/学习/day20/modules/coding_agent.py)

#### 作用

这是整个项目的中枢。

它把以下几件事串起来：

- 扫描工作区
- 查看文件
- 生成计划
- 生成草案
- 缓存最后一次结果

#### 为什么它是核心

因为它是“Agent 真正干活的地方”。

其他模块负责具体能力，而这个模块负责把这些能力组合起来。

---

### 5.10 `modules/__init__.py`

文件路径：
- [day20/modules/__init__.py](/D:/vscode项目/学习/day20/modules/__init__.py)

#### 作用

统一导出常用类，让别的模块导入更方便。

---

## 6. 练习文件详细说明

### 6.1 `01_scan_workspace.py`

文件路径：
- [day20/01_scan_workspace.py](/D:/vscode项目/学习/day20/01_scan_workspace.py)

#### 作用

练习工作区扫描。

你会看到：

- 工作区摘要
- 文件数量
- 总大小
- 简化目录树

#### 学习重点

先了解“Agent 要操作的环境长什么样”。

---

### 6.2 `02_build_plan.py`

文件路径：
- [day20/02_build_plan.py](/D:/vscode项目/学习/day20/02_build_plan.py)

#### 作用

练习生成修改计划。

它会根据一个 Coding 需求，输出结构化计划 JSON。

#### 学习重点

让你看到需求如何被拆成步骤。

---

### 6.3 `03_generate_change_set.py`

文件路径：
- [day20/03_generate_change_set.py](/D:/vscode项目/学习/day20/03_generate_change_set.py)

#### 作用

练习生成代码草案。

它会基于计划和代码上下文，输出 file-level 的变更建议。

#### 学习重点

理解“计划”和“真正的代码草案”不是一回事。

---

### 6.4 `04_file_inspect.py`

文件路径：
- [day20/04_file_inspect.py](/D:/vscode项目/学习/day20/04_file_inspect.py)

#### 作用

练习查看文件内容。

这是 Coding Agent 最基础也最重要的能力之一。

---

### 6.5 `05_full_coding_agent.py`

文件路径：
- [day20/05_full_coding_agent.py](/D:/vscode项目/学习/day20/05_full_coding_agent.py)

#### 作用

这是 Day 20 的完整交互式应用。

它支持：

- 扫描工作区
- 查看文件预览
- 查看指定文件
- 生成计划
- 生成代码草案
- 执行示例请求
- 保存最近一次结果

#### 为什么这个文件重要

它把前面的所有模块真正连起来了。

你可以把它当成一个“教学版 Coding Agent 前台”。

---

## 7. Day 20 的核心知识点

### 7.1 什么是 Coding Agent

Coding Agent 是一种能帮助你理解、规划、生成和验证代码改动的智能体。

它不是简单聊天，而是“面向开发任务”的智能体。

### 7.2 为什么先计划，再生成代码

因为直接生成代码容易：

- 改动过大
- 忽略依赖
- 漏掉验证

先计划可以让整个过程更安全、更可审阅。

### 7.3 为什么要扫描工作区

因为 Coding Agent 不能凭空知道你的项目结构。

它必须先看：

- 有哪些文件
- 文件大概内容是什么
- 哪些文件更可能被影响

### 7.4 为什么要生成 change set

因为真正的工程实践中，最好先审查修改方案，再落地修改。

change set 就是“可审阅的代码修改草案”。

### 7.5 在线模型的作用

如果配置了 API Key，在线模型可以帮助：

- 更准确地理解需求
- 更像人一样拆解任务
- 生成更自然的代码草案

所以 Day 20 这一节特别适合使用 API。

---

## 8. 推荐运行顺序

建议按下面顺序学：

1. `01_scan_workspace.py`
2. `04_file_inspect.py`
3. `02_build_plan.py`
4. `03_generate_change_set.py`
5. `05_full_coding_agent.py`

这样你会先了解环境，再了解计划，最后了解草案。

---

## 9. 如何运行

安装依赖：

```bash
pip install -r requirements.txt
```

启动主程序：

```bash
python main.py
```

或者单独运行练习脚本：

```bash
python 01_scan_workspace.py
python 05_full_coding_agent.py
```

---

## 10. 常见问题

### 10.1 如果没有 API Key，可以运行吗？

可以。

项目里已经做了本地兜底：

- 计划会用规则生成
- 草案也会用保守模板生成

但如果你想体验更强的 Coding Agent 效果，建议配置 API。

### 10.2 为什么不直接修改真实文件？

因为这是教学版项目。

先生成草案更安全，也更适合学习流程。

### 10.3 为什么要限制工作区范围？

因为 Coding Agent 不能随便去改工作区外的文件。

这是安全边界。

---

## 11. 学习建议

1. 先搞清楚工作区扫描。
2. 再学怎么输出计划。
3. 再学怎么输出草案。
4. 多改几个请求试试不同的 plan。
5. 如果配置了 API Key，观察在线和本地模式的区别。

---

## 12. 小结

Day 20 是从“会回答问题”走向“会协助开发”的一步。

你要记住：

- 工作区扫描是基础
- 计划生成是中间层
- 代码草案是结果层
- 安全审阅是工程实践的关键

如果你把 Day 20 理解透了，后面做真正的 Coding Agent 会容易很多。

