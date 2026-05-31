"""Exercise 4: Multi-field structured output."""

from modules.demo_workflow import StructuredOutputWorkflow


if __name__ == "__main__":
    workflow = StructuredOutputWorkflow()
    text = "Please summarize this sentence and extract keywords: AI agents can use tools and retrieval to solve tasks."
    result = workflow.run("extract", text)
    print(result)

