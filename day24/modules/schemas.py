"""Day24 的 Pydantic 数据模型。

部署项目里，最常见的接口不是复杂业务接口，而是：
- 健康检查；
- 版本信息；
- 部署环境信息；
- 首页提示。

这些接口能帮助你确认服务是否真的在线。
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Message(BaseModel):
    """通用消息响应模型。"""

    message: str


class HealthStatus(BaseModel):
    """健康检查响应模型。"""

    status: str = Field(description="服务状态，例如 ok。")
    service_name: str = Field(description="服务名称。")
    app_name: str = Field(description="应用名称。")
    version: str = Field(description="应用版本。")
    environment: str = Field(description="当前环境，例如 local、docker、production。")


class DeploymentInfo(BaseModel):
    """部署信息响应模型。"""

    service_name: str
    host: str
    port: int
    docs_url: str
    redoc_url: str
    environment: str
    docker_ready: bool
    recommended_start_command: str


class DeployCheckItem(BaseModel):
    """部署检查项模型。"""

    title: str
    passed: bool
    suggestion: str


if __name__ == "__main__":
    # 练习题答案 1：
    # 如何手动创建一个健康检查响应？
    # 如何添加：给 HealthStatus 传入所有必填字段。
    demo = HealthStatus(
        status="ok",
        service_name="day24-deploy-api",
        app_name="Day24 部署上线 API",
        version="1.0.0",
        environment="local",
    )
    print("练习题答案 1：HealthStatus 创建成功")
    print(demo.model_dump())
