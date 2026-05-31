"""练习 5：完整演示。"""

from modules.demo_workflow import StructuredOutputWorkflow


if __name__ == "__main__":
    workflow = StructuredOutputWorkflow()
    tests = [
        ("intent", "帮我翻译这段话"),
        ("extract", "请提取关键词并总结内容"),
        ("resume", "张三，本科，擅长 Python 和 LangChain"),
    ]

    for task, text in tests:
        print("=" * 60)
        print(f"任务：{task}")
        print(f"文本：{text}")
        print(workflow.run(task, text))
