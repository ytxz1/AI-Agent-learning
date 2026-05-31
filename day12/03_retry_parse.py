"""练习 3：重试解析。

这个练习主要看：当模型输出格式不理想时，系统会不会自动重试。
"""

from modules.demo_workflow import StructuredOutputWorkflow


if __name__ == "__main__":
    # max_retry=3 表示允许多试几次，方便观察重试逻辑。
    workflow = StructuredOutputWorkflow(max_retry=3)
    result = workflow.run("intent", "请帮我查一下北京的天气。")
    print("练习 3 输出结果：")
    print(result)
