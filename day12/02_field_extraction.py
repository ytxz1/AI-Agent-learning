"""练习 2：字段抽取。"""

from modules.demo_workflow import StructuredOutputWorkflow


if __name__ == "__main__":
    workflow = StructuredOutputWorkflow()
    result = workflow.run("resume", "我叫 Alice，学过计算机科学，会 Python、数据分析和 AI。")
    print("练习 2 输出结果：")
    print(result)
