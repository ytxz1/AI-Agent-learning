"""生成部署信息的工具模块。

把部署信息单独放在这里，有两个好处：
1. routes.py 不会塞满配置拼接逻辑；
2. 学习脚本可以直接复用 get_deployment_info()。
"""

from __future__ import annotations

import sys
from pathlib import Path


DAY24_DIR = Path(__file__).resolve().parents[1]
if str(DAY24_DIR) not in sys.path:
    sys.path.insert(0, str(DAY24_DIR))

from config import DOCS_URL, ENVIRONMENT, HOST, PORT, REDOC_URL, SERVICE_NAME

try:
    from .schemas import DeploymentInfo, DeployCheckItem
except ImportError:
    from schemas import DeploymentInfo, DeployCheckItem


def get_deployment_info() -> DeploymentInfo:
    """返回当前项目的部署信息。"""

    return DeploymentInfo(
        service_name=SERVICE_NAME,
        host=HOST,
        port=PORT,
        docs_url=DOCS_URL,
        redoc_url=REDOC_URL,
        environment=ENVIRONMENT,
        docker_ready=True,
        recommended_start_command="uvicorn main:app --host 0.0.0.0 --port 8000",
    )


def get_deploy_checklist() -> list[DeployCheckItem]:
    """返回部署前检查清单。"""

    required_files = [
        ("Dockerfile", DAY24_DIR / "Dockerfile"),
        ("docker-compose.yml", DAY24_DIR / "docker-compose.yml"),
        ("requirements.txt", DAY24_DIR / "requirements.txt"),
        (".env.example", DAY24_DIR / ".env.example"),
        ("main.py", DAY24_DIR / "main.py"),
    ]

    checklist: list[DeployCheckItem] = []
    for title, file_path in required_files:
        checklist.append(
            DeployCheckItem(
                title=f"检查 {title}",
                passed=file_path.exists(),
                suggestion=f"确保 {title} 存在并已提交到项目中。",
            )
        )

    checklist.append(
        DeployCheckItem(
            title="检查容器监听地址",
            passed=HOST == "0.0.0.0",
            suggestion="Docker 部署时 HOST 应该是 0.0.0.0，而不是 127.0.0.1。",
        )
    )
    return checklist


if __name__ == "__main__":
    # 练习题答案 2：
    # 如何查看部署信息和部署检查清单？
    # 如何添加：调用 get_deployment_info() 和 get_deploy_checklist()。
    print("练习题答案 2：部署信息")
    print(get_deployment_info().model_dump())
    print("\n部署检查清单：")
    for item in get_deploy_checklist():
        print(item.model_dump())
