"""练习 1：基础 JSON 输出。

这个脚本主要是为了熟悉“结构化输出”的基本形态。
"""

from modules.demo_workflow import StructuredOutputWorkflow


if __name__ == "__main__":
    # 创建工作流对象，然后用一段简单文本测试“信息抽取”。
    workflow = StructuredOutputWorkflow()
    result = workflow.run("extract", "Python 是一门适合 AI 开发的友好编程语言。")
    print("练习 1 输出结果：")
    print(result)
