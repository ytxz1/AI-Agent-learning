# Day26 - GitHub 优化

Day26 的主题是 **GitHub 优化**。

前面 Day22 到 Day25，我们已经完成了 API、部署和前端页面。Day26 要做的是把项目整理成更适合展示的 GitHub 仓库。

按照学习计划表，Day26 的任务是：

- 整理代码结构
- 完善 README
- 添加截图 / GIF
- 项目文档
- 产出：高质量 GitHub 仓库

## 1. 今日目标

学完 Day26，你应该能做到：

- 知道一个高质量 GitHub 仓库应该包含什么。
- 能检查项目结构是否清楚。
- 能判断 README 是否适合展示。
- 能准备截图和 GIF 计划。
- 能生成 GitHub 展示检查清单。
- 能生成项目质量报告。
- 能把学习项目包装成更适合简历和实习投递的作品。

## 2. Day26 是否需要 API Key

不需要。

Day26 是项目整理和 GitHub 展示优化，不涉及大模型 API 调用。

## 3. 项目结构

```text
day26/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── 01_code_structure_review.py
├── 02_readme_optimizer.py
├── 03_screenshot_plan.py
├── 04_project_docs.py
├── 05_github_quality_report.py
├── docs/
│   └── github_profile_tips.md
├── modules/
│   ├── __init__.py
│   ├── schemas.py
│   ├── project_scanner.py
│   ├── readme_reviewer.py
│   ├── github_advisor.py
│   ├── doc_generator.py
│   └── report_writer.py
├── assets/
└── output/
```

## 4. 安装依赖

在 `D:\vscode项目\学习` 下运行：

```powershell
pip install -r day26/requirements.txt
```

指定 Python：

```powershell
& "C:\Program Files\Python314\python.exe" -m pip install -r day26/requirements.txt
```

## 5. 运行练习脚本

```powershell
& "C:\Program Files\Python314\python.exe" day26/01_code_structure_review.py
& "C:\Program Files\Python314\python.exe" day26/02_readme_optimizer.py
& "C:\Program Files\Python314\python.exe" day26/03_screenshot_plan.py
& "C:\Program Files\Python314\python.exe" day26/04_project_docs.py
& "C:\Program Files\Python314\python.exe" day26/05_github_quality_report.py
```

## 6. 配置目标项目

默认检查 `day25`。

如果你想检查其他项目，可以复制 `.env.example` 为 `.env`，修改：

```env
TARGET_DAY=day23
```

也可以改成：

```env
TARGET_DAY=day24
```

## 7. 每个文件详细解释

### 7.1 requirements.txt

依赖说明：

- `python-dotenv`：读取 `.env` 配置。
- `pydantic`：定义检查结果和报告模型。
- `rich`：美化命令行输出。

### 7.2 .env.example

配置示例文件。

包含：

- `PROJECT_NAME`：项目名称。
- `TARGET_DAY`：要检查的目标目录。
- `AUTHOR_NAME`：作者名称。
- `GITHUB_REPO_URL`：GitHub 仓库地址。
- `IGNORE_OUTPUT`：是否忽略 output 文件夹。

### 7.3 config.py

配置中心。

负责读取 `.env` 并提供：

- 项目名；
- 目标 day；
- 仓库地址；
- 工作区路径；
- `get_target_project_dir()`。

### 7.4 modules/schemas.py

数据模型文件。

包含：

- `ProjectFile`：项目文件信息。
- `CheckItem`：单个检查项。
- `GitHubReport`：GitHub 优化报告。
- `ScreenshotPlan`：截图计划。

### 7.5 modules/project_scanner.py

项目结构扫描器。

负责：

- 列出目标项目文件；
- 检查 README；
- 检查 requirements；
- 检查主入口；
- 检查 modules；
- 检查 assets；
- 检查 docs。

### 7.6 modules/readme_reviewer.py

README 检查器。

会检查 README 是否包含：

- 项目；
- 安装；
- 运行；
- 结构；
- 练习；
- 常见错误。

还会生成 README 优化建议。

### 7.7 modules/github_advisor.py

GitHub 优化建议生成器。

它会综合：

- 项目结构检查；
- README 检查；
- 项目亮点；
- 下一步行动；

最终生成一个 `GitHubReport`。

### 7.8 modules/doc_generator.py

文档生成器。

负责生成：

- 截图计划；
- README 亮点段落；
- GitHub 展示检查清单。

### 7.9 modules/report_writer.py

报告写入工具。

负责把报告写入：

