"""Day24 部署上线项目模块包。

模块分工：
- schemas.py：接口请求和响应模型；
- deployment_info.py：生成部署信息；
- routes.py：FastAPI 路由；
- app_factory.py：创建 FastAPI 应用。
"""

from .app_factory import create_app
from .deployment_info import get_deployment_info
from .schemas import DeploymentInfo, HealthStatus, Message

__all__ = [
    "create_app",
    "get_deployment_info",
    "DeploymentInfo",
    "HealthStatus",
    "Message",
]
