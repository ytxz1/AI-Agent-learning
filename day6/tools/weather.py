def get_weather(city):

    weather_data = {
        "北京": "25°C，晴天",
        "上海": "28°C，多云",
        "广州": "32°C，暴雨",
        "深圳": "30°C，小雨",
        "杭州": "26°C，阴天"
    }

    return weather_data.get(city, "未找到该城市天气")