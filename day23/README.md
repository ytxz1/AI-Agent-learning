# Day23 - 集成项目 API

Day23 的主题是 **集成项目 API**。

在 Day22 里，我们学习了 FastAPI 基础。Day23 要更进一步：把前面做过的 Agent 思路包装成可以被外部调用的 API。

按照学习计划表，Day23 的任务是：

- 将 Agent 接口化
- 学习流式响应
- 学习错误处理
- 学习跨域配置
- 实践：把项目变成 API

## 1. 今日目标

学完 Day23，你应该能做到：

- 知道为什么脚本项目要改造成 API。
- 能写出 `POST /api/agent/chat` 这样的 Agent 问答接口。
- 能用 `StreamingResponse` 做流式输出。
- 能用自定义异常和异常处理器统一返回错误。
- 能配置 CORS，让前端页面可以调用后端 API。
- 能用 `TestClient` 在不启动服务器的情况下测试接口。

## 2. Day23 和 Day22 的区别

Day22 是 FastAPI 入门，重点是：

- 路由
- 请求参数
- 响应模型
- 自动文档

Day23 是项目集成，重点是：

- 把业务逻辑封装成服务类
- 把 Agent 能力暴露为 HTTP API
- 让前端或其他系统可以调用
- 处理真实项目会遇到的错误和跨域问题

简单说：

```text
Day22：学会写 API
Day23：把 Agent 项目变成 API
```

## 3. 是否需要 API Key

Day23 支持 OpenAI API，但不是必须。

如果你在 `day23/.env` 中配置了：

```env
OPENAI_API_KEY=你的 key
OPENAI_MODEL=gpt-4o-mini
```

项目会优先尝试调用在线模型。

如果没有配置 API Key，或者在线调用失败，项目会自动使用本地模拟 Agent。

这样设计是为了保证：

- 有 Key 时能体验真实大模型接口；
- 没 Key 时也能完整学习 FastAPI 集成；
- API 或网络出问题时项目不会直接崩掉。

## 4. 项目结构

```text
day23/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── main.py
├── 01_agent_api.py
├── 02_streaming_response.py
├── 03_error_handling.py
├── 04_cors_config.py
├── 05_full_api_test.py
├── data/
│   └── agent_knowledge.txt
├── modules/
│   ├── __init__.py
│   ├── schemas.py
│   ├── exceptions.py
│   ├── tools.py
│   ├── agent_service.py
│   ├── routes.py
│   └── app_factory.py
└── output/
```

## 5. 安装依赖

在 `D:\vscode项目\学习` 下运行：

```powershell
pip install -r day23/requirements.txt
```

如果你使用指定 Python：

```powershell
& "C:\Program Files\Python314\python.exe" -m pip install -r day23/requirements.txt
```

## 6. 快速运行

### 6.1 运行练习脚本

这些脚本不需要启动服务器，会用 `TestClient` 模拟请求：

```powershell
& "C:\Program Files\Python314\python.exe" day23/01_agent_api.py
& "C:\Program Files\Python314\python.exe" day23/02_streaming_response.py
& "C:\Program Files\Python314\python.exe" day23/03_error_handling.py
& "C:\Program Files\Python314\python.exe" day23/04_cors_config.py
& "C:\Program Files\Python314\python.exe" day23/05_full_api_test.py
```

### 6.2 查看主入口说明

```powershell
& "C:\Program Files\Python314\python.exe" day23/main.py
```

### 6.3 启动完整 API 服务

```powershell
cd day23
uvicorn main:app --reload
```

启动后访问：

- Swagger 文档：http://127.0.0.1:8000/docs
- ReDoc 文档：http://127.0.0.1:8000/redoc
- 首页：http://127.0.0.1:8000/
- 健康检查：http://127.0.0.1:8000/api/health

## 7. API 接口说明

### 7.1 首页

```http
GET /
```

返回：

```json
{
  "message": "欢迎来到 Day23 Agent API，请访问 /docs 查看接口文档。"
}
```

### 7.2 健康检查

```http
GET /api/health
```

用途：

- 判断服务是否正常运行；
- 部署后可以被监控系统调用。

### 7.3 工具列表

```http
GET /api/tools
```

返回当前 Agent 可以使用的工具：

- `read_learning_plan`
- `search_knowledge`
- `safe_calculate`

### 7.4 普通 Agent 问答

```http
POST /api/agent/chat
```

请求体：

```json
{
  "question": "Day23 主要学习什么？",
  "use_tools": true
}
```

响应体：

```json
{
  "answer": "Agent 的回答内容",
  "source": "local-fallback",
  "used_tools": ["search_knowledge"]
}
```

字段说明：

