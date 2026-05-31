"""计算器工具模块"""

import math


def calculator(expression: str) -> str:
    """
    执行数学计算。
    当需要计算数学表达式时使用此工具。

    参数:
        expression: 数学表达式，如 "2 + 3 * 4"、"sqrt(144)"

    返回:
        计算结果的字符串形式
    """
    try:
        # 创建安全的数学函数字典，防止恶意代码执行
        safe_dict = {
            "abs": abs,      # 绝对值
            "round": round,  # 四舍五入
            "min": min,      # 最小值
            "max": max,      # 最大值
            "sqrt": math.sqrt,  # 平方根
            "pow": pow,      # 幂运算
            "pi": math.pi,   # 圆周率
            "sin": math.sin, # 正弦
            "cos": math.cos, # 余弦
            "tan": math.tan, # 正切
            "log": math.log, # 对数
        }
        # 在受限环境中执行表达式
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        # 如果结果是整数，返回整数形式
        if isinstance(result, float) and result == int(result):
            return str(int(result))
        return str(result)
    except Exception as e:
        return f"计算错误：{e}"
