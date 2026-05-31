"""Exercise 2: Field extraction."""

from modules.demo_workflow import StructuredOutputWorkflow


if __name__ == "__main__":
    workflow = StructuredOutputWorkflow()
    result = workflow.run("resume", "My name is Alice. I studied computer science and know Python, data analysis, and AI.")
    print(result)

