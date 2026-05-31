"""
Day 11 - 练习 5（综合）：研究助手 Agent

任务：构建一个研究助手 Agent，支持搜索、总结、生成报告、保存结果。

新增内容（标注 [新增]）：
  1. [新增] search_topic 工具（主题知识搜索）
  2. [新增] summarize 工具（文本摘要）
  3. [新增] generate_report 工具（生成研究报告）
  4. [新增] save_to_file 工具（保存结果到文件）
  5. [新增] ResearchAgent 类（多步骤研究流程）
"""

import os, sys
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from rich.console import Console
from rich.panel import Panel

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 11 - 练习 5：研究助手 Agent", style="bold blue")
console.print("=" * 60, style="bold blue")

# [新增] 工具 1：主题知识搜索
@tool
def search_topic(topic: str) -> str:
    """搜索某个主题的相关知识。当用户想了解某个主题时使用此工具。
    参数: topic - 要搜索的主题"""
    knowledge = {
        "人工智能": "人工智能（AI）是计算机科学的分支，致力于创建能模拟人类智能的系统。"
            "1956年达特茅斯会议标志着 AI 诞生。经历了符号主义、连接主义、深度学习三个阶段。"
            "应用：NLP、计算机视觉、语音识别、自动驾驶、医疗诊断等。"
            "当前热门方向：大语言模型、多模态 AI、AI Agent、具身智能。",
        "python": "Python 是高级编程语言，由 Guido van Rossum 于 1991 年创建。"
            "特点：语法简洁、丰富标准库、跨平台、动态类型。"
            "应用：Web 开发（Django）、数据科学（Pandas）、AI（PyTorch）、自动化。"
            "PyPI 拥有超过 40 万个包，社区活跃。",
        "机器学习": "机器学习是 AI 的分支，使计算机从数据中学习规律。"
            "分类：监督学习（分类、回归）、无监督学习（聚类）、强化学习。"
            "常用算法：线性回归、决策树、随机森林、SVM、神经网络。"
            "工具：Scikit-learn、TensorFlow、PyTorch。",
        "langchain": "LangChain 是构建 LLM 应用的开源框架。"
            "核心组件：Prompt Template、LLM、Output Parser、Chain、Agent、Memory、Tool。"
            "用途：对话系统、文档问答、代码生成、自动化工作流。"
            "最新版本支持 LCEL（LangChain Expression Language）。",
        "transformer": "Transformer 是 2017 年 Google 提出的架构（Attention is All You Need）。"
            "核心：自注意力机制（Self-Attention），可并行处理序列。"
            "代表模型：BERT（编码器）、GPT（解码器）、T5。"
            "应用：NLP、计算机视觉（ViT）、语音（Whisper）。",
        "量子计算": "量子计算利用量子力学原理（叠加、纠缠）进行计算。"
            "优势：特定问题上比经典计算机快指数级。"
            "现状：IBM、Google、中科大等竞争激烈。"
            "挑战：量子退相干、纠错、极低温环境。",
    }
    for key, value in knowledge.items():
        if key.lower() in topic.lower() or topic.lower() in key.lower():
            return f"【{key}】{value}"
    return f"未找到与「{topic}」相关的详细信息。可尝试：人工智能、Python、机器学习、LangChain、Transformer、量子计算"

# [新增] 工具 2：文本摘要
@tool
def summarize(text: str, style: str = "brief") -> str:
    """总结一段文本。当用户需要对文本做总结时使用此工具。
    参数: text - 要总结的文本, style - 风格：brief（简要，默认）或 detailed（详细）"""
    sentences = [s.strip() for s in text.replace("。", ".|").replace("；", ".|").split(".|") if s.strip()]
    total = len(sentences)
    if style == "detailed":
        parts = [f"原文共 {total} 句，详细总结："]
        for i, s in enumerate(sentences, 1):
            parts.append(f"  {i}. {s}")
        return "\n".join(parts)
    else:
        key_sentences = sentences[:3]
        summary = "简要总结：\n" + "\n".join(f"  {i}. {s}" for i, s in enumerate(key_sentences, 1))
        if total > 3:
            summary += f"\n  ...（共 {total} 句，省略 {total - 3} 句）"
        return summary

