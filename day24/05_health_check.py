"""练习 05：健康检查接口。

部署上线后，最先要确认的不是复杂业务，而是服务是否还活着。
健康检查接口通常用于：
- Docker healthcheck；
- 云服务器监控；
- 负载均衡探活；
- 自动化部署验证。
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from rich.console import Console

from modules.app_factory import create_app


console = Console()


def main() -> None:
    """运行健康检查接口演示。"""

    client = TestClient(create_app())

    console.rule("[bold green]练习 05：健康检查")

    health_response = client.get("/api/health")
    deploy_info_response = client.get("/api/deploy/info")
    checklist_response = client.get("/api/deploy/checklist")

    console.print("GET /api/health 状态码：", health_response.status_code)
    console.print(health_response.json())
    console.print("\nGET /api/deploy/info：")
    console.print(deploy_info_response.json())
    console.print("\nGET /api/deploy/checklist：")
    console.print(checklist_response.json())

    # 练习题答案：
    # 题目：如何给健康检查加自动化断言？
    # 如何添加：
    # assert health_response.status_code == 200
    # assert health_response.json()["status"] == "ok"


if __name__ == "__main__":
    main()
