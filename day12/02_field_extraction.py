"""练习 2：字段抽取。

这个练习演示：如何从一段类似简历的话里抽出固定字段。
"""

from modules.demo_workflow import StructuredOutputWorkflow


if __name__ == "__main__":
    # 这里使用 resume schema，看看字段抽取后的结果长什么样。
    workflow = StructuredOutputWorkflow()
    result = workflow.run("resume", "我叫 Alice，学过计算机科学，会 Python、数据分析和 AI。")
    print("练习 2 输出结果：")
    print(result)
