import streamlit as st
from me_chatbot import Me

st.set_page_config(
    page_title="Meet Hernan 'Al' Mateus – AI Resume Agent",
    layout="centered",
)

# Styling
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        font-size: 16px;
        padding: 0.75rem;
    }
    .stButton > button {
        background-color: #f63366;
        color: white;
        border-radius: 5px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        margin: 5px 0;
    }
    .message-box {
        border-radius: 8px;
        padding: 1rem;
        background-color: #f3f3f3;
        margin-bottom: 1rem;
    }
    .chat-avatar {
        width: 24px;
        vertical-align: middle;
        margin-right: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Language toggle
lang = st.radio("🌐 Language", ["English", "中文 (Chinese)"], horizontal=True)

# Language-specific text
title_text = "🤖 Meet Hernan 'Al' Mateus — AI Resume Agent" if lang == "English" else "🤖 认识 Hernan 'Al' Mateus —— AI 简历助手"
desc_text = (
    "Welcome! I'm Hernan's digital twin — trained on his global career, MLOps mastery, love of Thai food, "
    "Star Wars, and GPT-powered systems. Ask me anything about his work, LLMOps projects, career journey, "
    "or how to scale AI across 3 clouds and 9 countries 🌏"
    if lang == "English" else
    "欢迎！我是 Hernan 的数字分身——了解他的全球职业背景、MLOps 专业知识、对泰国美食的热爱、星球大战和 GPT 系统。"
    "你可以问我有关他工作经验、AI 项目、职业发展或跨国部署 AI 的问题 🌏"
)

example_prompts = {
    "English": [
        "Tell about his experience building a consulting practice?",
        "What kind of projects does Hernan lead?",
        "Tell me something personal about Hernan.",
        "What is Hernan’s favorite tech stack?"
    ],
    "中文 (Chinese)": [
        "请介绍他创建咨询实践的经验。",
        "Hernan 领导了哪些类型的项目？",
        "讲一个关于 Hernan 的个人故事。",
        "Hernan 最喜欢的技术栈是什么？"
    ]
}

# Display UI
st.markdown(f"## {title_text}")
st.markdown(desc_text)

# Chatbot instance
me = Me()

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Examples
with st.expander("💡 示例问题 / Example Questions", expanded=True):
    cols = st.columns(2)
    for i, prompt in enumerate(example_prompts[lang]):
        with cols[i % 2]:
            if st.button(prompt):
                st.session_state.user_input = prompt

# Input
user_input = st.text_input("Ask something about Hernan..." if lang == "English" else "请输入你想了解 Hernan 的内容...")

if st.session_state.user_input:
    user_input = st.session_state.user_input
    st.session_state.user_input = ""

# Chat handling
if user_input:
    display_input = user_input  # Keep clean version for UI
    send_input = f"请用中文回答：{user_input}" if lang == "中文 (Chinese)" else user_input

    response = me.chat(send_input, st.session_state.history)
    st.session_state.history.append((display_input, response))

# History display
for user, bot in reversed(st.session_state.history):
    st.markdown(f"**🧑 You:** {user}")
    st.markdown(f"<div class='message-box'><img class='chat-avatar' src='https://img.icons8.com/color/48/000000/robot-2.png'/> <strong>🤖 Al:</strong> {bot}</div>", unsafe_allow_html=True)
