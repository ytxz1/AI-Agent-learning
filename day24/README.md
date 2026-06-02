# Day24 - 部署上线

Day24 的主题是 **部署上线**。

前面 Day22 和 Day23，我们已经把项目做成了 FastAPI API。Day24 要解决的问题是：如何让这个 API 不只是本地能跑，而是可以被打包、运行、部署到服务器。

按照学习计划表，Day24 的任务是：

- Docker 基础
- 构建镜像
- 运行容器
- 部署到云服务器
- 实践：部署你的项目

## 1. 今日目标

学完 Day24，你应该能做到：

- 知道 Docker 镜像和容器的区别。
- 能看懂一个基础 `Dockerfile`。
- 能用 Dockerfile 构建 FastAPI 镜像。
- 能用 `docker run` 或 `docker compose` 启动 API。
- 能理解为什么容器内服务要监听 `0.0.0.0`。
- 能写健康检查接口 `/api/health`。
- 能准备一份部署到云服务器的命令清单。

## 2. Day24 是否需要 API Key

不需要。

Day24 的重点是部署，不是大模型调用。真实项目中如果需要 API Key，应该通过 `.env` 或服务器环境变量传入，而不是写死在代码里。

## 3. 项目结构

```text
day24/
├── README.md
├── requirements.txt
├── .env.example
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── config.py
├── main.py
├── 01_docker_basics.py
├── 02_build_image_plan.py
├── 03_container_runtime_check.py
├── 04_deployment_config.py
├── 05_health_check.py
├── modules/
│   ├── __init__.py
│   ├── schemas.py
│   ├── deployment_info.py
│   ├── routes.py
│   └── app_factory.py
├── scripts/
│   └── deploy_commands.md
└── output/
```

## 4. 安装依赖

在 `D:\vscode项目\学习` 下运行：

```powershell
pip install -r day24/requirements.txt
```

指定 Python 版本：

```powershell
& "C:\Program Files\Python314\python.exe" -m pip install -r day24/requirements.txt
```

## 5. 运行学习脚本

这些脚本不需要 Docker 也能运行：

```powershell
& "C:\Program Files\Python314\python.exe" day24/01_docker_basics.py
& "C:\Program Files\Python314\python.exe" day24/02_build_image_plan.py
& "C:\Program Files\Python314\python.exe" day24/03_container_runtime_check.py
& "C:\Program Files\Python314\python.exe" day24/04_deployment_config.py
& "C:\Program Files\Python314\python.exe" day24/05_health_check.py
```

## 6. 本地启动 API

进入 day24：

```powershell
cd day24
uvicorn main:app --reload
```

启动后访问：

- Swagger 文档：http://127.0.0.1:8000/docs
- ReDoc 文档：http://127.0.0.1:8000/redoc
- 健康检查：http://127.0.0.1:8000/api/health
- 部署信息：http://127.0.0.1:8000/api/deploy/info
- 部署检查清单：http://127.0.0.1:8000/api/deploy/checklist

## 7. Docker 运行方式

如果你的电脑已经安装 Docker，可以运行：

```powershell
cd day24
docker compose up --build
```

后台运行：

```powershell
docker compose up -d --build
```

查看容器状态：

```powershell
docker compose ps
```

查看日志：

```powershell
docker compose logs -f
```

停止容器：

```powershell
docker compose down
```

## 8. 每个文件详细解释

### 8.1 requirements.txt

记录项目运行需要的依赖。

包含：

- `fastapi`：API 框架。
- `uvicorn`：运行 FastAPI 的服务器。
- `pydantic`：数据模型校验。
- `python-dotenv`：读取 `.env` 配置。
- `rich`：美化命令行输出。
- `httpx`：FastAPI `TestClient` 需要。

### 8.2 .env.example

环境变量示例文件。

部署时不要直接把敏感配置写进代码，而应该放到 `.env` 或服务器环境变量里。

重点字段：

- `HOST=0.0.0.0`：容器部署必须监听所有网卡。
- `PORT=8000`：服务端口。
- `ENVIRONMENT=local`：当前运行环境。
- `RUN_SERVER=0`：默认不让 `python main.py` 一直占用终端。

### 8.3 .dockerignore

告诉 Docker 构建镜像时忽略哪些文件。

