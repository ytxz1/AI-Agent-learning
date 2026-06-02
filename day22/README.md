# Day22 - FastAPI 入门

Day22 的主题是 **FastAPI 入门**。这一章开始把前面做过的 Agent、RAG、问答系统从“脚本项目”逐步变成“可以被别人调用的后端 API”。

按照学习计划表，Day22 的任务是：

- 学习 FastAPI 基础
- 学习路由和 HTTP 方法
- 学习路径参数、查询参数、请求体参数
- 学习响应模型 `response_model`
- 学习自动生成接口文档
- 实践：创建第一个 API

本项目不需要 OpenAI API Key。Day22 主要学习 Web API 基础，等后面 Day23 再把 Agent 接口化时，才会更自然地接入大模型能力。

## 1. 你今天要掌握什么

学完 Day22，你应该能做到：

- 知道 FastAPI 是什么，以及它为什么适合做 AI Agent 后端。
- 能写出一个最小的 FastAPI 应用。
- 能定义 `GET`、`POST`、`PUT`、`DELETE` 接口。
- 能区分路径参数、查询参数、请求体参数。
- 能用 Pydantic 模型校验请求数据。
- 能用 `response_model` 控制接口响应结构。
- 能打开 `/docs` 自动文档并测试接口。

## 2. 为什么 AI Agent 项目需要 FastAPI

前面几天我们写的项目，大多是命令行脚本，例如：

- 运行一个 RAG 问答脚本
- 运行一个文档加载脚本
- 运行一个 Agent 调用工具的脚本

这些脚本适合学习和调试，但如果你想让别人使用你的项目，就需要把能力包装成 API。

例如：

- 前端页面想调用你的 RAG 问答系统
- 手机 App 想调用你的 Agent
- 企业内部系统想调用你的文档问答接口
- 你想把项目部署到服务器上给别人访问

这时候就需要 FastAPI 这样的后端框架。

## 3. 项目结构

```text
day22/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── main.py
├── 01_fastapi_basics.py
├── 02_routes_and_methods.py
├── 03_request_params.py
├── 04_response_models.py
├── 05_auto_docs.py
├── data/
│   └── items.json
├── modules/
│   ├── __init__.py
│   ├── schemas.py
│   ├── fake_db.py
│   ├── routes.py
│   └── app_factory.py
└── output/
```

## 4. 安装依赖

在 `D:\vscode项目\学习` 下运行：

```powershell
pip install -r day22/requirements.txt
```

如果你使用的是指定 Python 版本，也可以运行：

```powershell
& "C:\Program Files\Python314\python.exe" -m pip install -r day22/requirements.txt
```

## 5. 运行方式

### 5.1 运行学习脚本

这些脚本会用 `TestClient` 模拟请求，不需要启动服务器：

```powershell
& "C:\Program Files\Python314\python.exe" day22/01_fastapi_basics.py
& "C:\Program Files\Python314\python.exe" day22/02_routes_and_methods.py
& "C:\Program Files\Python314\python.exe" day22/03_request_params.py
& "C:\Program Files\Python314\python.exe" day22/04_response_models.py
& "C:\Program Files\Python314\python.exe" day22/05_auto_docs.py
```

### 5.2 查看主项目说明

```powershell
& "C:\Program Files\Python314\python.exe" day22/main.py
```

默认情况下，`main.py` 只打印启动说明，不会一直占用终端。

### 5.3 真正启动 API 服务

进入 day22 文件夹：

```powershell
cd day22
uvicorn main:app --reload
```

启动后访问：

- Swagger 文档：http://127.0.0.1:8000/docs
- ReDoc 文档：http://127.0.0.1:8000/redoc
- 首页接口：http://127.0.0.1:8000/
- 健康检查：http://127.0.0.1:8000/api/health

## 6. 每个文件详细解释

### 6.1 requirements.txt

这个文件记录 Day22 需要安装的 Python 依赖。

包含：

- `fastapi`：后端 API 框架。
- `uvicorn`：ASGI 服务器，用来启动 FastAPI。
- `pydantic`：数据校验和模型定义工具。
- `python-dotenv`：读取 `.env` 配置文件。
- `rich`：让命令行输出更清楚。
- `httpx`：FastAPI 的 `TestClient` 底层需要用到它。

### 6.2 .env.example

这是环境变量示例文件。

你可以把它复制成 `.env`，然后修改配置。

例如你想把接口文档地址从 `/docs` 改成 `/api-docs`，可以在 `.env` 中写：

```env
DOCS_URL=/api-docs
```

### 6.3 config.py

