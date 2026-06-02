"""练习 04：响应模型 response_model。

response_model 的作用：
1. 约束接口返回的数据结构；
2. 过滤掉不应该暴露给前端的字段；
3. 自动生成更清楚的接口文档；
4. 让前后端协作时更容易知道返回值格式。
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from rich.console import Console


console = Console()


class PublicUser(BaseModel):
    """允许返回给前端的用户信息。"""

    id: int
    username: str


def create_response_model_app() -> FastAPI:
    """创建一个专门演示 response_model 的小应用。"""

    app = FastAPI(title="Day22 练习 04：响应模型")

    @app.get("/users/me", response_model=PublicUser)
    def get_current_user() -> dict[str, object]:
        """返回当前用户。

        注意：函数返回值里故意放了 password。
        但 response_model=PublicUser 不包含 password，
        所以 FastAPI 最终返回给客户端时会自动过滤 password。
        """

        return {
            "id": 1,
            "username": "xiaoming",
            "password": "这个字段不会被返回给前端",
        }

    return app


def main() -> None:
    """运行响应模型演示。"""

    client = TestClient(create_response_model_app())
    response = client.get("/users/me")

    console.rule("[bold green]练习 04：响应模型")
    console.print("接口返回：", response.json())
    console.print("可以看到 password 字段已经被 response_model 过滤掉了。")

    # 练习题答案：
    # 题目：如果想让接口返回 email，应该怎么添加？
    # 如何添加：
    # 1. 在 PublicUser 中新增 email: str；
    # 2. 在 get_current_user() 的返回字典里新增 "email": "xiaoming@example.com"；
    # 3. 再运行脚本，返回结果就会包含 email。


if __name__ == "__main__":
    main()