- `answer`：Agent 回答。
- `source`：回答来源，可能是 `openai` 或 `local-fallback`。
- `used_tools`：本次回答使用过的工具。

### 7.5 流式 Agent 问答

```http
POST /api/agent/stream
```

这个接口返回 `text/event-stream`。

每个片段类似：

```text
data: {"delta": "这", "done": false}
```

最后一个片段：

```text
data: {"delta": "", "done": true}
```

流式输出适合聊天机器人页面，因为用户可以看到内容一点点出现，而不是等完整回答生成完。

## 8. 每个文件详细解释

### 8.1 requirements.txt

依赖说明：

- `fastapi`：后端 API 框架。
- `uvicorn`：启动 FastAPI 的服务器。
- `pydantic`：请求和响应模型校验。
- `python-dotenv`：读取 `.env` 配置。
- `rich`：美化命令行输出。
- `httpx`：`TestClient` 需要使用。
- `openai`：配置 API Key 后可以调用在线模型。

### 8.2 .env.example

配置示例文件。

重点配置：

- `OPENAI_API_KEY`：可选，有就用在线模型，没有就走本地模拟。
- `OPENAI_MODEL`：模型名称。
- `ALLOWED_ORIGINS`：允许跨域访问后端的前端地址。
- `RUN_SERVER`：是否允许 `python main.py` 直接启动服务。

### 8.3 config.py

配置中心。

它会读取 `.env`，并导出：

- 应用名称和版本；
- API 路由前缀；
- 文档地址；
- OpenAI 配置；
- CORS 配置；
- 本地知识库文件路径。

### 8.4 data/agent_knowledge.txt

本地知识库文件。

本地 Agent 会读取这个文件，回答和 Day23 相关的问题。

这是一个简化版 RAG 思路：

```text
用户问题 -> 搜索本地知识 -> 拼接回答
```

### 8.5 modules/schemas.py

接口数据模型文件。

包含：

- `AgentRequest`：Agent 请求模型。
- `AgentResponse`：Agent 响应模型。
- `StreamChunk`：流式片段模型。
- `ToolResult`：工具结果模型。
- `HealthStatus`：健康检查模型。
- `Message`：通用消息模型。
- `ErrorResponse`：统一错误模型。

### 8.6 modules/exceptions.py

自定义异常文件。

包含：

- `AgentAPIError`
- `EmptyQuestionError`
- `ToolExecutionError`

为什么要单独写异常？

因为真实项目中你会遇到很多错误：

- 用户输入为空；
- 工具调用失败；
- 模型返回异常；
- 数据库查询失败；
- 文件不存在；

统一异常可以让接口错误更稳定。

### 8.7 modules/tools.py

Agent 工具文件。

包含：

- `read_learning_plan()`：读取本地知识库。
- `search_knowledge()`：搜索本地知识库。
- `safe_calculate()`：安全计算简单表达式。
- `extract_math_expression()`：从用户问题中提取数学表达式。

这里模拟了 Agent 的工具调用能力。

### 8.8 modules/agent_service.py

Agent 核心服务。

它是 Day23 最关键的业务文件。

核心方法：

- `chat()`：普通问答。
- `stream_chat()`：流式问答。
- `_chat_with_openai()`：在线模型回答。
- `_chat_locally()`：本地模拟回答。

设计重点：

- 路由层不要写复杂业务逻辑。
- Agent 逻辑放到服务类里。
- 有 API Key 就尝试在线模型。
- 没有 API Key 就使用本地 fallback。
- 在线模型失败时自动降级，不让项目直接崩掉。

### 8.9 modules/routes.py

FastAPI 路由文件。

定义：

- `GET /api/health`
- `GET /api/tools`
- `POST /api/agent/chat`
- `POST /api/agent/stream`
- `GET /api/agent/example`

普通问答返回 JSON。

流式问答返回 `StreamingResponse`。

### 8.10 modules/app_factory.py

FastAPI 应用工厂。

负责：

- 创建 FastAPI 应用；
- 添加 CORS 中间件；
- 注册统一异常处理器；
- 注册首页接口；
- 挂载 Agent 路由。

### 8.11 main.py

项目主入口。

最重要的是：

```python
app = create_app()
```

Uvicorn 会通过 `main:app` 找到这个对象。

### 8.12 01_agent_api.py

演示普通 Agent API。

调用：

```http
POST /api/agent/chat
```

观察响应中的：

- `answer`
- `source`
- `used_tools`

### 8.13 02_streaming_response.py

演示流式响应。

它会调用：

```http
POST /api/agent/stream
```

并打印前几个流式片段。

### 8.14 03_error_handling.py

演示错误处理。

它会故意发送空问题：

```json
{
  "question": "   ",
  "use_tools": true
}
```

