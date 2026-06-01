# Day 20 - 项目 3：Coding Agent

> Day 20 的任务：理解并实现一个教学版 Coding Agent。
>
> 这一节的重点不是让 Agent 直接大规模改文件，而是学习一个更安全、更工程化的流程：
>
> ```text
> 需求 -> 扫描工作区 -> 查看文件 -> 生成计划 -> 生成代码草案 -> 保存结果 -> 人工审阅
> ```

---

## 1. 今天你要学会什么

Day 20 对应学习计划表里的任务是：`项目 3：Coding Agent`。

完成这一天后，你应该能理解：

1. Coding Agent 和普通聊天助手有什么区别。
2. 为什么 Coding Agent 要先扫描工作区。
3. 为什么不能一上来就直接修改文件。
4. 如何把自然语言需求拆成结构化计划。
5. 如何把计划转成可审阅的代码草案。
6. 什么是 change set。
7. 为什么要限制文件读取在工作区内。
8. 在线模型和本地兜底分别做什么。
9. 如何保存最近一次计划和草案。
10. 一个安全的 Coding Agent 工作流应该长什么样。

---

## 2. 项目结构

```text
day20/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── main.py
├── 01_scan_workspace.py
├── 02_build_plan.py
├── 03_generate_change_set.py
├── 04_file_inspect.py
├── 05_full_coding_agent.py
├── documents/
│   ├── 01_coding_agent_overview.txt
│   ├── 02_safety_rules.md
│   └── 03_prompt_guidelines.txt
└── modules/
    ├── __init__.py
    ├── workspace.py
    ├── planner.py
    ├── coder.py
    └── coding_agent.py
```

Day 20 的核心链路是：

```text
workspace.py
  -> planner.py
  -> coder.py
  -> coding_agent.py
  -> 05_full_coding_agent.py
```

---

## 3. 运行方式

### 3.1 安装依赖

在 `day20` 文件夹下运行：

```powershell
pip install -r requirements.txt
```

### 3.2 配置环境变量

复制 `.env.example` 为 `.env`：

```powershell
copy .env.example .env
```

可配置内容：

```env
WORKSPACE_DIR=.
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.deepseek.com
PLAN_MODEL=deepseek-chat
CODE_MODEL=deepseek-chat
TEMPERATURE=0.2
MAX_FILES_PREVIEW=5
MAX_FILE_PREVIEW_CHARS=220
DEFAULT_TOP_N=5
```

Day 20 有 API Key 时效果更好。

如果没有 API Key，也可以运行，因为项目提供本地兜底计划和本地草案。

### 3.3 运行完整应用

```powershell
python main.py
```

进入程序后可以输入：

```text
scan
files
inspect
plan
draft
demo
save
q
```

### 3.4 分步骤运行练习脚本

```powershell
python 01_scan_workspace.py
python 04_file_inspect.py
python 02_build_plan.py
python 03_generate_change_set.py
python 05_full_coding_agent.py
```

建议第一次学习时按这个顺序运行。

---

## 4. Coding Agent 核心原理

### 4.1 什么是 Coding Agent

Coding Agent 是面向开发任务的智能体。

它不只是回答问题，还要能：

1. 理解需求。
2. 查看项目结构。
3. 读取相关文件。
4. 生成修改计划。
5. 生成代码草案。
6. 给出测试建议。
7. 让用户审阅后再决定是否落地。

### 4.2 为什么要先扫描工作区

如果 Agent 不知道项目结构，就很容易乱猜。

扫描工作区可以让 Agent 知道：

1. 有哪些代码文件。
2. 哪些文件可能是入口。
3. 项目有没有 README。
4. 配置文件在哪里。
5. 需要优先关注哪些文件。

### 4.3 为什么要先计划，再写代码

直接生成代码有风险。

常见问题：

1. 改错文件。
2. 改动范围过大。
3. 漏掉验证步骤。
4. 破坏已有功能。

先生成计划可以让修改过程更可控。

### 4.4 什么是 change set

change set 是结构化代码修改草案。

它通常包含：

```text
objective
mode
summary
files
tests
notes
```

其中 `files` 会说明：

1. 要处理哪个文件。
2. 动作是 create / update / delete / review。
3. 为什么要改。
4. 草案内容是什么。

---

## 5. 每个文件的详细解释

### 5.1 `config.py`

这个文件是 Day 20 的配置中心。

主要配置：

1. `WORKSPACE_DIR`：Coding Agent 要扫描的工作区。
2. `OPENAI_API_KEY`：在线模型 API Key。
3. `OPENAI_BASE_URL`：OpenAI 兼容接口地址。
4. `PLAN_MODEL`：生成计划用的模型。
5. `CODE_MODEL`：生成代码草案用的模型。
6. `TEMPERATURE`：模型随机性。
7. `MAX_FILES_PREVIEW`：最多预览几个文件。
8. `MAX_FILE_PREVIEW_CHARS`：每个文件最多预览多少字符。
9. `DEFAULT_TOP_N`：默认展示数量。

为什么要限制预览？

因为 Coding Agent 不能把整个项目一次性塞给模型。