- `output/github_report.md`
- `output/github_report.json`
- `output/readme_highlights.md`
- `output/showcase_checklist.md`

### 7.10 01_code_structure_review.py

练习 01：整理代码结构。

它会扫描目标项目，并输出结构检查结果。

### 7.11 02_readme_optimizer.py

练习 02：完善 README。

它会检查 README 的展示完整度，并输出优化建议。

### 7.12 03_screenshot_plan.py

练习 03：添加截图和 GIF 计划。

它会告诉你 GitHub README 里应该放哪些截图。

### 7.13 04_project_docs.py

练习 04：生成项目文档。

它会写入：

- `output/readme_highlights.md`
- `output/showcase_checklist.md`

### 7.14 05_github_quality_report.py

练习 05：生成 GitHub 仓库质量报告。

它会写入：

- `output/github_report.md`
- `output/github_report.json`

### 7.15 docs/github_profile_tips.md

GitHub 展示建议文档。

包含：

- 仓库名建议；
- Topics 建议；
- README 开头建议；
- 截图建议；
- 简历描述建议。

## 8. 什么是高质量 GitHub 仓库

一个适合展示的仓库，至少应该具备：

- 清楚的项目名称；
- 详细 README；
- 可复制的安装命令；
- 可复制的运行命令；
- 项目结构说明；
- 截图或 GIF；
- 功能亮点；
- 常见错误；
- 后续计划；
- 干净的代码结构。

## 9. README 推荐结构

可以按这个顺序写：

```text
# 项目名称

一句话说明项目是什么。

## 项目亮点

## 技术栈

## 效果截图

## 项目结构

## 安装依赖

## 运行方式

## 核心功能

## 常见问题

## 后续计划
```

## 10. 截图和 GIF 为什么重要

别人第一次打开你的仓库时，通常不会马上 clone 代码。

如果 README 有截图，别人可以快速知道：

- 项目是否真的能跑；
- 页面长什么样；
- API 是否完整；
- 你做到了什么程度。

所以截图不是装饰，而是项目展示的一部分。

## 11. GitHub Topics 建议

建议添加：

- `python`
- `fastapi`
- `streamlit`
- `ai-agent`
- `rag`
- `langchain`
- `docker`
- `openai`

## 12. 练习题

### 练习 1：GitHub 项目最少应该有哪些文件

要求：

- 说出一个项目最基础的展示文件。

答案位置：

- 已写在 `01_code_structure_review.py` 文件后面的注释中。

### 练习 2：README 最应该写清楚哪三件事

要求：

- 总结 README 的核心作用。

答案位置：

- 已写在 `02_readme_optimizer.py` 文件后面的注释中。

### 练习 3：为什么 README 里最好放截图

要求：

- 解释截图对项目展示的作用。

答案位置：

- 已写在 `03_screenshot_plan.py` 文件后面的注释中。

### 练习 4：项目文档应该放在哪里

要求：

- 区分 README、docs、output 的用途。

答案位置：

- 已写在 `04_project_docs.py` 文件后面的注释中。

### 练习 5：评分低是不是说明项目没用

要求：

- 正确理解质量评分。

答案位置：

- 已写在 `05_github_quality_report.py` 文件后面的注释中。

### 练习 6：如何写入一个简单报告

要求：

- 调用 `write_text_report()`。

答案位置：

- 已写在 `modules/report_writer.py` 文件后面的 `if __name__ == "__main__":` 中。

## 13. 常见错误

### 13.1 README 写得太短

只写一句“这是我的项目”是不够的。

至少要说明：

- 项目是什么；
- 怎么运行；
- 有哪些功能；
- 有什么亮点；
- 遇到问题怎么办。

### 13.2 没有截图

没有截图时，别人很难快速理解项目效果。

建议至少放一张：

```text
assets/streamlit-ui.png
```

### 13.3 运行命令不完整

不要只写：

```text
运行 main.py
```

应该写成可以直接复制的命令：

```powershell
& "C:\Program Files\Python314\python.exe" day25/05_full_frontend_demo.py
```

### 13.4 仓库结构太乱

如果所有代码都堆在根目录，别人会很难读。

建议：

- 核心代码放 `modules/`；
- 文档放 `docs/`；
- 图片放 `assets/`；
- 输出报告放 `output/`。

## 14. 今日总结

Day26 你完成的是“项目展示能力”。

写代码是一部分，把代码整理成别人愿意看、能运行、能理解的仓库，是另一项非常重要的能力。

一个好的 GitHub 仓库，会让你的项目更像作品，而不是零散练习。
