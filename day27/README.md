# Day27 - 简历优化与面试准备

Day27 的主题是 **简历优化与面试准备**。

前面 Day22 到 Day26，我们已经完成了 API、部署、前端和 GitHub 优化。Day27 要做的是把这些项目成果转化成可以用于求职的材料：

- 简历项目经历；
- 技术栈表达；
- 常见面试题；
- 自我介绍；
- 模拟面试反馈。

按照学习计划表，Day27 的任务是：

- 项目经历提炼
- 技术栈梳理
- 常见面试题
- 自我介绍准备
- 实践：模拟面试

## 1. 今日目标

学完 Day27，你应该能做到：

- 把一个学习项目写成简历上的项目经历。
- 知道简历 bullet 应该突出技术、动作、问题和结果。
- 能把技术栈讲成项目场景，而不是只说“我用过”。
- 能准备 AI Agent / FastAPI / Docker / Streamlit 相关面试题。
- 能写出 1 分钟自我介绍。
- 能通过模拟面试发现回答太空、太短或缺少结果的问题。

## 2. Day27 是否需要 API Key

不需要。

Day27 是简历和面试准备，不涉及大模型 API 调用。

## 3. 项目结构

```text
day27/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── 01_project_experience.py
├── 02_tech_stack_summary.py
├── 03_interview_questions.py
├── 04_self_intro.py
├── 05_mock_interview.py
├── data/
│   ├── project_profile.json
│   └── interview_questions.json
├── templates/
│   └── resume_project_template.md
├── modules/
│   ├── __init__.py
│   ├── schemas.py
│   ├── profile_loader.py
│   ├── resume_builder.py
│   ├── tech_stack_mapper.py
│   ├── interview_bank.py
│   ├── mock_interviewer.py
│   └── report_writer.py
└── output/
```

## 4. 安装依赖

在 `D:\vscode项目\学习` 下运行：

```powershell
pip install -r day27/requirements.txt
```

指定 Python：

```powershell
& "C:\Program Files\Python314\python.exe" -m pip install -r day27/requirements.txt
```

## 5. 运行练习脚本

```powershell
& "C:\Program Files\Python314\python.exe" day27/01_project_experience.py
& "C:\Program Files\Python314\python.exe" day27/02_tech_stack_summary.py
& "C:\Program Files\Python314\python.exe" day27/03_interview_questions.py
& "C:\Program Files\Python314\python.exe" day27/04_self_intro.py
& "C:\Program Files\Python314\python.exe" day27/05_mock_interview.py
```

运行后会在 `output/` 中生成：

- `resume_project.md`
- `tech_stack_summary.md`
- `interview_questions.md`
- `self_intro.md`
- `mock_interview_feedback.md`
- `mock_interview_feedback.json`

## 6. 每个文件详细解释

### 6.1 requirements.txt

依赖说明：

- `python-dotenv`：读取 `.env` 配置。
- `pydantic`：定义项目经历、面试题和反馈模型。
- `rich`：美化命令行输出。

### 6.2 .env.example

配置示例文件。

包含：

- `CANDIDATE_NAME`：你的名字。
- `TARGET_ROLE`：目标岗位。
- `TARGET_COMPANY`：目标公司。
- `PROJECT_NAME`：项目名称。
- `PROFILE_FILE`：项目经历素材文件。

### 6.3 config.py

配置中心。

负责读取：

- 候选人姓名；
- 目标岗位；
- 目标公司；
- 项目名称；
- 项目素材路径；
- 输出目录。

### 6.4 data/project_profile.json

项目经历素材文件。

它用结构化方式记录：

- 项目背景；
- 项目功能；
- 技术栈；
- 项目亮点；
- 遇到的问题；
- 解决方案；
- 最终结果。

简历和面试回答都应该从真实项目素材中提炼，而不是凭空编。

### 6.5 data/interview_questions.json

面试题库。

包含分类：

- 项目经历；
- FastAPI；
- 工程化；
- 部署；
- 前端；
- RAG；
- 自我反思。

### 6.6 templates/resume_project_template.md

简历项目经历模板。

里面包含：

- 简历写法；
- 面试讲法；
- 可以直接参考的项目描述。

### 6.7 modules/schemas.py

数据模型文件。

包含：

- `Challenge`：项目挑战。
- `ProjectProfile`：项目经历素材。
- `ResumeBullet`：简历 bullet。
- `InterviewQuestion`：面试题。
- `MockFeedback`：模拟面试反馈。

### 6.8 modules/profile_loader.py

项目素材加载器。

负责读取 `data/project_profile.json`，并转换成 `ProjectProfile` 对象。

### 6.9 modules/resume_builder.py

简历项目经历生成器。

它会根据项目素材生成：

- 项目标题；
- 5 条简历 bullet；
- 可复制到简历里的 Markdown 文本。

### 6.10 modules/tech_stack_mapper.py

技术栈梳理器。

它会把技术栈转成面试表达：

- 技术是什么；
- 项目中怎么用；
- 面试时怎么讲。

### 6.11 modules/interview_bank.py

面试题库管理器。

功能：

- 读取全部面试题；
- 按分类筛选面试题；
- 输出题目和回答提示。

### 6.12 modules/mock_interviewer.py

模拟面试评分器。

它不是大模型，而是规则评分器。

它会检查回答中是否包含：

- 项目；
- FastAPI；
- Streamlit；
- Docker；
- API；
- 问题；
- 解决；
- 结果；
- 学习。

评分不是绝对标准，而是帮助你发现回答是否缺少关键内容。

### 6.13 modules/report_writer.py

报告写入工具。

负责写入：

- Markdown 文件；
- JSON 文件。

### 6.14 01_project_experience.py

