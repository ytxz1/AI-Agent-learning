"""练习 1：基础 JSON 输出。"""

from modules.demo_workflow import StructuredOutputWorkflow


if __name__ == "__main__":
    workflow = StructuredOutputWorkflow()
    result = workflow.run("extract", "Python 是一门适合 AI 开发的友好编程语言。")
    print("练习 1 输出结果：")
    print(result)
