# Day24 常用部署命令

这个文件不是必须执行的脚本，而是部署时常用命令的速查表。

## 本地启动

```powershell
cd day24
uvicorn main:app --reload
```

## Docker 构建镜像

```powershell
cd day24
docker build -t day24-deploy-api .
```

## Docker 运行容器

```powershell
docker run --name day24-deploy-api -p 8000:8000 day24-deploy-api
```

## Docker Compose 启动

```powershell
cd day24
docker compose up --build
```

## 后台启动

```powershell
docker compose up -d --build
```

## 查看日志

```powershell
docker compose logs -f
```

## 停止服务

```powershell
docker compose down
```

## 服务器部署基本流程

```powershell
git pull
cd day24
cp .env.example .env
docker compose up -d --build
docker compose ps
docker compose logs -f
```
