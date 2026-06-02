# Day25 - 前端界面

Day25 的主题是 **前端界面**。

前面 Day22 学会了 FastAPI，Day23 把 Agent 变成了 API，Day24 学了部署上线。Day25 要解决的是：如何让普通用户通过一个 Web 页面来使用你的 Agent。

按照学习计划表，Day25 的任务是：

- Streamlit 入门
- 构建简单界面
- 美化 UI
- 交互优化
- 实践：做一个 Web 界面

## 1. 今日目标

学完 Day25，你应该能做到：

- 知道 Streamlit 是什么。
- 能启动一个 Streamlit Web 页面。
- 能用 `st.sidebar` 做控制面板。
- 能用 `st.chat_input` 和 `st.chat_message` 做聊天界面。
- 能用 `st.session_state` 保存聊天记录。
- 能让前端页面调用 Day23 的后端 Agent API。
- 能在没有后端时使用本地模拟模式跑通页面。

## 2. Day25 是否需要 API Key

不需要。

Day25 是前端界面任务，默认使用本地模拟 Agent。

如果你想连接 Day23 的后端，可以先启动 Day23：

```powershell
cd day23
uvicorn main:app --reload
```

然后在 Day25 页面里把模式切换为 `api`。

## 3. 项目结构

```text
day25/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── app.py
├── 01_streamlit_basics.py
├── 02_simple_ui.py
├── 03_api_connection.py
├── 04_ui_state.py
├── 05_full_frontend_demo.py
├── assets/
│   └── style.css
├── modules/
│   ├── __init__.py
│   ├── schemas.py
│   ├── local_agent.py
│   ├── api_client.py
│   ├── chat_store.py
│   └── ui_helpers.py
└── output/
```

## 4. 安装依赖

在 `D:\vscode项目\学习` 下运行：

```powershell
pip install -r day25/requirements.txt
```

指定 Python 版本：

```powershell
& "C:\Program Files\Python314\python.exe" -m pip install -r day25/requirements.txt
```

## 5. 运行练习脚本

这些脚本不需要打开网页：

```powershell
& "C:\Program Files\Python314\python.exe" day25/01_streamlit_basics.py
& "C:\Program Files\Python314\python.exe" day25/02_simple_ui.py
& "C:\Program Files\Python314\python.exe" day25/03_api_connection.py
& "C:\Program Files\Python314\python.exe" day25/04_ui_state.py
& "C:\Program Files\Python314\python.exe" day25/05_full_frontend_demo.py
```

## 6. 启动 Streamlit 页面

进入 day25：

```powershell
cd day25
streamlit run app.py
```

如果 `streamlit` 命令不可用，可以用：

```powershell
python -m streamlit run app.py
```

指定 Python：

```powershell
& "C:\Program Files\Python314\python.exe" -m streamlit run app.py
```

启动后浏览器会打开一个本地页面，通常是：

```text
http://localhost:8501
```

## 7. 页面功能说明

Day25 的页面包含：

- 顶部 Hero 区：展示项目标题和说明。
- 侧边栏控制面板：选择 `local` 或 `api` 模式。
- API 地址输入框：填写后端 Agent API 地址。
- 工具开关：控制是否允许 Agent 使用工具。
- 聊天区：展示用户和助手消息。
- 聊天输入框：输入问题。
- 清空按钮：清空聊天记录。

## 8. local 模式和 api 模式

### 8.1 local 模式

local 模式不需要后端。

页面会调用：

```python
LocalAgent().answer(question)
```

优点：

- 不需要启动 Day23；
- 不需要 API Key；
- 页面一定能跑通；
- 适合学习前端逻辑。

### 8.2 api 模式

api 模式会调用 Day23 后端：

```text
http://127.0.0.1:8000/api/agent/chat
```

请求体类似：

```json
{
  "question": "Day25 如何连接后端 API？",
  "use_tools": true
}
```

如果 Day23 后端没启动，页面会显示 API 调用失败提示，而不是直接崩掉。

## 9. 每个文件详细解释

### 9.1 requirements.txt

依赖说明：

- `streamlit`：构建 Web 页面。
- `requests`：调用后端 API。
- `python-dotenv`：读取 `.env` 配置。
- `pydantic`：管理聊天数据模型。
- `rich`：美化命令行练习脚本输出。

### 9.2 .env.example

配置示例文件。

包含：

- 页面标题；
- 页面副标题；
- 后端 API 地址；
- 默认模式；
- 页面主题色。

如果你想默认使用 API 模式，可以复制为 `.env` 后修改：

```env
DEFAULT_MODE=api
```

### 9.3 config.py

配置中心。

负责读取：

- `APP_TITLE`
- `APP_SUBTITLE`
- `AGENT_API_URL`
- `DEFAULT_MODE`
- `PRIMARY_COLOR`
- `ACCENT_COLOR`

### 9.4 assets/style.css

自定义样式文件。

Streamlit 默认界面比较普通，所以这里加了：

- 渐变 Hero；
- 卡片；
- 状态标签；
- 柔和阴影；
- 更清楚的视觉层次。

### 9.5 modules/schemas.py

数据模型文件。

包含：

- `ChatMessage`：聊天消息。
- `ChatResponse`：Agent 回答。
- `UIStatus`：页面状态。

### 9.6 modules/local_agent.py

本地模拟 Agent。

作用：

- 没有后端时仍然可以使用页面；
- 根据问题返回本地回答；
- 简单识别“前端”“Streamlit”等关键词；
- 可以计算简单数学表达式。

### 9.7 modules/api_client.py

后端 API 客户端。