需要先给模型一个合理的摘要。

---

### 5.2 `modules/workspace.py`

这个文件负责工作区操作。

核心结构：

```python
WorkspaceFile
```

保存：

1. 文件路径。
2. 文件大小。
3. 文件预览。

核心类：

```python
WorkspaceInspector
```

常用方法：

1. `resolve_path()`：把相对路径转换成安全绝对路径。
2. `list_files()`：列出常见代码和文档文件。
3. `tree_lines()`：生成简化目录树。
4. `read_text()`：读取文件文本。
5. `file_preview()`：生成单文件预览。
6. `stats()`：统计工作区信息。
7. `summarize_files()`：生成多文件预览。

最重要的安全点：

```text
读取文件前必须确认路径没有逃出工作区。
```

---

### 5.3 `modules/planner.py`

这个文件负责生成修改计划。

核心类：

```python
CodingPlanner
```

它有两种模式：

1. 在线模式：调用模型生成结构化计划。
2. 本地模式：根据关键词生成保守计划。

计划通常包含：

```text
objective
mode
assumptions
steps
validation
risks
workspace_summary
```

为什么计划要是 JSON？

因为结构化输出更方便：

1. 展示。
2. 保存。
3. 后续生成代码草案。
4. 自动化处理。

---

### 5.4 `modules/coder.py`

这个文件负责生成代码草案。

核心类：

```python
ChangeSetBuilder
```

它会根据：

1. 用户需求。
2. 修改计划。
3. 工作区文件预览。
4. 重点文件列表。

生成一个 change set。

注意：

```text
它不会直接修改真实文件。
```

这正是教学版 Coding Agent 的安全设计。

---

### 5.5 `modules/coding_agent.py`

这是整个项目的中枢模块。

核心类：

```python
CodingAgent
```

它组合了：

1. `WorkspaceInspector`
2. `CodingPlanner`
3. `ChangeSetBuilder`

常用方法：

1. `workspace_summary()`
2. `inspect()`
3. `scan_tree()`
4. `generate_plan()`
5. `generate_change_set()`
6. `pretty_json()`

你可以把它理解成：

```text
workspace 是眼睛
planner 是大脑里的计划器
coder 是草案生成器
CodingAgent 是调度中心
```

---

### 5.6 `01_scan_workspace.py`

这是练习 1 文件。

作用：

```text
扫描工作区，查看项目结构和文件摘要。
```

重点理解：

```python
agent.workspace_summary()
agent.scan_tree()
```

---

### 5.7 `02_build_plan.py`

这是练习 2 文件。

作用：

```text
根据一个需求生成结构化修改计划。
```

示例需求：

```text
给这个项目增加一个 help 命令，并保留现有菜单结构
```

重点理解：

```python
agent.generate_plan(...)
```

---

### 5.8 `03_generate_change_set.py`

这是练习 3 文件。

作用：

```text
根据需求和计划生成代码草案。
```

重点理解：

```python
agent.generate_change_set(...)
```

它只生成草案，不直接改文件。

---

### 5.9 `04_file_inspect.py`

这是练习 4 文件。

作用：

```text
安全查看指定文件内容。
```

重点理解：

```python
agent.inspect("main.py")
```

---

### 5.10 `05_full_coding_agent.py`

这是完整交互应用。

支持命令：

```text
scan
files
inspect
plan
draft
demo
save
q
```

其中：

`plan` 生成计划。

`draft` 生成代码草案。

`save` 把最近一次计划和草案保存到 `output/`。

---

## 6. 练习题专区

下面是 Day 20 的完整练习题。

以后每天的 README 都会按这个格式写：

```text
练习题编号
  -> 练习目标
  -> 题目要求
  -> 操作提示
  -> 参考答案
  -> 如何运行
  -> 你应该观察什么结果
```

---

### 6.1 练习 1：扫描工作区

文件：

```text
01_scan_workspace.py
```

练习目标：

理解 Coding Agent 如何获得项目结构。

题目要求：

1. 创建 `CodingAgent`。
2. 调用 `workspace_summary()`。
3. 调用 `scan_tree()`。
4. 打印 JSON 摘要和目录树。

参考答案：

答案已经写在 `01_scan_workspace.py` 中。

如何运行：

```powershell
python 01_scan_workspace.py
```

你应该观察到：

1. 工作区根目录。
2. 文件数量。
3. 总大小。
4. 部分文件预览。
5. 简化目录树。

---

### 6.2 练习 2：生成修改计划

文件：

```text
02_build_plan.py
```

练习目标：

理解自然语言需求如何变成结构化计划。

题目要求：

1. 创建 `CodingAgent`。
2. 输入一个功能需求。
3. 指定重点文件。
4. 输出 JSON 计划。

参考答案：

答案已经写在 `02_build_plan.py` 中。

如何运行：

```powershell
python 02_build_plan.py
```

你应该观察到：

1. `objective` 表示目标。
2. `steps` 表示拆解步骤。
3. `validation` 表示验证建议。
4. `risks` 表示风险提醒。

---

### 6.3 练习 3：生成代码草案

