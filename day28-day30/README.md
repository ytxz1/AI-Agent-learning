# Day28-Day30 - 投递与冲刺

Day28-Day30 是 1 个月 AI Agent 学习计划的最后三天，主题是 **投递与冲刺**。

前面你已经完成了：

- Python 和 API 基础；
- LangChain / Agent / Tools；
- RAG 项目；
- FastAPI 后端；
- Docker 部署；
- Streamlit 前端；
- GitHub 优化；
- 简历和面试准备。

最后三天要做的是把这些成果真正用于求职。

## 1. 三天目标

### Day28：投递实习岗位

- 筛选岗位；
- 分析 JD 关键词；
- 判断项目经历匹配度；
- 生成投递优先级；
- 开始投递。

### Day29：跟进面试

- 统计投递进度；
- 记录下一步行动；
- 准备面试清单；
- 复习项目介绍；
- 跟进已投递岗位。

### Day30：总结复盘

- 汇总岗位、投递、面试记录；
- 复盘 30 天成果；
- 明确下一轮补强方向；
- 形成 Offer 冲刺清单。

## 2. 是否需要 API Key

不需要。

Day28-Day30 是求职冲刺工具，不涉及大模型 API 调用。

## 3. 项目结构

```text
day28-day30/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── 01_day28_apply_jobs.py
├── 02_day29_follow_interviews.py
├── 03_day30_final_summary.py
├── 04_offer_sprint_checklist.py
├── 05_full_sprint_workflow.py
├── data/
│   ├── job_targets.json
│   ├── application_records.json
│   └── interview_reviews.json
├── templates/
│   ├── follow_up_message.md
│   └── final_summary_template.md
├── modules/
│   ├── __init__.py
│   ├── schemas.py
│   ├── data_loader.py
│   ├── job_matcher.py
│   ├── application_tracker.py
│   ├── interview_planner.py
│   ├── sprint_report.py
│   └── report_writer.py
└── output/
```

## 4. 安装依赖

在 `D:\vscode项目\学习` 下运行：

```powershell
pip install -r day28-day30/requirements.txt
```

指定 Python：

```powershell
& "C:\Program Files\Python314\python.exe" -m pip install -r day28-day30/requirements.txt
```

## 5. 运行练习脚本

```powershell
& "C:\Program Files\Python314\python.exe" day28-day30/01_day28_apply_jobs.py
& "C:\Program Files\Python314\python.exe" day28-day30/02_day29_follow_interviews.py
& "C:\Program Files\Python314\python.exe" day28-day30/03_day30_final_summary.py
& "C:\Program Files\Python314\python.exe" day28-day30/04_offer_sprint_checklist.py
& "C:\Program Files\Python314\python.exe" day28-day30/05_full_sprint_workflow.py
```

运行后会在 `output/` 生成：

- `day28_job_match_report.md`
- `day29_interview_follow_up.md`
- `day30_final_summary.md`
- `offer_sprint_checklist.md`
- `full_sprint_workflow.md`
- `full_sprint_workflow.json`

## 6. 每个文件详细解释

### 6.1 requirements.txt

依赖说明：

- `python-dotenv`：读取 `.env` 配置；
- `pydantic`：定义岗位、投递、面试复盘数据模型；
- `rich`：让命令行输出更清楚。

### 6.2 .env.example

配置示例文件。

包含：

- 候选人姓名；
- 目标岗位；
- 目标城市；
- 目标公司类型；
- 本周投递目标；
- 数据文件路径。

### 6.3 config.py

配置中心。

负责读取：

- `CANDIDATE_NAME`
- `TARGET_ROLE`
- `TARGET_CITY`
- `TARGET_COMPANY_TYPE`
- `WEEKLY_APPLICATION_GOAL`
- `JOB_FILE`
- `APPLICATION_FILE`
- `INTERVIEW_FILE`
- `OUTPUT_DIR`

### 6.4 data/job_targets.json

目标岗位列表。

每条岗位包含：

- 公司；
- 岗位；
- 城市；
- 来源；
- JD 关键词；
- 匹配原因；
- 优先级。

### 6.5 data/application_records.json

投递记录。

每条记录包含：

- 公司；
- 岗位；
- 日期；
- 渠道；
- 状态；
- 下一步行动；
- 备注。

### 6.6 data/interview_reviews.json

面试复盘记录。

每条记录包含：

- 公司；
- 岗位；
- 面试日期；
- 被问到的问题；
- 表现好的地方；
- 待改进的地方；
- 结果。

### 6.7 templates/follow_up_message.md

投递或面试跟进消息模板。

你可以根据具体公司和岗位稍微修改后发送。

### 6.8 templates/final_summary_template.md

30 天学习总结模板。

用于整理：

- 完成了什么；
- 最有价值的项目；
- 下一轮要补强什么。

### 6.9 modules/schemas.py

数据模型文件。

包含：

- `JobTarget`：目标岗位；
- `ApplicationRecord`：投递记录；
- `InterviewReview`：面试复盘；
- `SprintCheckItem`：冲刺检查项。

### 6.10 modules/data_loader.py

JSON 数据加载工具。

负责读取：

