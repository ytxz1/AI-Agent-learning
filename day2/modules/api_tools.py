"""requests 演示模块。

Day 2 的路线图里提到了常用库 requests。
为了避免必须联网才能学习，这里提供一个在线优先、本地兜底的示例。
"""

from __future__ import annotations

import requests


def fetch_python_repo_info(timeout: int = 5) -> dict:
    """获取 Python 官方仓库信息。

    如果网络不可用，就返回本地兜底数据。
    """
    url = "https://api.github.com/repos/python/cpython"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return {
            "source": "online",
            "name": data.get("full_name"),
            "stars": data.get("stargazers_count"),
            "language": data.get("language"),
            "description": data.get("description"),
        }
    except Exception as exc:
        return {
            "source": "fallback",
            "name": "python/cpython",
            "stars": "网络不可用时不展示实时数据",
            "language": "Python",
            "description": "The Python programming language",
            "error": str(exc),
        }

