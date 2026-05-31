"""文件操作工具模块"""

import os

# 安全目录限制，防止 Agent 访问敏感文件
SAFE_DIR = os.path.join(os.path.dirname(__file__), "sandbox")


def read_file(file_path: str) -> str:
    """
    读取文件内容。
    当需要查看文件内容时使用此工具。

    参数:
        file_path: 文件路径（相对于 sandbox 目录）

    返回:
        文件内容字符串
    """
    try:
        # 构建完整路径，限制在安全目录内
        full_path = os.path.join(SAFE_DIR, file_path)
        # 安全检查：确保路径不会跳出安全目录
        if not os.path.abspath(full_path).startswith(os.path.abspath(SAFE_DIR)):
            return "错误：不允许访问安全目录之外的文件"
        # 读取文件内容
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"文件 {file_path} 的内容：\n{content}"
    except FileNotFoundError:
        return f"文件 {file_path} 不存在"
    except Exception as e:
        return f"读取文件错误：{e}"


def write_file(file_path: str, content: str) -> str:
    """
    写入文件内容。
    当需要创建或修改文件时使用此工具。

    参数:
        file_path: 文件路径（相对于 sandbox 目录）
        content: 要写入的内容

    返回:
        操作结果字符串
    """
    try:
        # 构建完整路径
        full_path = os.path.join(SAFE_DIR, file_path)
        # 安全检查
        if not os.path.abspath(full_path).startswith(os.path.abspath(SAFE_DIR)):
            return "错误：不允许写入安全目录之外的文件"
        # 确保目录存在
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        # 写入文件
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"成功写入文件 {file_path}"
    except Exception as e:
        return f"写入文件错误：{e}"
