"""Day22 FastAPI 项目的配置文件。

这个文件负责统一管理项目中的配置项，例如：
1. API 项目名称
2. API 版本号
3. 路由前缀
4. 文档地址
5. 示例数据文件路径

把配置集中放在这里的好处是：
- 后面修改端口、路由前缀时，不需要到处找代码；
- main.py、modules/routes.py、modules/app_factory.py 都可以共用同一套配置；
- 真实项目中可以进一步区分开发环境、测试环境、生产环境。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


# 当前 day22 文件夹的绝对路径。
DAY22_DIR = Path(__file__).resolve().parent

# 读取 day22/.env 文件。如果文件不存在，也不会报错。
load_dotenv(DAY22_DIR / ".env")


# FastAPI 应用基础信息。
APP_NAME = os.getenv("APP_NAME", "Day22 FastAPI 入门 API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# API_PREFIX 表示所有业务接口的统一前缀。
# 例如 API_PREFIX=/api 时，items 接口就是 /api/items。
API_PREFIX = os.getenv("API_PREFIX", "/api")

# 服务启动地址和端口。
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

# FastAPI 自动生成文档的地址。
DOCS_URL = os.getenv("DOCS_URL", "/docs")
REDOC_URL = os.getenv("REDOC_URL", "/redoc")

# 示例数据文件路径。
DATA_FILE = DAY22_DIR / "data" / "items.json"

# 是否允许 python main.py 直接启动服务。
RUN_SERVER = os.getenv("RUN_SERVER", "0") == "1"
