"""练习 4：实现多工具组合任务

题目
示例：
1. 先查天气。
2. 再把温度换算成华氏度。
3. 最后把结果整理成一句完整回答。

--------------------------------------------------
答案写在后面
--------------------------------------------------

答案思路
多工具任务的关键不是“同时调用”，而是：
**按顺序调用，并把前一步结果喂给下一步。**

这类逻辑最好放在 `day14/modules/agent.py` 里。

示例答案 1：天气 + 换算

你可以写一个组合逻辑：

```python
def answer_weather_and_convert(self, city: str) -> str:
    weather_text = get_weather.invoke({"city": city})
    temp_match = re.search(r"(\\d+)°C", weather_text)
    if not temp_match:
        return weather_text
    temp_value = float(temp_match.group(1))
    converted = unit_convert.invoke(
        {"value": temp_value, "from_unit": "celsius", "to_unit": "fahrenheit"}
    )
    return f"{weather_text}，换算后约为 {converted}"
```

示例答案 2：把两个工具结果合并成自然语言

你可以把最终输出组织成：

```text
北京今天晴，25°C，换算成华氏度约 77°F。
```

这样用户不用自己读两条工具输出。

具体是如何添加的
1. 打开 `day14/modules/agent.py`。
2. 新增一个组合处理函数，比如 `answer_weather_and_convert()`。
3. 在 `auto_mode()` 或 `tool_mode()` 里识别这类组合问题。
4. 先调用第一个工具，再把结果转给第二个工具。
5. 最后把结果整理成人类可读的完整句子。

推荐测试句子

```text
帮我查北京天气，再把温度换成华氏度
上海天气怎么样，并把温度换成华氏度
```

如果 Agent 能先查天气，再做换算，再总结，这题就完成了。
"""

print("答案：在 day14/modules/agent.py 中新增组合处理逻辑，把多个工具结果串起来。")
