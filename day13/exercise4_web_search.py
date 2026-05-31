"""
Day 13 - 练习 4（挑战）：添加网络搜索功能

任务：让 Agent 能够搜索真实网络信息。

新增内容（标注 [新增]）：
  1. [新增] web_search 工具（使用 requests + 百度搜索）
  2. [新增] 真实信息查询能力
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_core.tools import tool
from rich.console import Console
from rich.panel import Panel

console = Console()

console.print("=" * 60, style="bold blue")
console.print("Day 13 - 练习 4：添加网络搜索", style="bold blue")
console.print("=" * 60, style="bold blue")

# [新增] 网络搜索工具（模拟，实际使用需 requests + 搜索 API）
@tool
def web_search(query: str) -> str:
    """搜索网络获取最新信息。当用户问实时、最新信息时使用此工具。
    参数: query - 搜索关键词"""
    import requests
    from urllib.parse import quote

    try:
        # 使用 DuckDuckGo 的简化搜索
        url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json"
        headers = {"User-Agent": "Mozilla/5.0 (compatible; Day13Agent/1.0)"}
        resp = requests.get(url, headers=headers, timeout=5)

        if resp.status_code == 200:
            data = resp.json()
            abstract = data.get("Abstract", "")
            if abstract:
                return f"搜索结果：{abstract}"
            related = data.get("RelatedTopics", [])
            if related:
                items = []
                for topic in related[:3]:
                    if isinstance(topic, dict) and "Text" in topic:
                        items.append(topic["Text"])
                return "相关信息：\n" + "\n".join(items) if items else f"未找到「{query}」的搜索结果"
            return f"未找到「{query}」的搜索结果"
        return f"搜索出错：HTTP {resp.status_code}"

    except ImportError:
        return "需要安装 requests 库：pip install requests"
    except Exception as e:
        return f"搜索失败：{e}"

# [新增] 测试
console.print("[bold cyan][新增] 测试网络搜索[/bold cyan]")

result = web_search.invoke({"query": "Python编程语言"})
console.print(f"  搜索 Python：{result}", style="green")

result = web_search.invoke({"query": "人工智能"})
console.print(f"  搜索 人工智能：{result}", style="green")

# [新增] 注册到 Agent
console.print("\n[bold cyan][新增] 通过 Agent 调用搜索[/bold cyan]")
try:
    from modules.tools import all_tools, tool_map
    from modules.agent import SmartAgent

    all_tools.append(web_search)
    tool_map[web_search.name] = web_search
    console.print("  已注册 web_search 工具到 Agent", style="green")

    agent = SmartAgent()
    result = agent.tool_mode("搜索一下 Python 编程语言的相关信息")
    console.print(f"  Agent：{result}", style="bold green")

except Exception as e:
    console.print(f"  Agent 调用失败：{e}", style="red")

console.print(Panel(
    "[bold]网络搜索的价值：[/bold]\n"
    "  - 获取实时信息（天气、新闻）\n"
    "  - 弥补 LLM 知识截止日期\n"
    "  - 查询最新技术、文档\n\n"
    "[bold]注意事项：[/bold]\n"
    "  - 需要网络连接\n"
    "  - 注意 API 调用频率\n"
    "  - 验证搜索结果准确性",
    title="网络搜索总结",
    style="green"
))

console.log("\n练习 4 完成！", style="bold green")
