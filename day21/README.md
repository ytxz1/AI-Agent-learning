# Day 21 - 项目优化与调试

> Day 21 的任务：对前面完成的项目进行优化与调试。
>
> 这一天不是从零写新项目，而是学习真实开发中非常重要的一步：
>
> ```text
> 发现问题 -> 诊断原因 -> 提出优化 -> 验证效果 -> 沉淀报告
> ```

---

## 1. 今天你要学会什么

Day 21 对应学习计划表里的任务是：`项目优化与调试`。

完成这一天后，你应该能理解：

1. 为什么项目完成后还需要优化。
2. 如何评估 README、入口文件、配置文件和练习脚本是否完整。
3. 如何优化提示词，让模型输出更稳定。
4. 如何提高 RAG 或 Agent 项目的准确率。
5. 如何给项目规划下一步功能。
6. 如何检查命令行用户体验。
7. 如何生成完整优化报告。
8. 如何把优化结果保存到 `output/`。

---

## 2. 项目结构

```text
day21/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── main.py
├── 01_prompt_optimization.py
├── 02_quality_evaluation.py
├── 03_feature_backlog.py
├── 04_ux_review.py
├── 05_full_optimization_app.py
├── documents/
│   ├── 01_optimization_goals.txt
│   ├── 02_debug_checklist.md
│   └── 03_ux_rules.txt
├── modules/
│   ├── __init__.py
│   ├── project_inspector.py
│   ├── prompt_optimizer.py
│   ├── quality_evaluator.py
│   ├── feature_planner.py
│   ├── ux_reviewer.py
│   └── optimization_app.py
└── output/
```

Day 21 的核心链路是：

```text
project_inspector.py
  -> quality_evaluator.py
  -> prompt_optimizer.py
  -> feature_planner.py
  -> ux_reviewer.py
  -> optimization_app.py
```

---

## 3. 运行方式

### 3.1 安装依赖

```powershell
pip install -r requirements.txt
```

### 3.2 配置环境变量

复制 `.env.example` 为 `.env`：

```powershell
copy .env.example .env
```

默认配置：

```env
TARGET_PROJECTS=../day19,../day20
REPORT_DIR=output
MAX_PREVIEW_CHARS=500
MIN_SCORE_PASS=70
```

Day 21 不需要 API Key。

它主要使用本地规则分析项目质量、提示词、功能清单和用户体验。

### 3.3 运行完整应用

```powershell
python main.py
```

可用命令：

```text
scan
quality
prompt
features
ux
report
save
q
```

### 3.4 分步骤运行练习

```powershell
python 01_prompt_optimization.py
python 02_quality_evaluation.py
python 03_feature_backlog.py
python 04_ux_review.py
python 05_full_optimization_app.py
```

---

## 4. 项目优化与调试核心原理

### 4.1 为什么要优化项目

项目能跑只是第一步。

真正好用的项目还需要：

1. 说明清楚。
2. 入口统一。
3. 错误提示友好。
4. 输出可验证。
5. 提示词稳定。
6. 功能边界明确。
7. 有练习题和答案。

### 4.2 优化的四个方向

Day 21 围绕四个方向：

```text
优化提示词
提升准确率
增加功能
用户体验优化
```

这正好对应 Day 21 学习计划里的任务。

### 4.3 为什么要生成报告

报告可以帮助你：

1. 记录当前项目状态。
2. 知道哪些地方已经做好。
3. 知道下一步要改什么。
4. 方便以后复盘。

---

## 5. 每个文件的详细解释

### 5.1 `config.py`

统一配置文件。

主要配置：

1. `TARGET_PROJECTS`：要优化的目标项目，默认是 Day 19 和 Day 20。
2. `REPORT_DIR`：报告保存目录。
3. `MAX_PREVIEW_CHARS`：文件预览字符数。
4. `MIN_SCORE_PASS`：评分通过线。

---

### 5.2 `modules/project_inspector.py`

项目扫描模块。

核心类：

```python
ProjectInspector
```

它负责：

1. 解析项目路径。
2. 扫描 Python 文件。
3. 扫描 Markdown 文件。
4. 扫描配置文件。
5. 预览 README、main.py、config.py。

核心数据结构：

```python
ProjectSnapshot
```

它保存一个项目的扫描快照。

---

### 5.3 `modules/prompt_optimizer.py`

提示词优化模块。

它会检查提示词是否包含：

1. 角色。
2. 上下文。
3. 任务。
4. 约束。
5. 输出格式。

如果提示词不完整，它会生成更稳定的模板。

---

### 5.4 `modules/quality_evaluator.py`

项目质量评估模块。

它会检查项目是否包含：

1. README。
2. config.py。
3. main.py。
4. 足够的练习脚本。
5. 练习题说明。
6. API / 本地模式说明。

输出包括：

```text
score
findings
suggestions
```

---

### 5.5 `modules/feature_planner.py`

功能规划模块。

它会根据项目类型生成后续功能清单。

例如 Day 19 推荐：

1. sources 命令。
2. rebuild 命令。
3. eval 命令。

Day 20 推荐：

1. help 命令。
2. apply-dry-run。
3. validate 命令。

---

### 5.6 `modules/ux_reviewer.py`

用户体验评审模块。

它会检查：

1. 是否有菜单。
2. 是否有 demo/example。
3. 是否能保存结果。
4. README 是否有运行说明。

---

### 5.7 `modules/optimization_app.py`

完整优化应用模块。

它把所有模块串起来：

1. 扫描项目。
2. 评估质量。
3. 优化提示词。
4. 生成功能清单。
5. 评审用户体验。
6. 保存完整报告。

---

### 5.8 `01_prompt_optimization.py`

练习 1 文件。

