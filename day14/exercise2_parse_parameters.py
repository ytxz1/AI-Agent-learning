"""练习 2：把自然语言解析成工具参数

题目
1. 从用户文本中提取城市、数值、目标语言等参数。
2. 提高工具调用成功率。

你可以尝试处理：
- "帮我查北京天气"
- "把 25 摄氏度换成华氏度"
- "把谢谢翻译成英文"

--------------------------------------------------
答案写在后面
--------------------------------------------------

答案思路
这道题的重点不在工具本身，而在于：
**把用户的自然语言，拆成工具需要的结构化参数。**

最适合改的位置是：
`day14/modules/agent.py`

你需要补强的通常有三块：

1. 城市识别
2. 翻译文本提取
3. 单位换算参数提取

示例答案 1：城市识别

你可以在 `ToolAgent` 里增加一个辅助函数：

```python
def _guess_city(self, text: str) -> str:
    city_candidates = ["北京", "上海", "广州", "深圳", "杭州", "成都"]
    for city in city_candidates:
        if city in text:
            return city
    return "北京"
```

它的作用是：
1. 从句子里找城市名。
2. 找不到时给一个默认城市。

示例答案 2：翻译目标语言提取

```python
def _guess_target_language(self, text: str) -> str:
    if "英文" in text or "英语" in text or "en" in text.lower():
        return "English"
    if "中文" in text or "汉语" in text or "zh" in text.lower():
        return "Chinese"
    return "English"
```

它的作用是：
1. 识别用户想翻成哪种语言。
2. 让 `translate` 工具收到正确参数。

示例答案 3：单位换算参数提取

```python
def _guess_unit_conversion(self, text: str):
    patterns = [
        (r"(\\d+(?:\\.\\d+)?)\\s*(?:摄氏度|celsius|c)\\s*(?:转|换算成|换成|到)\\s*(?:华氏度|fahrenheit|f)", "celsius", "fahrenheit"),
    ]
```

它的作用是：
1. 先用正则提取数字。
2. 再识别“从什么单位到什么单位”。

具体是如何添加的
1. 打开 `day14/modules/agent.py`。
2. 找到 `ToolAgent` 类。
3. 在 `chat_mode` / `tool_mode` 之前添加参数提取辅助函数。
4. 在 `_fallback_tool_answer()` 或真正的工具调用逻辑里使用这些函数。
5. 保存后重新测试 `python 04_tool_agent.py`。

验证方法
输入下面这些句子：

```text
帮我查北京天气
把谢谢翻译成英文
把 25 摄氏度换成华氏度
```

如果工具拿到的参数是正确的，说明这题完成了。
"""

print("答案：请在 day14/modules/agent.py 中加入参数提取辅助函数。")
