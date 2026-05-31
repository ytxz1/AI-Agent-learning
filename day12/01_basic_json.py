"""Exercise 1: Basic JSON output."""

from modules.demo_workflow import StructuredOutputWorkflow


if __name__ == "__main__":
    workflow = StructuredOutputWorkflow()
    result = workflow.run("extract", "Python is a friendly programming language for AI development.")
    print(result)