作用：

```text
评估一个粗糙提示词，并生成优化后的提示词模板。
```

---

### 5.9 `02_quality_evaluation.py`

练习 2 文件。

作用：

```text
评估 Day 19 和 Day 20 的项目完整度。
```

---

### 5.10 `03_feature_backlog.py`

练习 3 文件。

作用：

```text
为 Day 19 和 Day 20 生成后续功能优化清单。
```

---

### 5.11 `04_ux_review.py`

练习 4 文件。

作用：

```text
检查目标项目命令行体验是否友好。
```

---

### 5.12 `05_full_optimization_app.py`

完整交互应用。

支持：

```text
scan
quality
prompt
features
ux
report
save
q
```

---

## 6. 练习题专区

下面是 Day 21 的完整练习题。

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

### 6.1 练习 1：优化提示词

文件：

```text
01_prompt_optimization.py
```

练习目标：

学会判断提示词是否足够清楚。

题目要求：

1. 准备一个粗糙提示词。
2. 使用 `PromptOptimizer.review()` 评分。
3. 查看缺少哪些要素。
4. 生成优化后的模板。

参考答案：

答案已经写在 `01_prompt_optimization.py` 中。

如何运行：

```powershell
python 01_prompt_optimization.py
```

你应该观察到：

1. 原始提示词。
2. 评分。
3. 优点。
4. 问题。
5. 优化后的模板。

---

### 6.2 练习 2：项目质量评估

文件：

```text
02_quality_evaluation.py
```

练习目标：

检查 Day 19 和 Day 20 的基础项目质量。

题目要求：

1. 扫描目标项目。
2. 检查 README、config.py、main.py。
3. 检查练习脚本数量。
4. 输出评分和建议。

参考答案：

答案已经写在 `02_quality_evaluation.py` 中。

如何运行：

```powershell
python 02_quality_evaluation.py
```

你应该观察到：

1. 每个项目的评分。
2. 已完成项。
3. 待优化建议。

---

### 6.3 练习 3：增加功能清单

文件：

```text
03_feature_backlog.py
```

练习目标：

为 Day 19 和 Day 20 规划后续可增加功能。

题目要求：

1. 识别项目类型。
2. 生成 5 条功能建议。
3. 标记优先级。
4. 用表格展示。

参考答案：

答案已经写在 `03_feature_backlog.py` 中。

如何运行：

```powershell
python 03_feature_backlog.py
```

你应该观察到：

1. Day 19 的 RAG 优化功能。
2. Day 20 的 Coding Agent 优化功能。
3. high / medium 优先级。

---

### 6.4 练习 4：用户体验评审

文件：

```text
04_ux_review.py
```

练习目标：

检查项目是否容易上手。

题目要求：

1. 扫描主入口和 README。
2. 检查菜单。
3. 检查 demo/example。
4. 检查 output 保存能力。
5. 输出优点和建议。

参考答案：

答案已经写在 `04_ux_review.py` 中。

如何运行：

```powershell
python 04_ux_review.py
```

你应该观察到：

1. 做得好的地方。
2. 可以继续优化的地方。

---

### 6.5 练习 5：完整优化报告

文件：

```text
05_full_optimization_app.py
```

练习目标：

体验完整项目优化与调试流程。

题目要求：

1. 启动应用。
2. 输入 `scan`。
3. 输入 `quality`。
4. 输入 `features`。
5. 输入 `ux`。
6. 输入 `report`。
7. 输入 `save`。

参考答案：

答案已经写在 `05_full_optimization_app.py` 中。

如何运行：

```powershell
python 05_full_optimization_app.py
```

或：

```powershell
python main.py
```

你应该观察到：

1. 可以生成完整报告。
2. `save` 后会在 `output/` 下保存 JSON 文件。

---

## 7. 练习题对应文件答案说明

Day 21 的练习答案已经写进对应代码文件中。

对应关系：

```text
练习 1 -> 01_prompt_optimization.py
练习 2 -> 02_quality_evaluation.py
练习 3 -> 03_feature_backlog.py
练习 4 -> 04_ux_review.py
练习 5 -> 05_full_optimization_app.py
```

这些文件都是完整可运行的参考答案。

---

## 8. API Key 与本地模式说明

Day 21 不需要 API Key。

原因：

1. 它主要做本地项目扫描。
2. 它使用规则评估提示词。
3. 它使用规则生成优化建议。
4. 它不调用大模型。

如果以后你想增强 Day 21，可以把优化建议生成接入在线模型。

---

## 9. 常见问题

### 9.1 为什么评分不是 100

评分是规则化检查，不代表项目不好。

它只是提醒你哪些方面还可以补强。

### 9.2 为什么只评估 Day 19 和 Day 20

因为 Day 21 的任务是优化第三周项目。

默认目标项目是：

```text
../day19
../day20
```

你可以在 `.env` 中修改 `TARGET_PROJECTS`。

### 9.3 保存的报告在哪里

默认保存到：

```text
day21/output/day21_optimization_report.json
```

---

## 10. 推荐学习顺序

建议按这个顺序学习：

1. 读 `README.md`。
2. 运行 `python 01_prompt_optimization.py`。
3. 运行 `python 02_quality_evaluation.py`。
4. 运行 `python 03_feature_backlog.py`。
5. 运行 `python 04_ux_review.py`。
6. 运行 `python main.py`。
7. 在主程序中输入 `report` 和 `save`。

---

## 11. Day 21 总结

Day 21 的关键词是：

```text
优化
调试
提示词
准确率
功能清单
用户体验
质量评估
报告保存
```

一句话总结：

```text
Day 21 是把项目从“能跑”推进到“更清楚、更可靠、更好用”的一天。
```
