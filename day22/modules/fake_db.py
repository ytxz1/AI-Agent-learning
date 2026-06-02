"""内存版模拟数据库。

真实项目中通常会使用 MySQL、PostgreSQL、MongoDB 等数据库。
为了让 Day22 专注学习 FastAPI，本项目先使用一个简单的内存数据库：
- 程序启动时从 data/items.json 读取初始数据；
- 运行过程中新增、修改、删除都保存在内存中；
- 重启程序后会重新读取 items.json，之前运行时新增的数据不会永久保存。

这样做的好处是代码更轻，不需要安装数据库，也更适合刚入门 API 的阶段。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


# 让这个文件既可以被包导入，也可以被 python modules/fake_db.py 直接运行。
DAY22_DIR = Path(__file__).resolve().parents[1]
if str(DAY22_DIR) not in sys.path:
    sys.path.insert(0, str(DAY22_DIR))

try:
    from .schemas import Item, ItemCreate, ItemUpdate
except ImportError:
    from schemas import Item, ItemCreate, ItemUpdate


class FakeItemDB:
    """一个非常小的内存数据库类。"""

    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file
        self._items: dict[int, Item] = {}
        self._next_id = 1
        self._load_seed_data()

    def _load_seed_data(self) -> None:
        """从 JSON 文件加载初始数据。"""

        if not self.data_file.exists():
            return

        raw_items = json.loads(self.data_file.read_text(encoding="utf-8"))
        for raw_item in raw_items:
            item = Item(**raw_item)
            self._items[item.id] = item

        if self._items:
            self._next_id = max(self._items) + 1

    def list_items(
        self,
        *,
        skip: int = 0,
        limit: int = 10,
        keyword: str | None = None,
    ) -> list[Item]:
        """查询资料列表。

        skip 表示跳过前几条，limit 表示最多返回几条。
        keyword 不为空时，会按名称、描述、标签做简单搜索。
        """

        items = list(self._items.values())

        if keyword:
            lowered_keyword = keyword.lower()
            items = [
                item
                for item in items
                if lowered_keyword in item.name.lower()
                or lowered_keyword in item.description.lower()
                or any(lowered_keyword in tag.lower() for tag in item.tags)
            ]

        return items[skip : skip + limit]

    def get_item(self, item_id: int) -> Item | None:
        """根据 id 查询单条资料。"""

        return self._items.get(item_id)

    def create_item(self, payload: ItemCreate) -> Item:
        """创建一条新资料。"""

        item = Item(
            id=self._next_id,
            is_active=True,
            **payload.model_dump(),
        )
        self._items[item.id] = item
        self._next_id += 1
        return item

    def update_item(self, item_id: int, payload: ItemUpdate) -> Item | None:
        """更新资料。

        exclude_unset=True 表示只取用户真正传入的字段。
        例如用户只传 {"price": 19.9}，就只更新 price。
        """

        old_item = self.get_item(item_id)
        if old_item is None:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        new_item = old_item.model_copy(update=update_data)
        self._items[item_id] = new_item
        return new_item

    def delete_item(self, item_id: int) -> bool:
        """删除资料。删除成功返回 True，不存在返回 False。"""

        if item_id not in self._items:
            return False

        del self._items[item_id]
        return True


if __name__ == "__main__":
    # 练习题答案 2：
    # 如何不用启动 FastAPI，也能测试数据库类是否能新增和查询数据？
    # 答案：直接创建 FakeItemDB，然后调用 create_item 和 list_items。
    demo_db = FakeItemDB(DAY22_DIR / "data" / "items.json")
    created = demo_db.create_item(
        ItemCreate(
            name="练习题答案：内存数据库新增资料",
            description="这条数据是在 fake_db.py 的答案区域里添加的。",
            price=12.5,
            tags=["answer", "db"],
        )
    )

    print("练习题答案 2：新增资料成功")
    print(created.model_dump())
    print("当前资料数量：", len(demo_db.list_items(limit=100)))
