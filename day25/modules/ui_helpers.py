"""Streamlit UI 辅助函数。

这个文件负责：
- 加载 CSS；
- 渲染顶部 Hero 区；
- 渲染信息卡片；
- 渲染聊天消息。

把 UI 辅助函数拆出来，app.py 会更清楚。
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import streamlit as st
except ModuleNotFoundError:
    # 这样处理是为了让 python modules/ui_helpers.py 可以直接运行查看说明。
    # 真正启动 app.py 前，仍然需要 pip install -r requirements.txt 安装 streamlit。
    st = None


DAY25_DIR = Path(__file__).resolve().parents[1]
if str(DAY25_DIR) not in sys.path:
    sys.path.insert(0, str(DAY25_DIR))

from config import ACCENT_COLOR, APP_SUBTITLE, APP_TITLE, PRIMARY_COLOR

try:
    from .schemas import ChatMessage
except ImportError:
    from schemas import ChatMessage


def load_css() -> None:
    """加载 assets/style.css 自定义样式。"""

    if st is None:
        raise RuntimeError("缺少 streamlit，请先安装 day25/requirements.txt。")

    css_path = DAY25_DIR / "assets" / "style.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <style>
        :root {{
            --day25-primary: {PRIMARY_COLOR};
            --day25-accent: {ACCENT_COLOR};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """渲染页面顶部介绍区。"""

    if st is None:
        raise RuntimeError("缺少 streamlit，请先安装 day25/requirements.txt。")

    st.markdown(
        f"""
        <div class="day25-hero">
            <span class="day25-badge">Day 25 · Streamlit</span>
            <h1>{APP_TITLE}</h1>
            <p>{APP_SUBTITLE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_card(mode: str, api_url: str, message_count: int) -> None:
    """渲染侧边栏状态卡片。"""

    if st is None:
        raise RuntimeError("缺少 streamlit，请先安装 day25/requirements.txt。")

    st.markdown(
        f"""
        <div class="day25-card">
            <b>当前模式：</b>{mode}<br>
            <b>消息数量：</b>{message_count}<br>
            <span class="day25-small">API：{api_url}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_message(message: ChatMessage) -> None:
    """渲染单条聊天消息。"""

    if st is None:
        raise RuntimeError("缺少 streamlit，请先安装 day25/requirements.txt。")

    with st.chat_message(message.role):
        st.markdown(message.content)
        st.caption(f"发送时间：{message.created_at}")


if __name__ == "__main__":
    # 练习题答案 5：
    # 如何在 Streamlit 页面中加载 CSS？
    # 如何添加：在 app.py 开头调用 load_css()。
    print("练习题答案 5：UI 辅助函数用于 Streamlit 页面，直接运行只做说明。")
    print("在 app.py 中调用 load_css()、render_hero()、render_message()。")
    if st is None:
        print("当前环境还没有安装 streamlit，运行页面前请先安装 day25/requirements.txt。")
