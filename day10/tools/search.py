"""
知识搜索工具：搜索本地知识库

模拟知识库搜索，实际项目中可以接入向量数据库或搜索引擎
"""


def search_knowledge(query: str) -> str:
    """
    搜索知识库

    参数:
        query: 搜索关键词

    返回:
        搜索结果字符串
    """
    # 模拟知识库
    knowledge_base = {
        "python": "Python是一种高级编程语言，由Guido van Rossum于1991年创建。它以简洁易读的语法著称，广泛应用于Web开发、数据科学、人工智能等领域。",
        "机器学习": "机器学习是人工智能的一个分支，它使计算机能够从数据中学习，而无需显式编程。主要分为监督学习、无监督学习和强化学习三大类。",
        "深度学习": "深度学习是机器学习的一个子集，使用多层神经网络来学习数据的层次化表示。常见的架构包括CNN、RNN、Transformer等。",
        "langchain": "LangChain是一个用于构建大语言模型应用的开源框架，提供了Prompt模板、Chain、Agent、Memory等核心组件。",
        "agent": "AI Agent是能够自主决策和执行任务的智能体，通常结合LLM、工具调用和记忆系统来完成复杂任务。",
        "rag": "RAG（检索增强生成）是一种结合信息检索和文本生成的技术，通过从外部知识库检索相关信息来增强LLM的回答质量。",
        "transformer": "Transformer是2017年Google提出的神经网络架构，是现代大语言模型（如GPT、BERT）的基础，核心机制是自注意力（Self-Attention）。",
        "gpt": "GPT（Generative Pre-trained Transformer）是OpenAI开发的大语言模型系列，通过预训练和微调来生成高质量文本。",
        "prompt": "Prompt是给大语言模型的输入文本，好的Prompt设计可以显著提升模型输出质量。常见技巧包括Few-shot、Chain-of-Thought等。",
        "embedding": "Embedding是将文本转换为向量表示的技术，用于计算文本相似度、语义搜索等任务。常用的模型包括OpenAI Embedding、BGE等。",
    }

    query_lower = query.lower()
    results = []

    for key, value in knowledge_base.items():
        if key in query_lower or query_lower in key:
            results.append(f"【{key}】{value}")

    if results:
        return "\n\n".join(results)

    return f"未找到与「{query}」相关的知识。知识库中包含：{', '.join(knowledge_base.keys())}"
