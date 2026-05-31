"""Exercise 3: Retry parsing."""

from modules.demo_workflow import StructuredOutputWorkflow


if __name__ == "__main__":
    workflow = StructuredOutputWorkflow(max_retry=3)
    result = workflow.run("intent", "Please help me check the weather in Beijing.")
    print(result)

