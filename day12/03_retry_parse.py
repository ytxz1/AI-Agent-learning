"""练习 3：重试解析。"""

from modules.demo_workflow import StructuredOutputWorkflow


if __name__ == "__main__":
    workflow = StructuredOutputWorkflow(max_retry=3)
    result = workflow.run("intent", "请帮我查一下北京的天气。")
    print("练习 3 输出结果：")
    print(result)
