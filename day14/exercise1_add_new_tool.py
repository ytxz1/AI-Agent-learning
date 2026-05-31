"""练习 1：给 Agent 新增一个工具

题目
1. 理解工具的基本格式。
2. 学会把新工具接入 `tool_map`。

建议做法
1. 在 `modules/tools.py` 中新增一个 `@tool` 函数。
2. 把它加入 `all_tools` 列表。
3. 重新运行 `04_tool_agent.py` 测试。

--------------------------------------------------
答案写在后面
--------------------------------------------------

答案思路
你需要做的事情不是改这个练习文件，而是去修改
`day14/modules/tools.py`。

最推荐的添加方式是：
1. 先写一个独立函数。
2. 用 `@tool` 包起来。
3. 给它补上清晰的 docstring。
4. 加入 `all_tools`。
5. 让 `tool_map` 自动收录它。

示例答案 1：新增一个“计算百分比”的工具

你可以把下面这段代码添加到 `day14/modules/tools.py` 里，
放在现有工具函数后面，`all_tools` 列表前面：

```python
@tool
def calculate_percentage(value: float, percent: float) -> str:
    '''计算一个数的百分之几。'''
    result = value * percent / 100
    return f"{value} 的 {percent}% = {result}"
```

然后把它加入 `all_tools`：

```python
all_tools = [
    calculator,
    get_weather,
    translate,
    get_current_time,
    unit_convert,
    calculate_percentage,
]
```

`tool_map` 不需要手工写死新内容，因为它是根据 `all_tools` 自动生成的：

```python
tool_map = {tool_item.name: tool_item for tool_item in all_tools}
```

这样新增工具就完成了。

具体是如何添加的
1. 打开 `day14/modules/tools.py`。
2. 找到现有的 `@tool` 函数区域。
3. 在最后一个工具函数后面添加新函数。
4. 在 `all_tools` 列表里把新函数名补进去。
5. 保存后重新运行 `python 04_tool_agent.py`。

验证方法
你可以在 `04_tool_agent.py` 或 `05_chat_interface.py` 里输入：

```text
帮我算一下 80 的 15%
```

如果 Agent 能调用新工具，就说明添加成功了。
"""

print("答案：请到 day14/modules/tools.py 中新增工具函数，并把它加入 all_tools。")
