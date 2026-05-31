"""兼容包装模块。

Day 13 的主实现仍然放在 `05_agent_module.py` 里。
这个文件只是提供一个稳定的导入路径，方便其他模块使用：

    from modules.agent import SmartAgent
"""

from __future__ import annotations

import importlib.util
import os


def _load_agent_class():
    """从项目根目录加载 `05_agent_module.py`。"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    module_path = os.path.join(project_root, "05_agent_module.py")
    spec = importlib.util.spec_from_file_location("day13_agent_module", module_path)
    if spec is None or spec.loader is None:
        raise ImportError("无法加载 05_agent_module.py")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.SmartAgent


SmartAgent = _load_agent_class()