例如：

- `__pycache__/`
- `.env`
- `.venv/`
- `output/`
- `.git/`

为什么要忽略 `.env`？

因为 `.env` 可能包含 API Key、数据库密码等敏感信息，不应该被打进镜像。

### 8.4 Dockerfile

Dockerfile 是构建镜像的说明书。

核心流程：

```text
选择 Python 基础镜像
设置环境变量
设置工作目录
复制 requirements.txt
安装依赖
复制项目代码
暴露端口
启动 uvicorn
```

最关键的一点：

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

容器里必须监听 `0.0.0.0`，否则外部访问不到。

### 8.5 docker-compose.yml

Docker Compose 用来管理容器运行配置。

它做了几件事：

- 构建当前目录的镜像；
- 创建名为 `day24-deploy-api` 的容器；
- 映射端口 `8000:8000`；
- 读取 `.env`；
- 设置 `ENVIRONMENT=docker`；
- 配置容器自动重启；
- 配置健康检查。

### 8.6 config.py

配置中心。

负责读取：

- 应用名称；
- 版本；
- 路由前缀；
- 服务地址；
- 端口；
- 文档地址；
- 当前环境；
- 服务名称。

还提供：

```python
is_production()
```

用于判断是否生产环境。

### 8.7 modules/schemas.py

Pydantic 模型文件。

包含：

- `Message`：通用消息响应。
- `HealthStatus`：健康检查响应。
- `DeploymentInfo`：部署信息响应。
- `DeployCheckItem`：部署检查项。

### 8.8 modules/deployment_info.py

部署信息工具模块。

包含：

- `get_deployment_info()`：返回当前部署信息。
- `get_deploy_checklist()`：返回部署前检查清单。

检查清单会确认：

- Dockerfile 是否存在；
- docker-compose.yml 是否存在；
- requirements.txt 是否存在；
- .env.example 是否存在；
- main.py 是否存在；
- HOST 是否是 `0.0.0.0`。

### 8.9 modules/routes.py

部署检查 API 路由。

定义：

- `GET /api/health`
- `GET /api/deploy/info`
- `GET /api/deploy/checklist`

这些接口上线后很实用。

例如你可以用浏览器打开：

```text
http://服务器IP:8000/api/health
```

如果返回 `status=ok`，说明服务基本正常。

### 8.10 modules/app_factory.py

FastAPI 应用工厂。

负责：

- 创建 FastAPI 应用；
- 注册首页；
- 注册部署检查路由；
- 在生产环境关闭 `/docs` 和 `/redoc`。

为什么生产环境可能关闭文档？

因为公开文档可能暴露接口结构。学习项目可以打开，公开生产项目建议加权限或关闭。

### 8.11 main.py

项目主入口。

关键代码：

```python
app = create_app()
```

Uvicorn 会通过 `main:app` 找到这个应用。

### 8.12 01_docker_basics.py

解释 Docker 基础概念。

你会看到：

- 镜像；
- 容器；
- Dockerfile；
- 端口映射；
- 环境变量。

### 8.13 02_build_image_plan.py

读取并解释 Dockerfile。

它会逐行说明：

- `FROM` 是什么；
- `ENV` 是什么；
- `WORKDIR` 是什么；
- `COPY` 是什么；
- `RUN` 是什么；
- `EXPOSE` 是什么；
- `CMD` 是什么。

### 8.14 03_container_runtime_check.py

解释容器运行命令。

包括：

- `docker compose up --build`
- `docker compose ps`
- `docker compose logs -f`
- `docker compose down`

### 8.15 04_deployment_config.py

打印当前部署配置和检查清单。

它能帮你确认：

- 服务名；
- 环境；
- HOST；
- PORT；
- 文档地址；
- 部署文件是否齐全。

### 8.16 05_health_check.py

调用健康检查接口和部署信息接口。

它会测试：

- `/api/health`
- `/api/deploy/info`
- `/api/deploy/checklist`

### 8.17 scripts/deploy_commands.md

部署命令速查表。

里面整理了：

- 本地启动命令；
- Docker 构建命令；
- Docker 运行命令；
- Docker Compose 命令；
- 服务器部署基本流程。

## 9. 核心知识点

### 9.1 镜像和容器

镜像可以理解为“项目安装包”。

