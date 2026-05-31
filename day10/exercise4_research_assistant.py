"""
Day 10 - 练习 4（挑战）：研究助手 Agent

任务：构建一个研究助手 Agent，支持搜索、总结、生成报告。

功能：
  1. search_topic     - 搜索某个主题的知识
  2. summarize        - 总结一段文本
  3. generate_report  - 生成研究报告
  4. save_to_file     - 将结果保存到文件

知识点：
  1. 多步骤任务的 Agent 编排
  2. 工具之间的数据传递
  3. 文件写入的安全实践
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel

console = Console()

print("=" * 60)
print("Day 10 - 练习 4：研究助手 Agent")
print("=" * 60)

# ==============================
# 定义工具
# ==============================

@tool
def search_topic(topic: str) -> str:
    """搜索某个主题的相关知识。当用户想了解某个主题时使用此工具。
    参数: topic - 要搜索的主题，如 "人工智能"、"Python"、"量子计算"
    """
    # 模拟知识库（实际项目中会调用搜索引擎或数据库）
    knowledge_base = {
        "人工智能": {
            "定义": "人工智能（AI）是计算机科学的一个分支，致力于创建能模拟人类智能的系统。",
            "历史": "1956年达特茅斯会议标志着 AI 作为学科的诞生。经历了符号主义、连接主义、深度学习三个阶段。",
            "应用": "自然语言处理、计算机视觉、语音识别、自动驾驶、医疗诊断、金融风控等。",
            "趋势": "大语言模型（LLM）、多模态 AI、AI Agent、具身智能是当前热门方向。",
        },
        "python": {
            "定义": "Python 是一种高级编程语言，以简洁易读著称，由 Guido van Rossum 于 1991 年创建。",
            "特点": "语法简洁、丰富的标准库、跨平台、动态类型、支持多种编程范式。",
            "应用": "Web 开发（Django、Flask）、数据科学（Pandas、NumPy）、AI（PyTorch、TensorFlow）、自动化脚本。",
            "生态": "PyPI 拥有超过 40 万个包，社区活跃，文档完善。",
        },
        "机器学习": {
            "定义": "机器学习是 AI 的分支，使计算机从数据中学习规律，无需显式编程。",
            "分类": "监督学习（分类、回归）、无监督学习（聚类、降维）、强化学习（奖励驱动）。",
            "算法": "线性回归、决策树、随机森林、SVM、神经网络、K-Means 等。",
            "工具": "Scikit-learn、TensorFlow、PyTorch、XGBoost、LightGBM。",
        },
        "langchain": {
            "定义": "LangChain 是构建 LLM 应用的开源框架，提供模块化的组件。",
            "组件": "Prompt Template、LLM、Output Parser、Chain、Agent、Memory、Tool。",
            "用途": "对话系统、文档问答、代码生成、数据分析、自动化工作流。",
            "版本": "当前版本支持 LCEL（LangChain Expression Language），推荐使用 Runnable 接口。",
        },
        "transformer": {
            "定义": "Transformer 是 2017 年 Google 在论文 Attention is All You Need 中提出的架构。",
            "核心": "自注意力机制（Self-Attention），可以并行处理序列数据。",
            "影响": "BERT（编码器）、GPT（解码器）、T5（编码器-解码器）都基于 Transformer。",
            "应用": "NLP（文本分类、翻译、问答）、CV（ViT）、语音（Whisper）。",
        },
        "量子计算": {
            "定义": "量子计算利用量子力学原理（叠加、纠缠）进行计算的新型计算模式。",
            "优势": "在特定问题上（如质因数分解、优化、模拟）比经典计算机快指数级。",
            "现状": "IBM、Google、中国科学技术大学等在量子比特数量上竞争激烈。",
            "挑战": "量子退相干、纠错、极低温环境是主要技术瓶颈。",
        },
    }
    # 搜索知识库
    topic_lower = topic.lower()
    for key, value in knowledge_base.items():
        if key.lower() in topic_lower or topic_lower in key.lower():
            result_parts = [f"【{key}】"]
            for sub_key, sub_val in value.items():
                result_parts.append(f"  {sub_key}：{sub_val}")
            return "\n".join(result_parts)
    return f"未找到与「{topic}」相关的详细信息。请尝试：人工智能、Python、机器学习、LangChain、Transformer、量子计算"

@tool
def summarize(text: str, style: str = "brief") -> str:
    """总结一段文本。当用户需要对文本进行总结时使用此工具。
    参数: text - 要总结的文本, style - 总结风格：brief（简要，默认）或 detailed（详细）"""
    sentences = [s.strip() for s in text.replace("。", ".|").replace("；", ".|").split(".|") if s.strip()]
    total = len(sentences)

    if style == "detailed":
        # 详细总结：保留更多内容
        summary_parts = [f"原文共 {total} 个句子，详细总结如下："]
        for i, s in enumerate(sentences, 1):
            summary_parts.append(f"  {i}. {s}")
        return "\n".join(summary_parts)
    else:
        # 简要总结：取前 3 句
        key_sentences = sentences[:3]
        summary = "简要总结：\n"
        for i, s in enumerate(key_sentences, 1):
            summary += f"  {i}. {s}\n"
        if total > 3:
            summary += f"  ...（共 {total} 句，已省略 {total - 3} 句）"
        return summary

@tool
def generate_report(topic: str, content: str) -> str:
    """根据主题和内容生成一份格式化的研究报告。
    参数: topic - 报告主题, content - 报告内容素材"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"""
{'=' * 50}
研究报告：{topic}
{'=' * 50}
生成时间：{now}

