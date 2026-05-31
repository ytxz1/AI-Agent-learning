"""
计算器工具：执行数学运算

支持的运算：
- 基本运算：加减乘除
- 数学函数：abs, round, min, max
- 幂运算：**
- 取余：%
"""

import math


def calculator(expression: str) -> str:
    """
    执行数学计算

    参数:
        expression: 数学表达式字符串，如 "2 + 3 * 4"

    返回:
        计算结果字符串
    """
    try:
        # 安全的数学环境，只允许数学相关的操作
        safe_dict = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "pow": pow,
            "sqrt": math.sqrt,
            "pi": math.pi,
            "e": math.e,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
        }

        # 使用 eval 在安全环境中执行（生产环境应使用 ast.literal_eval 或解析器）
        result = eval(expression, {"__builtins__": {}}, safe_dict)

        # 格式化输出
        if isinstance(result, float):
            # 如果是整数结果，去掉小数点
            if result == int(result):
                return str(int(result))
            return f"{result:.6g}"

        return str(result)

    except ZeroDivisionError:
        return "计算错误：除数不能为零"
    except Exception as e:
        return f"计算错误：{str(e)}"