文件：

```text
03_generate_change_set.py
```

练习目标：

理解计划如何进一步变成可审阅的代码草案。

题目要求：

1. 创建 `CodingAgent`。
2. 输入同一个功能需求。
3. 调用 `generate_change_set()`。
4. 输出 change set JSON。

参考答案：

答案已经写在 `03_generate_change_set.py` 中。

如何运行：

```powershell
python 03_generate_change_set.py
```

你应该观察到：

1. `summary` 总结草案。
2. `files` 说明文件级改动建议。
3. `tests` 给出验证建议。
4. 本地模式不会直接修改文件。

---

### 6.4 练习 4：查看文件

文件：

```text
04_file_inspect.py
```

练习目标：

理解 Coding Agent 如何安全读取工作区内文件。

题目要求：

1. 创建 `CodingAgent`。
2. 调用 `inspect("main.py")`。
3. 输出文件路径、大小和预览。

参考答案：

答案已经写在 `04_file_inspect.py` 中。

如何运行：

```powershell
python 04_file_inspect.py
```

你应该观察到：

1. 文件绝对路径。
2. 文件大小。
3. 文件前若干字符预览。

---

### 6.5 练习 5：完整 Coding Agent 应用

文件：

```text
05_full_coding_agent.py
```

练习目标：

体验完整 Coding Agent 工作流。

题目要求：

1. 启动应用。
2. 输入 `scan`。
3. 输入 `files`。
4. 输入 `inspect`。
5. 输入 `plan`。
6. 输入 `draft`。
7. 输入 `save`。
8. 输入 `q`。

操作提示：

建议命令顺序：

```text
scan
files
inspect
plan
draft
save
q
```

参考答案：

答案已经写在 `05_full_coding_agent.py` 中。

如何运行：

```powershell
python 05_full_coding_agent.py
```

或：

```powershell
python main.py
```

你应该观察到：

1. 菜单正常显示。
2. 可以扫描工作区。
3. 可以查看文件。
4. 可以生成计划。
5. 可以生成代码草案。
6. `save` 后会生成 `output/last_plan.json` 和 `output/last_change_set.json`。

---

## 7. 练习题对应文件答案说明

Day 20 的练习答案已经写进对应代码文件中。

对应关系：

```text
练习 1 -> 01_scan_workspace.py
练习 2 -> 02_build_plan.py
练习 3 -> 03_generate_change_set.py
练习 4 -> 04_file_inspect.py
练习 5 -> 05_full_coding_agent.py
```

这些文件都是完整可运行的参考答案。

---

## 8. API Key 与本地模式说明

Day 20 支持两种模式。

### 8.1 没有 API Key

如果没有配置 `OPENAI_API_KEY`：

1. 工作区扫描正常。
2. 文件查看正常。
3. 计划生成使用本地规则。
4. 代码草案使用本地模板。
5. 不会产生 API 费用。

### 8.2 有 API Key

如果配置了 `OPENAI_API_KEY`：

1. `CodingPlanner` 会尝试调用在线模型生成计划。
2. `ChangeSetBuilder` 会尝试调用在线模型生成代码草案。
3. 输出通常更贴合需求。
4. 如果在线调用失败，会自动回退本地模式。

---

## 9. 常见问题

### 9.1 为什么不直接修改文件

因为 Day 20 是教学版 Coding Agent。

先输出计划和草案更安全。

真正修改文件前，你应该先审阅：

1. 目标文件是否正确。
2. 计划是否合理。
3. 草案是否会破坏现有逻辑。
4. 验证步骤是否完整。

---

### 9.2 为什么要限制工作区路径

因为 Coding Agent 不能随便读取或修改工作区外文件。

`resolve_path()` 会检查目标路径是否仍在工作区内。

这是安全边界。

---

### 9.3 为什么在线模型输出有时不是 JSON

模型有时会输出解释文字或 Markdown 代码块。

所以 `planner.py` 和 `coder.py` 都写了 `_extract_json()`：

1. 先尝试解析纯 JSON。
2. 再尝试解析 ```json 代码块。
3. 最后尝试从文本中截取 JSON 主体。

---

## 10. 推荐学习顺序

建议按这个顺序学习：

1. 读 `README.md`。
2. 运行 `python 01_scan_workspace.py`。
3. 打开 `modules/workspace.py`。
4. 运行 `python 04_file_inspect.py`。
5. 运行 `python 02_build_plan.py`。
6. 打开 `modules/planner.py`。
7. 运行 `python 03_generate_change_set.py`。
8. 打开 `modules/coder.py`。
9. 打开 `modules/coding_agent.py`。
10. 运行 `python main.py`。

---

## 11. Day 20 总结

Day 20 的关键词是：

```text
Coding Agent
workspace
inspect
plan
change set
draft
validation
safety
local fallback
online model
```

一句话总结：

```text
Coding Agent 的核心不是“立刻改代码”，而是先看清楚、想清楚、写出可审阅草案，再决定是否落地。
```

如果你把 Day 20 学明白了，就已经开始接近真实 AI 编程助手的工作方式了。
