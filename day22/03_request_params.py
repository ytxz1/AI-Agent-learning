"""练习 03：请求参数。

FastAPI 中常见参数有三类：
1. 路径参数：/api/items/{item_id}
2. 查询参数：/api/items?skip=0&limit=2
3. 请求体参数：POST /api/items 时提交的 JSON

本练习会把三类参数都跑一遍。
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from rich.console import Console

from modules.app_factory import create_app


console = Console()


def main() -> None:
    """运行请求参数演示。"""

    client = TestClient(create_app())

    console.rule("[bold green]练习 03：请求参数")

    path_response = client.get("/api/items/1")
    console.print("1. 路径参数 item_id=1：")
    console.print(path_response.json())

    query_response = client.get("/api/items", params={"skip": 0, "limit": 2, "keyword": "python"})
    console.print("\n2. 查询参数 skip=0 limit=2 keyword=python：")
    console.print(query_response.json())

    body_response = client.post(
        "/api/items",
        json={
            "name": "请求体参数练习",
            "description": "这条数据通过 JSON 请求体提交。",
            "price": 8.8,
            "tags": ["body", "json"],
        },
    )
    console.print("\n3. 请求体参数 JSON：")
    console.print(body_response.json())

    # 练习题答案：
    # 题目：如何限制 limit 最大不能超过 50？
    # 如何添加：
    # 在 modules/routes.py 的 list_items 函数中写：
    # limit: int = Query(default=10, ge=1, le=50, description='最多返回几条数据。')
    # 其中 le=50 表示 less than or equal，小于等于 50。


if __name__ == "__main__":
    main()
