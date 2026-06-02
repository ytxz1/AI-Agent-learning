"""Day24 的 FastAPI 路由。

部署上线时，健康检查和版本信息非常重要。
它们可以帮助你判断：
- 服务是否启动；
- 当前部署的是哪个版本；
- 文档地址在哪里；
- Docker 配置是否准备好。
"""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import APIRouter


DAY24_DIR = Path(__file__).resolve().parents[1]
if str(DAY24_DIR) not in sys.path:
    sys.path.insert(0, str(DAY24_DIR))

from config import API_PREFIX, APP_NAME, APP_VERSION, ENVIRONMENT, SERVICE_NAME

try:
    from .deployment_info import get_deploy_checklist, get_deployment_info
    from .schemas import DeploymentInfo, DeployCheckItem, HealthStatus
except ImportError:
    from deployment_info import get_deploy_checklist, get_deployment_info
    from schemas import DeploymentInfo, DeployCheckItem, HealthStatus


router = APIRouter(prefix=API_PREFIX, tags=["部署检查 API"])


@router.get("/health", response_model=HealthStatus)
def health_check() -> HealthStatus:
    """健康检查接口。

    Docker healthcheck、云服务器监控、负载均衡都可以调用这个接口。
    """

    return HealthStatus(
        status="ok",
        service_name=SERVICE_NAME,
        app_name=APP_NAME,
        version=APP_VERSION,
        environment=ENVIRONMENT,
    )


@router.get("/deploy/info", response_model=DeploymentInfo)
def deployment_info() -> DeploymentInfo:
    """查看当前部署信息。"""

    return get_deployment_info()


@router.get("/deploy/checklist", response_model=list[DeployCheckItem])
def deployment_checklist() -> list[DeployCheckItem]:
    """查看部署前检查清单。"""

    return get_deploy_checklist()


if __name__ == "__main__":
    # 练习题答案 3：
    # 如何查看当前注册的部署接口？
    # 如何添加：遍历 router.routes，打印 path 和 methods。
    print("练习题答案 3：当前部署接口如下")
    for route in router.routes:
        methods = ",".join(sorted(route.methods or []))
        print(f"{methods:10s} {route.path}")