负责调用：

```text
POST /api/agent/chat
```

如果请求失败，会返回：

```text
source = api-error
```

这样页面不会崩掉。

### 9.8 modules/chat_store.py

聊天记录管理。

包含：

- `add_user_message()`
- `add_assistant_message()`
- `clear()`
- `count()`

它会在 `app.py` 中放进 `st.session_state`。

### 9.9 modules/ui_helpers.py

UI 辅助函数。

包含：

- `load_css()`
- `render_hero()`
- `render_status_card()`
- `render_message()`

把这些函数拆出来，可以让 `app.py` 更简洁。

### 9.10 app.py

Streamlit 主页面。

核心逻辑：

1. 设置页面配置。
2. 加载 CSS。
3. 渲染顶部 Hero。
4. 在侧边栏选择模式。
5. 从 `session_state` 获取聊天记录。
6. 渲染历史消息。
7. 用 `st.chat_input` 接收问题。
8. 根据模式调用 LocalAgent 或 AgentAPIClient。
9. 保存并显示助手回答。

### 9.11 01_streamlit_basics.py

讲解 Streamlit 基础组件。

包括：

- `st.title`
- `st.sidebar`
- `st.chat_input`
- `st.chat_message`
- `st.session_state`

### 9.12 02_simple_ui.py

讲解页面布局结构。

包括：

- 顶部 Hero；
- 侧边栏；
- 主聊天区域；
- 输入框；
- 状态卡片。

### 9.13 03_api_connection.py

测试后端 API 连接。

如果 Day23 没启动，也会返回清楚的错误说明。

### 9.14 04_ui_state.py

演示聊天记录管理。

重点理解：Streamlit 页面会反复重新运行，普通变量不能保存状态。

### 9.15 05_full_frontend_demo.py

命令行模拟完整前端流程。

流程：

```text
用户提问 -> 保存用户消息 -> Agent 回答 -> 保存助手消息 -> 打印聊天记录
```

## 10. 核心知识点

### 10.1 Streamlit 是什么

Streamlit 是一个用 Python 快速构建 Web 页面的小框架。

它特别适合：

- AI Demo；
- 数据分析页面；
- 内部工具；
- 快速原型；
- 聊天机器人界面。

### 10.2 为什么要做前端界面

命令行适合开发者。

Web 页面适合普通用户。

如果你的 Agent 只能在终端运行，别人很难使用。

如果你的 Agent 有一个页面，别人只需要输入问题、点击按钮，就可以体验。

### 10.3 st.session_state 是什么

Streamlit 每次点击按钮、输入内容，都会重新执行脚本。

所以普通变量会丢失。

`st.session_state` 可以保存状态，例如：

- 聊天记录；
- 当前模式；
- 用户配置；
- 历史输入。

### 10.4 前端如何调用后端

前端通过 HTTP 请求调用后端。

Day25 使用：

```python
requests.post(api_url, json={"question": question, "use_tools": use_tools})
```

后端返回 JSON，前端再展示到页面上。

### 10.5 UI 美化要注意什么

美化不是堆颜色。

更重要的是：

- 信息层次清楚；
- 输入区域明显；
- 状态提示明确；
- 错误提示友好；
- 页面不要让用户迷路。

## 11. 练习题

### 练习 1：为什么需要 st.session_state

要求：

- 解释普通变量为什么保存不了聊天记录。

答案位置：

- 已写在 `01_streamlit_basics.py` 文件后面的注释中。

### 练习 2：添加清空聊天记录按钮

要求：

- 在侧边栏添加按钮；
- 点击后清空聊天记录；
- 重新渲染页面。

答案位置：

- 已写在 `02_simple_ui.py` 文件后面的注释中。

### 练习 3：修改后端 API 地址

要求：

- 如果后端运行在 9000 端口，修改配置。

答案位置：

- 已写在 `03_api_connection.py` 文件后面的注释中。

### 练习 4：为什么不用普通 list 保存聊天记录

要求：

- 解释 Streamlit 重跑机制。

答案位置：

- 已写在 `04_ui_state.py` 文件后面的注释中。

### 练习 5：把命令行流程搬到 Streamlit 页面

要求：

- 说明从输入到回答展示的完整流程。

答案位置：

- 已写在 `05_full_frontend_demo.py` 文件后面的注释中。

### 练习 6：启动 Day25 页面

要求：

- 使用 Streamlit 启动页面。

答案位置：

- 已写在 `app.py` 文件后面的注释中。

## 12. 常见错误

### 12.1 streamlit 命令不可用

运行：

```powershell
python -m streamlit run app.py
```

或者：

```powershell
& "C:\Program Files\Python314\python.exe" -m streamlit run app.py
```

### 12.2 API 模式调用失败

先确认 Day23 是否启动：

```powershell
cd day23
uvicorn main:app --reload
```

再确认地址是否是：

```text
http://127.0.0.1:8000/api/agent/chat
```

### 12.3 页面没有保存聊天记录

检查是否使用了：

```python
st.session_state
```

如果每次输入后历史记录消失，通常是因为只用了普通变量。

### 12.4 样式没有生效

检查：

- `assets/style.css` 是否存在；
- `ui_helpers.py` 是否调用了 `load_css()`；
- `app.py` 是否在页面开头调用了 `load_css()`。

## 13. 今日总结

Day25 你完成了从 API 到 Web 页面的一步。

现在你的项目不只是后端能跑，而是具备了一个用户可以直接操作的界面。

后面 Day26 会进入 GitHub 优化，把代码结构、README、截图、文档继续整理成更适合展示和求职的项目。
