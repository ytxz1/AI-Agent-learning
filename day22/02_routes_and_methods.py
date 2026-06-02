"""练习 02：路由和 HTTP 方法。

本练习会调用完整项目里的接口，演示：
- GET 查询
- POST 新增
- PUT 修改
- DELETE 删除

这些 HTTP 方法是后端 API 最常用的基础。
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from rich.console import Console

from modules.app_factory import create_app


console = Console()


def main() -> None:
    """运行路由和 HTTP 方法演示。"""

    app = create_app()
    client = TestClient(app)

    console.rule("[bold green]练习 02：路由和 HTTP 方法")

    list_response = client.get("/api/items")
    console.print("1. GET /api/items 查询列表：")
    console.print(list_response.json())

    create_response = client.post(
        "/api/items",
        json={
            "name": "FastAPI 路由练习资料",
            "description": "这条数据由 POST /api/items 创建。",
            "price": 16.8,
            "tags": ["fastapi", "post", "练习"],
        },
    )
    created_item = create_response.json()
    console.print("\n2. POST /api/items 新增资料：")
    console.print(created_item)

    item_id = created_item["id"]
    update_response = client.put(
        f"/api/items/{item_id}",
        json={"price": 12.0, "tags": ["fastapi", "put", "已修改"]},
    )
    console.print("\n3. PUT /api/items/{item_id} 修改资料：")
    console.print(update_response.json())

    delete_response = client.delete(f"/api/items/{item_id}")
    console.print("\n4. DELETE /api/items/{item_id} 删除资料：")
    console.print(delete_response.json())

    # 练习题答案：
    # 题目：如何添加一个 PATCH 接口只修改 price？
    # 如何添加：
    # 1. 到 modules/routes.py 中新增 @router.patch('/items/{item_id}/price')；
    # 2. 接收 item_id 路径参数和 price 请求体字段；
    # 3. 调用 db.update_item(item_id, ItemUpdate(price=price))；
    # 4. 设置 response_model=Item，让返回结构保持稳定。


if __name__ == "__main__":
    main()
