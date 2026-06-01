"""HTTP 请求封装模块。

这里不直接把 requests 写在主程序里，而是封装成函数。
这样后面做重试、日志、错误处理时会更清楚。
"""

from __future__ import annotations

import requests


class APIRequestError(RuntimeError):
    """API 请求失败时抛出的错误。"""


def post_json(url: str, headers: dict, payload: dict, timeout: int = 30) -> dict:
    """发送 JSON POST 请求，并返回响应 JSON。"""
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise APIRequestError(f"请求失败：{exc}") from exc

    try:
        return response.json()
    except ValueError as exc:
        raise APIRequestError(f"响应不是合法 JSON：{exc}") from exc

