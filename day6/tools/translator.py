def translate(text, target_language):

    translations = {
        ("你好", "英文"): "Hello",
        ("谢谢", "英文"): "Thank you",
        ("再见", "英文"): "Goodbye",

        ("hello", "中文"): "你好",
        ("thank you", "中文"): "谢谢"
    }

    return translations.get(
        (text.lower(), target_language),
        "暂时无法翻译"
    )