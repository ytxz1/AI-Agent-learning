# Day24 Dockerfile
# 作用：把 FastAPI 项目打包成一个可以运行的 Docker 镜像。

# 1. 选择基础镜像。
# python:3.12-slim 体积较小，适合部署 Python Web API。
FROM python:3.12-slim

# 2. 设置环境变量。
# PYTHONDONTWRITEBYTECODE=1：不生成 .pyc 文件。
# PYTHONUNBUFFERED=1：让日志实时输出，方便容器中查看。
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. 设置容器内工作目录。
WORKDIR /app

# 4. 先复制 requirements.txt。
# 这样 Docker 构建时可以缓存依赖安装层，代码变了也不必每次重新装依赖。
COPY requirements.txt .

# 5. 安装依赖。
RUN pip install --no-cache-dir -r requirements.txt

# 6. 复制项目代码到容器。
COPY . .

# 7. 暴露容器端口。
EXPOSE 8000

# 8. 容器启动命令。
# 这里必须使用 0.0.0.0，否则容器外部访问不到服务。
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
