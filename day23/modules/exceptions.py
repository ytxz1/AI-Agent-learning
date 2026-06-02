"""Day23 的自定义异常。

为什么要自定义异常？
因为 API 项目不能把内部错误原样丢给用户。
更好的做法是：
- 内部代码抛出有意义的异常；
- FastAPI 统一捕获；
- 返回结构稳定的 JSON 错误信息。
"""

from __future__ import annotations


class AgentAPIError(Exception):
    """Agent API 的基础异常。"""

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class EmptyQuestionError(AgentAPIError):
    """用户问题为空时抛出的异常。"""


class ToolExecutionError(AgentAPIError):
    """工具执行失败时抛出的异常。"""


if __name__ == "__main__":
    # 练习题答案 2：
    # 如何创建一个自定义异常并携带错误详情？
    # 如何添加：继承 AgentAPIError，然后传入 detail。
    error = EmptyQuestionError("问题不能为空")
    print("练习题答案 2：自定义异常创建成功")
    print("错误详情：", error.detail)
