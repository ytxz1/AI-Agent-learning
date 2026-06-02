"""Day22 FastAPI 入门项目的模块包。

把核心代码放到 modules 文件夹里，是为了让主程序 main.py 更干净：
- schemas.py 负责数据结构；
- fake_db.py 负责模拟数据库；
- routes.py 负责接口路由；
- app_factory.py 负责创建 FastAPI 应用。
"""

from .app_factory import create_app
from .fake_db import FakeItemDB
from .schemas import HealthStatus, Item, ItemCreate, ItemUpdate, Message, SearchResult

__all__ = [
    "create_app",
    "FakeItemDB",
    "HealthStatus",
    "Item",
    "ItemCreate",
    "ItemUpdate",
    "Message",
    "SearchResult",
]
