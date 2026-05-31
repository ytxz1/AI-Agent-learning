"""练习 3：完善错误处理

题目
1. 工具参数缺失时，给出友好提示。
2. 工具执行失败时，程序不要崩。
3. 对未知工具做降级处理。

--------------------------------------------------
答案写在后面
--------------------------------------------------

答案思路
错误处理最关键的是三层：

1. 工具函数内部兜底
2. Agent 调用时兜底
3. 对用户输出时兜底

最推荐修改的文件：
`day14/modules/tools.py`
和
`day14/modules/agent.py`

示例答案 1：工具内部兜底

在 `calculator` 里已经使用了 `try / except`：

```python
try:
    tree = ast.parse(expression, mode="eval")
    result = _safe_eval(tree)
    return _format_number(result)
except Exception as exc:
    return f"计算失败：{exc}"
```

这说明：
1. 即使表达式非法，也不会让程序崩。
2. 会把错误信息转成可读文本返回。

示例答案 2：Agent 调用时兜底

你可以在 `modules/agent.py` 的 `_invoke_tool()` 中继续强化：

```python
def _invoke_tool(self, tool_name: str, tool_args: dict):
    tool = self.tool_map.get(tool_name)
    if not tool:
        return f"未找到工具：{tool_name}"
    try:
        return tool.invoke(tool_args)
    except Exception as exc:
        return f"工具 {tool_name} 执行失败：{exc}"
```

这一步的作用是：
1. 防止未知工具名导致崩溃。
2. 防止工具参数异常导致崩溃。

示例答案 3：未知场景降级

如果 Agent 不知道该怎么处理，可以回退成普通聊天：

```python
def auto_mode(self, user_input: str) -> str:
    self.current_mode = self.MODE_AUTO
    if self._needs_tool(user_input):
        return self.tool_mode(user_input)
    return self.chat_mode(user_input)
```

这表示：
1. 能用工具就用工具。
2. 不能确定时就别乱调用。

具体是如何添加的
1. 打开 `day14/modules/tools.py`。
2. 给每个工具补上 `try / except`。
3. 打开 `day14/modules/agent.py`。
4. 在 `_invoke_tool()` 里加未知工具和异常兜底。
5. 在 `auto_mode()` 里保持保守策略。
6. 保存后重新运行 `python 04_tool_agent.py`。

验证方法
试一下这些异常输入：

```text
计算 abc
调用一个不存在的工具
把 25 摄氏度换成不存在的单位
```

如果程序没有崩，并且能返回清晰错误提示，就说明完成了。
"""

print("答案：请在 day14/modules/tools.py 和 day14/modules/agent.py 中加入 try/except 和未知场景兜底。")
