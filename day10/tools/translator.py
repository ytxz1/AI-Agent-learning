"""
翻译工具：中英文互译

模拟翻译数据，实际项目中可以接入翻译 API（如百度翻译、DeepL）
"""


def translate(text: str, target_language: str = "英文") -> str:
    """
    翻译文本

    参数:
        text: 待翻译的文本
        target_language: 目标语言，默认为"英文"

    返回:
        翻译结果字符串
    """
    # 模拟翻译数据
    translations = {
        ("你好", "英文"): "Hello",
        ("谢谢", "英文"): "Thank you",
        ("再见", "英文"): "Goodbye",
        ("早上好", "英文"): "Good morning",
        ("晚上好", "英文"): "Good evening",
        ("对不起", "英文"): "Sorry",
        ("没问题", "英文"): "No problem",
        ("我爱你", "英文"): "I love you",
        ("今天天气怎么样", "英文"): "How is the weather today?",
        ("我喜欢编程", "英文"): "I like programming",
        ("hello", "中文"): "你好",
        ("thank you", "中文"): "谢谢",
        ("goodbye", "中文"): "再见",
        ("good morning", "中文"): "早上好",
        ("i love you", "中文"): "我爱你",
        ("python", "中文"): "Python（一种编程语言）",
    }

    key = (text.strip().lower(), target_language)
    if key in translations:
        return translations[key]

    return f"暂时无法将「{text}」翻译为{target_language}，目前支持的翻译有限。"