练习 01：项目经历提炼。

它会生成：

```text
output/resume_project.md
```

### 6.15 02_tech_stack_summary.py

练习 02：技术栈梳理。

它会生成：

```text
output/tech_stack_summary.md
```

### 6.16 03_interview_questions.py

练习 03：常见面试题准备。

它会生成：

```text
output/interview_questions.md
```

### 6.17 04_self_intro.py

练习 04：自我介绍准备。

它会生成：

```text
output/self_intro.md
```

### 6.18 05_mock_interview.py

练习 05：模拟面试。

它会生成：

```text
output/mock_interview_feedback.md
output/mock_interview_feedback.json
```

## 7. 简历项目经历怎么写

不要写成：

```text
学习了 Python、FastAPI、Docker、Streamlit。
```

这样太像学习记录，不像项目经历。

更好的写法：

```text
使用 FastAPI 将 Agent 能力封装为 REST API，支持普通问答、流式响应、健康检查和统一错误处理。
```

因为它说明了：

- 用了什么技术；
- 做了什么功能；
- 体现了什么能力。

## 8. 简历 bullet 推荐结构

推荐使用：

```text
使用 技术 + 完成 功能 + 解决 问题 + 产生 结果
```

例如：

```text
设计本地 fallback 方案，在未配置 API Key 或在线模型异常时仍可完整演示项目。
```

这句话体现：

- 工程稳定性；
- 对演示场景的考虑；
- 对 API 依赖问题的解决能力。

## 9. 面试项目介绍结构

推荐使用：

```text
背景 -> 目标 -> 技术栈 -> 核心功能 -> 难点 -> 结果 -> 收获
```

示例：

```text
这个项目是我为了系统学习 AI Agent 工程化能力做的连续实践。
目标是把 AI 能力从脚本逐步做成 API、部署配置和前端页面。
我使用 FastAPI 做接口化，Streamlit 做前端展示，Docker 准备部署。
项目中我遇到的一个问题是 API Key 或网络异常时无法稳定演示，
所以我设计了本地 fallback，让项目没有在线模型也能完整跑通。
最终我完成了从后端接口、部署配置到前端页面的完整链路。
```

## 10. 技术栈怎么讲

不要只说：

```text
我用过 FastAPI。
```

应该说：

```text
我在项目中使用 FastAPI 将 Agent 能力封装成 REST API，
包括普通问答接口、流式响应接口、健康检查和统一错误处理。
这样前端页面和外部系统就可以通过 HTTP 调用 Agent。
```

## 11. 常见面试问题

你至少要准备：

- 请介绍一下你的项目。
- 这个项目最难的地方是什么？
- 为什么要用 FastAPI？
- 为什么要做本地 fallback？
- Docker 部署时为什么监听 `0.0.0.0`？
- Streamlit 为什么需要 `session_state`？
- RAG 的基本流程是什么？
- 如果让你继续优化这个项目，你会做什么？

## 12. 自我介绍建议

自我介绍控制在 1 分钟左右。

结构：

- 我是谁；
- 我投什么方向；
- 我最近做了什么项目；
- 项目用了什么技术；
- 我最想突出什么能力；
- 我希望在实习中继续提升什么。

## 13. 练习题

### 练习 1：简历项目经历不要写成流水账

要求：

- 说明简历项目经历应该突出什么。

答案位置：

- 已写在 `01_project_experience.py` 文件后面的注释中。

### 练习 2：面试时说技术栈最常见的问题

要求：

- 说明为什么不能只说“我用过某技术”。

答案位置：

- 已写在 `02_tech_stack_summary.py` 文件后面的注释中。

### 练习 3：为什么不能只背标准答案

要求：

- 说明面试官真正想听什么。

答案位置：

- 已写在 `03_interview_questions.py` 文件后面的注释中。

### 练习 4：自我介绍应该控制在多久

要求：

- 说明自我介绍的时间和重点。

答案位置：

- 已写在 `04_self_intro.py` 文件后面的注释中。

### 练习 5：模拟面试回答最重要的结构

要求：

- 给出项目回答结构。

答案位置：

- 已写在 `05_mock_interview.py` 文件后面的注释中。

### 练习 6：如何做一次模拟面试评分

要求：

- 调用 `MockInterviewer.evaluate()`。

答案位置：

- 已写在 `modules/mock_interviewer.py` 文件后面的 `if __name__ == "__main__":` 中。

### 练习 7：如何写入 Markdown 报告

要求：

- 调用 `write_markdown()`。

答案位置：

- 已写在 `modules/report_writer.py` 文件后面的 `if __name__ == "__main__":` 中。

## 14. 常见错误

### 14.1 简历写得像学习笔记

错误写法：

```text
学习了 FastAPI、Docker、Streamlit。
```

优化写法：

```text
使用 FastAPI 将 Agent 能力封装为 REST API，并通过 Streamlit 构建聊天前端。
```

### 14.2 面试回答没有结果

回答项目时不要只说做了什么，还要说结果。

例如：

```text
最终完成了从后端 API、部署配置到前端页面的完整链路。
```

### 14.3 不敢讲遇到的问题

项目遇到问题很正常。

面试官更想听的是：

- 你怎么发现问题；
- 你怎么定位；
- 你怎么解决；
- 你学到了什么。

### 14.4 技术栈讲得太虚

不要说：

```text
我了解 Docker。
```

要说：

```text
我用 Dockerfile 和 docker-compose 为 FastAPI 项目准备容器化部署配置，并通过 /api/health 做健康检查。
```

## 15. 今日总结

Day27 你完成的是“把项目转化成求职表达”的能力。

写完项目只是第一步，能把项目讲清楚、写进简历、回答面试问题，才是真正能用于实习投递的作品。
