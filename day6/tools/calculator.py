def calculator(expression):

    try:
        result = eval(expression)

        return f"计算结果：{result}"

    except Exception as e:

        return f"计算错误：{e}"