一、概述
  本报告对「{topic}」进行了系统性的研究和分析。

二、核心内容
{content}

三、关键发现
  1. {topic} 是当前技术领域的热门方向
  2. 相关技术正在快速发展和演进
  3. 在多个行业有广泛的应用前景

四、建议
  - 持续关注该领域的最新进展
  - 结合实际项目进行实践
  - 参考官方文档和学术论文

{'=' * 50}
报告结束
{'=' * 50}"""
    return report

@tool
def save_to_file(filename: str, content: str) -> str:
    """将内容保存到文件。当用户想保存结果时使用此工具。
    参数: filename - 文件名（如 report.txt）, content - 要保存的内容"""
    try:
        safe_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(safe_dir, exist_ok=True)
        full_path = os.path.normpath(os.path.join(safe_dir, filename))
        if not full_path.startswith(safe_dir):
            return "错误：不允许写入安全目录之外的文件"
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"成功保存到文件：output/{filename}"
    except Exception as e:
        return f"保存文件错误：{e}"

tools = [search_topic, summarize, generate_report, save_to_file]

# ==============================
# Agent 循环
# ==============================

system_prompt = SystemMessage(content=(
    "你是一个研究助手 Agent，专门帮助用户进行主题研究和报告生成。\n"
    "你的工具：\n"
    "1. search_topic - 搜索主题知识\n"
    "2. summarize - 总结文本\n"
    "3. generate_report - 生成研究报告\n"
    "4. save_to_file - 保存到文件\n"
    "工作流程：先搜索知识，再总结，然后生成报告，最后按需保存。"
))

def run_agent(user_input: str, max_rounds: int = 5):
    """运行研究助手 Agent"""
    console.print(f"\n[bold]用户: {user_input}[/bold]")
    llm_with_tools = llm.bind_tools(tools)
    messages = [system_prompt, HumanMessage(content=user_input)]

    for round_num in range(max_rounds):
        console.print(f"[dim]--- 第 {round_num + 1} 轮 ---[/dim]")
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            for tc in response.tool_calls:
                tool_name = tc["name"]
                tool_args = tc["args"]
                console.print(f"  [工具] {tool_name}({tool_args})", style="yellow")
                tool_func = next((t for t in tools if t.name == tool_name), None)
                if tool_func:
                    result = tool_func.invoke(tool_args)
                else:
                    result = "未知工具"
                display = result if len(result) < 300 else result[:300] + "..."
                console.print(f"  [结果] {display}", style="green")
                messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
        else:
            console.print(f"\n[bold green]AI: {response.content}[/bold green]")
            return response.content
    return "达到最大调用轮数"

# ==============================
# LLM 实例
# ==============================

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=MODEL_NAME,
    temperature=0.7,
)

# ==============================
# 测试
# ==============================

console.print(Panel.fit("Day 10 - 练习 4：研究助手 Agent", style="bold green"))

# 测试1：搜索并总结
run_agent("帮我搜索一下人工智能的相关知识，然后做一个简要总结")

# 测试2：搜索并生成报告
run_agent("研究一下 LangChain 框架，帮我生成一份研究报告")

# 测试3：完整的多步骤流程
run_agent("帮我研究 Python 语言，搜索相关知识，生成报告，然后保存到文件")

console.print("\n" + "=" * 60, style="bold green")
console.print("练习 4 完成：研究助手 Agent 构建成功！", style="bold green")
console.print("=" * 60, style="bold green")
