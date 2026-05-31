"""
Day 13 - 综合 AI 助手

运行方式：python main.py

整合 Day 8-12 所有知识：
  Day 8: LLM + Prompt
  Day 9: Memory 对话记忆
  Day 10: Tools 工具系统
  Day 11: Agent 智能代理
  Day 12: RAG 文档问答
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # 运行 06_chat_interface.py
    exec(open(os.path.join(os.path.dirname(__file__), "06_chat_interface.py")).read())
