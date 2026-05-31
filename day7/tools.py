def get_weather(city):

    weather_data = {
        "北京": "25°C，晴天",
        "上海": "28°C，多云",
        "广州": "32°C，暴雨",
        "深圳": "30°C，小雨",
        "杭州": "26°C，阴天"
    }

    return weather_data.get(
        city,
        "未找到该城市天气"
    )


def calculator(expression):

    try:

        result = eval(expression)

        return f"计算结果：{result}"

    except Exception as e:

        return f"计算错误：{e}"


def translate(text, target_language):

    translations = {

        ("你好", "英文"): "Hello",
        ("谢谢", "英文"): "Thank you",
        ("再见", "英文"): "Goodbye",

        ("hello", "中文"): "你好",
        ("thank you", "中文"): "谢谢",
        ("goodbye", "中文"): "再见"
    }

    return translations.get(
        (text.lower(), target_language),
        "暂时无法翻译"
    )