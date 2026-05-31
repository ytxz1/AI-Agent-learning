"""知识搜索工具模块"""


def search_knowledge(query: str) -> str:
    """
    搜索知识库获取信息。
    当用户问知识性问题时使用此工具。

    参数:
        query: 搜索关键词

    返回:
        搜索结果字符串
    """
    # 模拟知识库（实际项目中会连接数据库或搜索引擎）
    knowledge_base = {
        "python": "Python 是一种高级编程语言，以简洁易读著称。广泛应用于 Web 开发、数据科学、AI 等领域。最新版本为 Python 3.12。",
        "机器学习": "机器学习是 AI 的分支，使计算机从数据中学习。分为监督学习、无监督学习、强化学习三大类。",
        "langchain": "LangChain 是构建 LLM 应用的开源框架，提供 Prompt、Chain、Agent、Memory 等核心组件。",
        "transformer": "Transformer 是 2017 年 Google 在论文 Attention is All You Need 中提出的架构。",
        "agent": "AI Agent 是能自主决策和执行任务的智能体，结合 LLM（大脑）、Tools（工具）和 Memory（记忆）。",
        "深度学习": "深度学习是机器学习的子集，使用多层神经网络。擅长处理图像、语音、文本等非结构化数据。",
    }
    results = []
    for key, value in knowledge_base.items():
        if key in query.lower():
            results.append(f"【{key}】{value}")
    return "\n".join(results) if results else f"未找到与「{query}」相关的信息"