然后观察统一错误返回。

### 8.15 04_cors_config.py

演示 CORS 跨域配置。

它会发送一个 OPTIONS 预检请求，模拟前端跨域调用后端。

### 8.16 05_full_api_test.py

完整 API 测试脚本。

它会一次性调用：

- 首页
- 健康检查
- 工具列表
- 普通问答
- 错误处理
- 流式问答

## 9. 核心知识点

### 9.1 什么是接口化

接口化就是把原本只能自己运行的 Python 代码，包装成别人可以通过 HTTP 调用的服务。

脚本调用：

```text
python agent.py
```

API 调用：

```http
POST /api/agent/chat
```

### 9.2 为什么业务逻辑不要直接写在路由里

不推荐：

```python
@router.post("/agent/chat")
def chat(request):
    # 这里写一大堆 Agent 逻辑
```

推荐：

```python
@router.post("/agent/chat")
def chat(request):
    return agent_service.chat(request)
```

原因：

- 路由更清晰；
- 服务逻辑更容易测试；
- 后面复用更方便；
- 出问题更容易定位。

### 9.3 什么是流式响应

普通响应：

```text
等完整答案生成完 -> 一次性返回
```

流式响应：

```text
生成一点 -> 返回一点 -> 前端显示一点
```

聊天机器人常用流式响应，因为用户体验更好。

### 9.4 什么是 CORS

CORS 是跨域资源共享。

如果前端和后端地址不同，例如：

```text
前端：http://localhost:5173
后端：http://127.0.0.1:8000
```

浏览器会认为这是跨域请求。

后端必须明确允许这个前端地址访问，浏览器才会放行。

### 9.5 什么是统一错误处理

统一错误处理就是让所有错误都返回稳定结构。

不要这样：

```text
Traceback ...
```

应该这样：

```json
{
  "error": "EmptyQuestionError",
  "detail": "问题不能为空，请输入一个有效问题。"
}
```

## 10. 练习题

### 练习 1：让 Agent 不使用工具

要求：

- 调用 `/api/agent/chat`。
- 设置 `use_tools=false`。
- 观察 `used_tools` 是否为空。

答案位置：

- 已写在 `01_agent_api.py` 文件后面的注释中。

### 练习 2：理解流式接口 media_type

要求：

- 找到流式接口。
- 说明为什么使用 `text/event-stream`。

答案位置：

- 已写在 `02_streaming_response.py` 文件后面的注释中。

### 练习 3：新增一种自定义错误

要求：

- 在 `exceptions.py` 中新增异常类。
- 在业务代码中抛出。
- 观察统一错误处理器返回结果。

答案位置：

- 已写在 `03_error_handling.py` 文件后面的注释中。

### 练习 4：允许新的前端地址跨域访问

要求：

- 允许 `http://localhost:8080` 调用后端。

答案位置：

- 已写在 `04_cors_config.py` 文件后面的注释中。

### 练习 5：给完整测试加断言

要求：

- 在 `05_full_api_test.py` 中给接口调用添加 `assert`。

答案位置：

- 已写在 `05_full_api_test.py` 文件后面的注释中。

### 练习 6：直接测试 AgentService

要求：

- 不启动服务。
- 直接创建 `AgentService`。
- 调用 `chat()`。

答案位置：

- 已写在 `modules/agent_service.py` 文件后面的 `if __name__ == "__main__":` 中。

## 11. 常见错误

### 11.1 ModuleNotFoundError

推荐在 `D:\vscode项目\学习` 下运行脚本：

```powershell
& "C:\Program Files\Python314\python.exe" day23/01_agent_api.py
```

启动服务时进入 day23：

```powershell
cd day23
uvicorn main:app --reload
```

### 11.2 OPENAI_API_KEY 没有配置

这是正常的。

Day23 没有 Key 也能运行，会使用本地模拟 Agent。

如果你想用在线模型，复制 `.env.example` 为 `.env`，然后填写：

```env
OPENAI_API_KEY=你的 key
```

### 11.3 在线模型返回错误

如果 API Key、模型名、base_url 不匹配，可能会失败。

Day23 会自动降级到本地回答，并在回答最后提示在线调用失败。

### 11.4 前端调用接口跨域失败

检查 `.env` 中的：

```env
ALLOWED_ORIGINS=
```

把你的前端地址加入进去，然后重启服务。

## 12. 今日总结

Day23 你完成了从“脚本项目”到“API 项目”的关键一步。

现在你的 Agent 不只是自己能跑，而是可以通过 HTTP 被前端、移动端或其他系统调用。

后面的 Day24 部署上线，会继续沿着这个方向，把本地 API 项目变成可以运行在服务器上的项目。