这是配置中心。

它负责读取：

- `APP_NAME`
- `APP_VERSION`
- `API_PREFIX`
- `HOST`
- `PORT`
- `DOCS_URL`
- `REDOC_URL`
- `DATA_FILE`
- `RUN_SERVER`

为什么要有配置文件？

因为真实项目里，配置会越来越多。如果都写在 `main.py` 或 `routes.py` 里面，后面会很乱。

### 6.4 data/items.json

这是示例数据文件。

项目启动时，`FakeItemDB` 会从这里读取初始资料。

注意：本项目使用的是内存数据库。新增、修改、删除的数据只在当前程序运行期间有效，不会写回 `items.json`。

### 6.5 modules/schemas.py

这是 Pydantic 数据模型文件。

主要模型：

- `ItemBase`：公共字段，包括 `name`、`description`、`price`、`tags`。
- `ItemCreate`：创建资料时使用，不包含 `id`。
- `ItemUpdate`：更新资料时使用，所有字段都是可选的。
- `Item`：接口返回时使用，包含 `id` 和 `is_active`。
- `Message`：通用消息响应。
- `HealthStatus`：健康检查响应。
- `SearchResult`：搜索接口响应。

这里最重要的是理解：**Schema 就是接口的数据契约**。

### 6.6 modules/fake_db.py

这是模拟数据库。

它提供：

- `list_items()`：查询列表。
- `get_item()`：根据 id 查询单条数据。
- `create_item()`：新增数据。
- `update_item()`：更新数据。
- `delete_item()`：删除数据。

为什么不用真实数据库？

因为 Day22 的重点不是数据库，而是 FastAPI。先用内存数据库，可以让你更专注理解 API 的基本结构。

### 6.7 modules/routes.py

这是路由文件，也是 Day22 最核心的文件之一。

它定义了这些接口：

| 方法 | 路径 | 作用 |
|---|---|---|
| GET | `/api/health` | 健康检查 |
| GET | `/api/items` | 查询资料列表 |
| POST | `/api/items` | 创建资料 |
| GET | `/api/items/{item_id}` | 查询单条资料 |
| PUT | `/api/items/{item_id}` | 更新资料 |
| DELETE | `/api/items/{item_id}` | 删除资料 |
| GET | `/api/search` | 搜索资料 |

这里你会学到：

- `@router.get()` 是定义 GET 接口。
- `@router.post()` 是定义 POST 接口。
- `@router.put()` 是定义 PUT 接口。
- `@router.delete()` 是定义 DELETE 接口。
- `response_model=Item` 表示响应必须符合 `Item` 模型。
- `Query()` 可以给查询参数加限制和说明。
- `HTTPException` 可以返回错误状态码。

### 6.8 modules/app_factory.py

这是应用工厂文件。

它提供一个函数：

```python
create_app()
```

这个函数负责：

- 创建 FastAPI 应用。
- 设置标题、版本、描述。
- 设置 `/docs` 和 `/redoc`。
- 注册首页接口 `/`。
- 挂载 `routes.py` 里的业务路由。

### 6.9 main.py

这是主入口文件。

里面最重要的一行是：

```python
app = create_app()
```

当你运行：

```powershell
uvicorn main:app --reload
```

Uvicorn 就会找到 `main.py` 里的 `app` 对象，然后启动服务。

### 6.10 01_fastapi_basics.py

这个文件演示最小 FastAPI 应用。

它包含：

- 创建 `FastAPI()` 对象。
- 定义 `/` 首页接口。
- 定义 `/health` 健康检查接口。
- 使用 `TestClient` 模拟请求。

你不需要启动服务器，也能看到接口返回结果。

### 6.11 02_routes_and_methods.py

这个文件演示 HTTP 方法。

它会依次调用：

- `GET /api/items`
- `POST /api/items`
- `PUT /api/items/{item_id}`
- `DELETE /api/items/{item_id}`

这就是最常见的 CRUD 流程。

CRUD 的意思是：

- Create：创建
- Read：读取
- Update：更新
- Delete：删除

### 6.12 03_request_params.py

这个文件演示三类请求参数。

路径参数：

```text
/api/items/1
```

查询参数：

```text
/api/items?skip=0&limit=2&keyword=python
```

请求体参数：

```json
{
  "name": "请求体参数练习",
  "description": "这条数据通过 JSON 请求体提交。",
  "price": 8.8,
  "tags": ["body", "json"]
}
```

### 6.13 04_response_models.py

这个文件演示 `response_model`。