# [新增] 工具 3：生成研究报告
@tool
def generate_report(topic: str, content: str) -> str:
    """根据主题和内容生成格式化的研究报告。
    参数: topic - 报告主题, content - 报告内容素材"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return (
        f"{'=' * 50}\n"
        f"研究报告：{topic}\n"
        f"{'=' * 50}\n"
        f"生成时间：{now}\n\n"
        f"一、概述\n"
        f"  本报告对「{topic}」进行了系统性研究。\n\n"
        f"二、核心内容\n"
        f"  {content}\n\n"
        f"三、关键发现\n"
        f"  1. {topic} 是当前技术领域的热门方向\n"
        f"  2. 相关技术正在快速发展\n"
        f"  3. 在多个行业有广泛应用\n\n"
        f"四、建议\n"
        f"  - 持续关注最新进展\n"
        f"  - 结合项目进行实践\n"
        f"  - 参考官方文档\n\n"
        f"{'=' * 50}\n"
        f"报告结束\n"
        f"{'=' * 50}"
    )

# [新增] 工具 4：保存到文件
@tool
def save_to_file(filename: str, content: str) -> str:
    """将内容保存到文件。当用户想保存研究结果时使用此工具。
    参数: filename - 文件名, content - 要保存的内容"""
    try:
        safe_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(safe_dir, exist_ok=True)
        full_path = os.path.normpath(os.path.join(safe_dir, filename))
        if not full_path.startswith(safe_dir):
            return "错误：不允许写入安全目录之外的文件"
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"成功保存到 output/{filename}"
    except Exception as e:
        return f"保存失败：{e}"

all_tools = [search_topic, summarize, generate_report, save_to_file]
tool_map = {t.name: t for t in all_tools}

llm = ChatOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, model=MODEL_NAME, temperature=0.7)

# [新增] 研究助手 Agent 类
class ResearchAgent:
    """研究助手 Agent：搜索 -> 总结 -> 报告 -> 保存"""

    def __init__(self):
        self.system_prompt = SystemMessage(content=(
            "你是一个研究助手 Agent，帮助用户进行主题研究和报告生成。\n"
            "工具：search_topic（搜索知识）、summarize（总结）、generate_report（生成报告）、save_to_file（保存文件）。\n"
            "工作流程：先搜索知识，再总结，然后生成报告，最后按需保存。"
        ))
        self.messages = [self.system_prompt]
        self.llm = llm.bind_tools(all_tools)

    def chat(self, user_input, max_rounds=5):
        self.messages.append(HumanMessage(content=user_input))
        for _ in range(max_rounds):
            response = self.llm.invoke(self.messages)
            self.messages.append(response)
            if response.tool_calls:
                for tc in response.tool_calls:
                    console.print(f"  [工具] {tc['name']}({tc['args']})", style="yellow")
                    result = tool_map[tc["name"]].invoke(tc["args"]) if tc["name"] in tool_map else "未知工具"
                    display = result if len(result) < 300 else result[:300] + "..."
                    console.print(f"  [结果] {display}", style="green")
                    self.messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
            else:
                return response.content
        return "达到最大推理轮数"

# 演示
console.print("\n[bold cyan]研究助手 Agent 演示[/bold cyan]")
agent = ResearchAgent()

# 测试1：搜索并总结
console.print("\n[bold]测试 1：搜索并总结[/bold]")
r = agent.chat("帮我搜索人工智能的相关知识，然后做一个简要总结")
console.print(f"Agent：{r}", style="bold green")

# 测试2：生成报告
console.print("\n[bold]测试 2：生成研究报告[/bold]")
r = agent.chat("研究一下 LangChain，帮我生成一份研究报告")
console.print(f"Agent：{r}", style="bold green")

# 测试3：完整流程（搜索+总结+报告+保存）
console.print("\n[bold]测试 3：完整研究流程[/bold]")
r = agent.chat("帮我研究 Python 语言，搜索知识，生成报告，保存到文件")
console.print(f"Agent：{r}", style="bold green")

# 验证文件是否保存
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
if os.path.exists(output_dir):
    files = os.listdir(output_dir)
    console.print(f"\n[bold cyan]output 目录中的文件：{files}[/bold cyan]")

console.print("\n练习 5 完成！", style="bold green")
