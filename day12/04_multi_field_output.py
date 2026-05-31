"""练习 4：多字段结构化输出。

这个练习演示：一个输出里可以同时包含标题、摘要、关键词和分类。
"""

from modules.demo_workflow import StructuredOutputWorkflow


if __name__ == "__main__":
    # 这里用抽取任务测试多字段输出。
    workflow = StructuredOutputWorkflow()
    text = "请总结这句话并提取关键词：AI Agent 可以结合工具和检索来解决任务。"
    result = workflow.run("extract", text)
    print("练习 4 输出结果：")
    print(result)