重点是：函数返回的数据里有 `password`，但是 `response_model=PublicUser` 不包含 `password`，所以 FastAPI 会自动过滤掉它。

这在真实项目里非常重要，因为你不能把密码、Token、内部字段随便返回给前端。

### 6.14 05_auto_docs.py

这个文件演示自动文档。

它会读取 `/openapi.json`，并打印当前项目中自动生成的接口路径。

你启动服务后，也可以直接打开：

```text
http://127.0.0.1:8000/docs
```

## 7. 核心知识点

### 7.1 FastAPI 最小结构

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}
```

这就是一个最小 API。

### 7.2 路由是什么

路由就是 URL 和函数的绑定。

```python
@app.get("/hello")
def hello():
    return {"message": "hello"}
```

访问 `/hello` 时，FastAPI 就会执行 `hello()` 函数。

### 7.3 HTTP 方法是什么

常见方法：

| 方法 | 用途 |
|---|---|
| GET | 查询数据 |
| POST | 新增数据 |
| PUT | 整体或部分更新数据 |
| PATCH | 局部更新数据 |
| DELETE | 删除数据 |

### 7.4 路径参数

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
```

访问 `/items/3` 时，`item_id` 就是 `3`。

### 7.5 查询参数

```python
@app.get("/items")
def list_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

访问：

```text
/items?skip=10&limit=5
```

FastAPI 会自动把参数解析成整数。

### 7.6 请求体参数

```python
class ItemCreate(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(payload: ItemCreate):
    return payload
```

POST 请求发送 JSON 时，FastAPI 会自动校验字段。

### 7.7 response_model

```python
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    return item
```

这表示接口最终返回的数据必须符合 `Item` 模型。

## 8. 练习题

### 练习 1：新增 /about 接口

要求：

- 在 `01_fastapi_basics.py` 的 `create_basic_app()` 中新增 `/about`。
- 返回项目说明。

答案位置：

- 已写在 `01_fastapi_basics.py` 文件后面的注释中。

### 练习 2：测试模拟数据库新增数据

要求：

- 不启动 FastAPI。
- 直接创建 `FakeItemDB`。
- 新增一条数据。
- 打印新增结果。

答案位置：

- 已写在 `modules/fake_db.py` 文件后面的 `if __name__ == "__main__":` 中。

### 练习 3：查看当前注册了哪些路由

要求：

- 打印 `routes.py` 中注册的所有接口路径。

答案位置：

- 已写在 `modules/routes.py` 文件后面的 `if __name__ == "__main__":` 中。

### 练习 4：确认 create_app() 创建成功

要求：

- 调用 `create_app()`。
- 打印应用标题。
- 打印路由数量。

答案位置：

- 已写在 `modules/app_factory.py` 文件后面的 `if __name__ == "__main__":` 中。

### 练习 5：修改自动文档地址

要求：

- 把 Swagger 文档地址从 `/docs` 改成 `/api-docs`。

答案位置：

- 已写在 `05_auto_docs.py` 文件后面的注释中。

## 9. 常见错误

### 9.1 ModuleNotFoundError

如果你看到：

```text
ModuleNotFoundError: No module named 'modules'
```

优先确认你是不是在正确目录运行。

推荐在 `D:\vscode项目\学习` 下运行：

```powershell
& "C:\Program Files\Python314\python.exe" day22/01_fastapi_basics.py
```

如果要启动服务，推荐先进入 day22：

```powershell
cd day22
uvicorn main:app --reload
```

### 9.2 fastapi 未安装

如果看到：

```text
ModuleNotFoundError: No module named 'fastapi'
```

运行：

```powershell
pip install -r day22/requirements.txt
```

### 9.3 uvicorn 不是内部或外部命令

可以改用：

```powershell
python -m uvicorn main:app --reload
```

或者：

```powershell
& "C:\Program Files\Python314\python.exe" -m uvicorn main:app --reload
```

### 9.4 为什么 python main.py 没有启动服务

这是故意设计的。

默认 `RUN_SERVER=0`，所以 `python main.py` 只打印说明，不会占住终端。

你可以用更推荐的方式启动：

```powershell
uvicorn main:app --reload
```

也可以复制 `.env.example` 为 `.env`，然后设置：

```env
RUN_SERVER=1
```

再运行：

```powershell
python main.py
```

## 10. 今日总结

Day22 你完成了第一个 FastAPI API 项目。

你现在已经具备把 Python 脚本变成后端接口的基础能力。后面 Day23 就可以把 Agent、RAG、文档问答系统进一步接口化，让它真正变成一个可以被前端或外部系统调用的项目。