容器可以理解为“安装包运行起来后的程序”。

一个镜像可以启动多个容器。

### 9.2 Dockerfile 是什么

Dockerfile 是镜像构建说明书。

你告诉 Docker：

- 用什么基础环境；
- 复制哪些文件；
- 安装哪些依赖；
- 暴露哪个端口；
- 启动时执行什么命令。

### 9.3 为什么要用 0.0.0.0

本地开发时：

```text
127.0.0.1
```

通常没问题。

但是容器里如果只监听 `127.0.0.1`，服务只能在容器内部访问，外部访问不到。

所以 Docker 部署时要用：

```text
0.0.0.0
```

### 9.4 端口映射是什么意思

```yaml
ports:
  - "8000:8000"
```

左边是宿主机端口，右边是容器端口。

意思是：

```text
访问电脑或服务器的 8000 端口 -> 转发到容器的 8000 端口
```

### 9.5 健康检查为什么重要

部署上线后，你不能只靠“感觉服务应该在跑”。

健康检查接口可以让你快速确认：

- 服务是否启动；
- 路由是否可访问；
- 容器是否健康；
- 服务器是否能访问 API。

## 10. 云服务器部署基本流程

假设你已经把代码上传到服务器。

服务器上安装 Docker 后，常见流程是：

```powershell
git pull
cd day24
cp .env.example .env
docker compose up -d --build
docker compose ps
docker compose logs -f
```

然后访问：

```text
http://服务器IP:8000/api/health
```

如果云服务器有安全组，还要开放 8000 端口。

## 11. 练习题

### 练习 1：镜像和容器有什么区别

要求：

- 用自己的话解释 image 和 container。

答案位置：

- 已写在 `01_docker_basics.py` 文件后面的注释中。

### 练习 2：为什么先复制 requirements.txt

要求：

- 解释 Dockerfile 中为什么先 `COPY requirements.txt`，再 `COPY . .`。

答案位置：

- 已写在 `02_build_image_plan.py` 文件后面的注释中。

### 练习 3：为什么容器监听 0.0.0.0

要求：

- 解释 `127.0.0.1` 和 `0.0.0.0` 在容器中的区别。

答案位置：

- 已写在 `03_container_runtime_check.py` 文件后面的注释中。

### 练习 4：生产环境是否一定开放 /docs

要求：

- 思考公开 API 文档的风险。

答案位置：

- 已写在 `04_deployment_config.py` 文件后面的注释中。

### 练习 5：给健康检查加断言

要求：

- 在 `05_health_check.py` 中给健康检查加断言。

答案位置：

- 已写在 `05_health_check.py` 文件后面的注释中。

### 练习 6：查看部署信息

要求：

- 不启动 API，直接运行模块查看部署信息。

答案位置：

- 已写在 `modules/deployment_info.py` 文件后面的 `if __name__ == "__main__":` 中。

## 12. 常见错误

### 12.1 Docker 未安装

如果运行：

```powershell
docker --version
```

提示找不到命令，说明 Docker 没装或没启动。

先学习 Day24 的 Python 脚本也没关系，它们不依赖 Docker。

### 12.2 docker compose up 后访问不到

优先检查：

- 容器是否启动；
- 端口是否映射；
- FastAPI 是否监听 `0.0.0.0`；
- 云服务器安全组是否开放 8000；
- 防火墙是否拦截。

### 12.3 .env 不存在

`docker-compose.yml` 使用了：

```yaml
env_file:
  - .env
```

所以 Docker Compose 启动前建议复制：

```powershell
copy .env.example .env
```

### 12.4 生产环境看不到 /docs

如果设置：

```env
ENVIRONMENT=production
```

本项目会关闭 `/docs` 和 `/redoc`。

这是为了模拟生产环境中保护接口文档的做法。

## 13. 今日总结

Day24 你完成了从“本地 API 项目”到“可部署项目”的关键一步。

你现在不只是能写 FastAPI，还知道如何：

- 准备 Dockerfile；
- 构建镜像；
- 运行容器；
- 配置 docker-compose；
- 写健康检查接口；
- 准备服务器部署命令。

后面的 Day25 会进入前端界面，把已经部署或可调用的 API 变成用户能直接操作的 Web 页面。
