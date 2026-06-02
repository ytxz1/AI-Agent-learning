"""Pydantic 数据模型，也叫 Schema。

FastAPI 中的 Schema 主要有三个作用：
1. 校验请求数据：用户传过来的 JSON 是否符合要求；
2. 控制响应结构：接口返回给前端的数据长什么样；
3. 自动生成文档：/docs 页面会根据这里的模型展示字段说明。

本文件里的模型会被 routes.py 引用。
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """商品/学习资料的公共字段。

    ItemCreate、Item 都会继承这些字段，避免重复写代码。
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="资料名称，不能为空，最多 50 个字符。",
        examples=["FastAPI 入门笔记"],
    )
    description: str = Field(
        ...,
        min_length=1,
        description="资料说明，告诉用户这个资料是做什么的。",
        examples=["包含路由、请求参数、响应模型和自动文档。"],
    )
    price: float = Field(
        ...,
        ge=0,
        description="价格，必须大于等于 0。",
        examples=[29.9],
    )
    tags: list[str] = Field(
        default_factory=list,
        description="标签列表，用于搜索和分类。",
        examples=[["fastapi", "api", "python"]],
    )


class ItemCreate(ItemBase):
    """创建资料时，客户端需要提交的数据。

    注意：创建时不需要传 id，因为 id 应该由后端生成。
    """


class ItemUpdate(BaseModel):
    """更新资料时允许提交的数据。

    所有字段都是可选的，这样用户只想改 name 或 price 时，不用把整条数据都传一遍。
    """

    name: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None, min_length=1)
    price: float | None = Field(default=None, ge=0)
    tags: list[str] | None = None
    is_active: bool | None = None


class Item(ItemBase):
    """接口返回给客户端的完整资料结构。"""

    id: int = Field(..., description="后端生成的唯一编号。")
    is_active: bool = Field(default=True, description="资料是否启用。")


class Message(BaseModel):
    """通用消息响应模型。"""

    message: str


class HealthStatus(BaseModel):
    """健康检查接口的响应模型。"""

    status: str
    app_name: str
    version: str


class SearchResult(BaseModel):
    """搜索接口的响应模型。"""

    query: str
    count: int
    items: list[Item]


if __name__ == "__main__":
    # 练习题答案 1：
    # 如何手动创建一个符合 ItemCreate 模型的数据？
    # 答案：像下面这样传入 name、description、price、tags 即可。
    demo_item = ItemCreate(
        name="练习题答案资料",
        description="这是 schemas.py 文件后面给出的练习题答案示例。",
        price=9.9,
        tags=["answer", "schema"],
    )

    print("练习题答案 1：成功创建 ItemCreate 模型")
    print(demo_item.model_dump())