- 岗位数据；
- 投递数据；
- 面试复盘数据。

### 6.11 modules/job_matcher.py

岗位匹配分析器。

它会根据 JD 关键词和你当前项目技能计算匹配分。

匹配分越高，越应该优先投递。

### 6.12 modules/application_tracker.py

投递记录统计器。

它会统计：

- 已投递数量；
- 本周目标；
- 完成进度；
- 各状态数量；
- 投递渠道；
- 需要跟进的事项。

### 6.13 modules/interview_planner.py

面试准备与复盘工具。

它会生成：

- 面试前准备清单；
- 面试复盘摘要；
- 常见项目问题。

### 6.14 modules/sprint_report.py

30 天冲刺总结报告生成器。

它会综合：

- 岗位匹配；
- 投递统计；
- 面试复盘；
- 最终冲刺清单。

### 6.15 modules/report_writer.py

报告写入工具。

负责写入 Markdown 和 JSON。

### 6.16 01_day28_apply_jobs.py

Day28 投递实习岗位练习。

它会生成岗位匹配报告：

```text
output/day28_job_match_report.md
```

### 6.17 02_day29_follow_interviews.py

Day29 跟进面试练习。

它会生成面试跟进报告：

```text
output/day29_interview_follow_up.md
```

### 6.18 03_day30_final_summary.py

Day30 总结复盘练习。

它会生成：

```text
output/day30_final_summary.md
```

### 6.19 04_offer_sprint_checklist.py

Offer 冲刺检查清单。

它会生成：

```text
output/offer_sprint_checklist.md
```

### 6.20 05_full_sprint_workflow.py

完整求职冲刺工作流。

一次性运行岗位匹配、投递统计、面试准备和总结报告。

## 7. Day28 投递策略

投递不是越多越好，而是先保证匹配度。

优先投递：

- JD 中出现 Python；
- JD 中出现 FastAPI；
- JD 中出现 LLM / Agent / RAG；
- JD 中提到 API 开发；
- JD 中提到 Docker 或部署；
- JD 中需要 GitHub 项目展示。

## 8. Day29 跟进策略

投递后不要完全等消息。

你应该记录：

- 投递日期；
- 投递渠道；
- 当前状态；
- 下一步行动；
- 是否需要补充作品集；
- 是否需要准备面试题。

## 9. Day30 复盘策略

30 天结束后，要问自己：

- 我完成了哪些可展示项目？
- 哪个项目最适合写进简历？
- 哪些岗位最匹配？
- 面试时我最容易卡在哪里？
- 下一轮 7 天要补强什么？

## 10. 求职闭环

完整求职闭环是：

```text
筛选岗位 -> 修改简历 -> 投递 -> 跟进 -> 面试 -> 复盘 -> 修改项目和表达 -> 再投递
```

不要只停留在学习，也不要只盲目投递。

## 11. 练习题

### 练习 1：为什么投递岗位要看关键词匹配

答案位置：

- 已写在 `01_day28_apply_jobs.py` 文件后面的注释中。

### 练习 2：为什么投递后要记录 next_action

答案位置：

- 已写在 `02_day29_follow_interviews.py` 文件后面的注释中。

### 练习 3：30 天结束后是不是就停止学习

答案位置：

- 已写在 `03_day30_final_summary.py` 文件后面的注释中。

### 练习 4：冲刺阶段最重要的事情是什么

答案位置：

- 已写在 `04_offer_sprint_checklist.py` 文件后面的注释中。

### 练习 5：为什么要把岗位、投递、面试放在一个工作流里

答案位置：

- 已写在 `05_full_sprint_workflow.py` 文件后面的注释中。

### 练习 6：如何生成 30 天冲刺总结

答案位置：

- 已写在 `modules/sprint_report.py` 文件后面的 `if __name__ == "__main__":` 中。

### 练习 7：如何写入一份跟进记录

答案位置：

- 已写在 `modules/report_writer.py` 文件后面的 `if __name__ == "__main__":` 中。

## 12. 常见错误

### 12.1 只学习不投递

学习项目是为了形成作品和能力，最后必须进入投递和面试环节。

### 12.2 只投递不复盘

如果投递后没有回复，要复盘：

- 简历是否太弱；
- 项目是否没有截图；
- JD 是否不匹配；
- 沟通话术是否不清楚。

### 12.3 面试后不记录问题

面试问题是最真实的学习资料。

每次面试后当天记录：

- 被问了什么；
- 哪些回答好；
- 哪些回答卡住；
- 下次如何回答。

### 12.4 一直做新功能，不展示已有成果

冲刺阶段不是无限加功能。

更重要的是：

- 把项目讲清楚；
- 把 README 写清楚；
- 把截图补上；
- 把简历投出去；
- 根据反馈迭代。

## 13. 今日总结

Day28-Day30 完成的是最后的求职闭环。

一个月学习计划的目标不是“学完就结束”，而是让你拥有：

- 可运行项目；
- 可展示仓库；
- 可投递简历；
- 可回答面试问题；
- 可持续复盘的求职节奏。

如果你能坚持投递、复盘、迭代，这个 30 天计划就真正变成了拿 Offer 的起点。
