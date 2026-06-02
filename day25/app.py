"""Day25 Streamlit 前端主页面。

启动方式：
    cd day25
    streamlit run app.py

这个页面支持两种模式：
1. 本地模拟模式：不需要后端，直接使用 LocalAgent；
2. API 模式：调用 Day23 的 /api/agent/chat 接口。
"""

from __future__ import annotations

import streamlit as st

from config import AGENT_API_URL, DEFAULT_MODE
from modules.api_client import AgentAPIClient
from modules.chat_store import ChatStore
from modules.local_agent import LocalAgent
from modules.ui_helpers import load_css, render_hero, render_message, render_status_card


def get_chat_store() -> ChatStore:
    """从 session_state 中获取聊天记录。"""

    if "chat_store" not in st.session_state:
        st.session_state.chat_store = ChatStore()
    return st.session_state.chat_store


def answer_question(question: str, mode: str, api_url: str, use_tools: bool) -> str:
    """根据当前模式回答问题。"""

    if mode == "api":
        client = AgentAPIClient(api_url)
        response = client.chat(question, use_tools=use_tools)
    else:
        response = LocalAgent().answer(question)

    used_tools = "、".join(response.used_tools) if response.used_tools else "无"
    return f"{response.answer}\n\n---\n来源：{response.source}\n使用工具：{used_tools}"


def main() -> None:
    """渲染 Streamlit 页面。"""

    st.set_page_config(
        page_title="Day25 AI Agent Web 界面",
        page_icon="🤖",
        layout="wide",
    )
    load_css()
    render_hero()

    store = get_chat_store()

    with st.sidebar:
        st.header("控制面板")
        mode = st.radio(
            "运行模式",
            options=["local", "api"],
            index=0 if DEFAULT_MODE == "local" else 1,
            help="local 不需要后端；api 会调用 Day23 的 Agent API。",
        )
        api_url = st.text_input("Agent API 地址", value=AGENT_API_URL)
        use_tools = st.checkbox("允许 Agent 使用工具", value=True)

        if st.button("清空聊天记录"):
            store.clear()
            st.rerun()

        render_status_card(mode, api_url, store.count())

        st.markdown("### 运行提示")
        st.info("如果选择 api 模式，请先启动 Day23：cd day23 && uvicorn main:app --reload")

    st.markdown("### 对话区")

    if store.count() == 0:
        st.markdown(
            """
            <div class="day25-card">
            你可以先问：<b>Day25 前端页面要学什么？</b><br>
            也可以试试：<b>2 + 3 * 4 等于多少？</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

    for message in store.messages:
        render_message(message)

    question = st.chat_input("输入你的问题，例如：Day25 如何连接后端 API？")
    if question:
        store.add_user_message(question)
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Agent 正在思考..."):
                answer = answer_question(question, mode, api_url, use_tools)
                st.markdown(answer)

        store.add_assistant_message(answer)


if __name__ == "__main__":
    # 练习题答案 6：
    # 如何启动 Day25 Web 页面？
    # 如何添加：在 day25 目录运行 streamlit run app.py。
    main()
