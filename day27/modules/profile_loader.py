"""项目经历素材加载器。

简历优化不能凭空编。
更好的做法是先把项目事实整理成结构化素材，再从素材中提炼简历和面试回答。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


DAY27_DIR = Path(__file__).resolve().parents[1]
if str(DAY27_DIR) not in sys.path:
    sys.path.insert(0, str(DAY27_DIR))

from config import PROFILE_FILE

try:
    from .schemas import ProjectProfile
except ImportError:
    from schemas import ProjectProfile


def load_project_profile(profile_file: Path = PROFILE_FILE) -> ProjectProfile:
    """读取项目经历素材 JSON。"""

    data = json.loads(profile_file.read_text(encoding="utf-8"))
    return ProjectProfile(**data)


if __name__ == "__main__":
    # 练习题答案 2：
    # 如何读取项目经历素材？
    # 如何添加：调用 load_project_profile()。
    profile = load_project_profile()
    print("练习题答案 2：项目素材读取成功")
    print("项目名称：", profile.project_name)
    print("技术栈：", "、".join(profile.tech_stack))
