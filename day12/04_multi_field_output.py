"""练习 4：多字段结构化输出。"""

from modules.demo_workflow import StructuredOutputWorkflow


if __name__ == "__main__":
    workflow = StructuredOutputWorkflow()
    text = "请总结这句话并提取关键词：AI Agent 可以结合工具和检索来解决任务。"
    result = workflow.run("extract", text)
    print("练习 4 输出结果：")
    print(result)
