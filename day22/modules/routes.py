"""FastAPI 路由文件。

路由就是 URL 和 Python 函数之间的对应关系。
例如：
- GET /api/items       -> list_items()
- POST /api/items      -> create_item()
- GET /api/items/{id}  -> get_item()

本文件集中管理业务接口，main.py 只负责创建和启动应用。
"""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query, status


# 兼容两种运行方式：
# 1. python main.py
# 2. python day22/modules/routes.py
DAY22_DIR = Path(__file__).resolve().parents[1]
if str(DAY22_DIR) not in sys.path:
    sys.path.insert(0, str(DAY22_DIR))

from config import API_PREFIX, APP_NAME, APP_VERSION, DATA_FILE

try:
    from .fake_db import FakeItemDB
    from .schemas import HealthStatus, Item, ItemCreate, ItemUpdate, Message, SearchResult
except ImportError:
    from fake_db import FakeItemDB
    from schemas import HealthStatus, Item, ItemCreate, ItemUpdate, Message, SearchResult


# 创建路由对象，prefix 表示本文件下的接口都以 /api 开头。
router = APIRouter(prefix=API_PREFIX, tags=["学习资料 API"])

# 创建一个全局内存数据库实例。
db = FakeItemDB(DATA_FILE)


@router.get("/health", response_model=HealthStatus)
def health_check() -> HealthStatus:
    """健康检查接口。

    真实项目部署上线后，经常用这个接口判断服务是否还活着。
    """

    return HealthStatus(
        status="ok",
        app_name=APP_NAME,
        version=APP_VERSION,
    )


@router.get("/items", response_model=list[Item])
def list_items(
    skip: int = Query(default=0, ge=0, description="跳过前几条数据。"),
    limit: int = Query(default=10, ge=1, le=50, description="最多返回几条数据。"),
    keyword: str | None = Query(default=None, description="按关键词搜索名称、描述和标签。"),
) -> list[Item]:
    """查询资料列表。

    这里演示了 Query 查询参数：
    /api/items?skip=0&limit=2&keyword=python
    """

    return db.list_items(skip=skip, limit=limit, keyword=keyword)


@router.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> Item:
    """创建资料。

    payload 会自动从请求体 JSON 中解析，并被 ItemCreate 校验。
    """

    return db.create_item(payload)


@router.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    """根据 id 查询资料。

    item_id 是路径参数，也就是 URL 里面的一部分。
    """

    item = db.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"没有找到 id={item_id} 的资料")
    return item


@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, payload: ItemUpdate) -> Item:
    """更新资料。

    PUT /api/items/1
    请求体可以只传需要修改的字段。
    """

    item = db.update_item(item_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail=f"没有找到 id={item_id} 的资料")
    return item


@router.delete("/items/{item_id}", response_model=Message)
def delete_item(item_id: int) -> Message:
    """删除资料。"""

    deleted = db.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"没有找到 id={item_id} 的资料")
    return Message(message=f"id={item_id} 的资料已删除")


@router.get("/search", response_model=SearchResult)
def search_items(
    q: str = Query(..., min_length=1, description="搜索关键词，不能为空。"),
    limit: int = Query(default=5, ge=1, le=20, description="最多返回几条搜索结果。"),
) -> SearchResult:
    """搜索资料。

    这个接口专门用来演示响应模型 SearchResult。
    """

    items = db.list_items(limit=limit, keyword=q)
    return SearchResult(query=q, count=len(items), items=items)


if __name__ == "__main__":
    # 练习题答案 3：
    # 如何确认路由对象里到底注册了哪些接口？
    # 答案：直接遍历 router.routes，查看 path 和 methods。
    print("练习题答案 3：当前 routes.py 注册的接口如下")
    for route in router.routes:
        methods = ",".join(sorted(route.methods or []))
        print(f"{methods:10s} {route.path}")
