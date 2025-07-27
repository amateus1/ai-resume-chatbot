import streamlit as st
import random
from me_chatbot import Me

st.set_page_config(page_title="Meet Hernan 'Al' Mateus — AI Resume Agent", layout="centered")

language_options = {
    "English": {
        "title": "🤖 Meet Hernan 'Al' Mateus — AI Resume Agent",
        "desc": (
            "Ask me anything about Hernan’s MLOps journey, global AI projects, or tech stack. "
            "I’m his digital twin — trained on his resume and career across 9 countries 🌏"
        ),
        "input_placeholder": "Ask something about Hernan..."
    },
    "中文 (Chinese)": {
        "title": "🤖 认识 Hernan 'Al' Mateus —— AI 简历助手",
        "desc": "我是 Hernan 的数字分身——欢迎咨询他的 AI 项目、技术战略或职业旅程 🧠🌏",
        "input_placeholder": "请输入你想了解 Hernan 的内容..."
    },
    "Español": {
        "title": "🤖 Conoce a Hernan 'Al' Mateus — Asistente AI",
        "desc": "Soy el gemelo digital de Hernan — pregúntame sobre sus proyectos, trayectoria y pasión por la IA 🚀",
        "input_placeholder": "Haz una pregunta sobre Hernan..."
    }
}

selected_lang = st.selectbox("🌐 Language / 语言 / Idioma", list(language_options.keys()))
ui = language_options[selected_lang]

if "lang_prev" not in st.session_state:
    st.session_state.lang_prev = selected_lang
if st.session_state.lang_prev != selected_lang:
    st.session_state.history = []
    st.session_state.lang_prev = selected_lang

st.markdown(f"## {ui['title']}")
st.markdown(f"<div style='color:gray;font-size:1.1em;'>{ui['desc']}</div>", unsafe_allow_html=True)

me = Me()
if "history" not in st.session_state:
    st.session_state.history = []

# Input box
user_input = st.chat_input(ui["input_placeholder"], key="chat_input")

if user_input:
    display_input = user_input
    if selected_lang == "中文 (Chinese)":
        user_input = f"请用中文回答：{user_input}"
    elif selected_lang == "Español":
        user_input = f"Por favor responde en español: {user_input}"

    with st.chat_message("user"):
        st.markdown(display_input)

    with st.chat_message("assistant"):
        response_container = st.empty()
        collected = ""

        for chunk in me.chat_stream(user_input):
            collected += chunk
            response_container.markdown(collected.replace("**", "**").replace("\n", "  \n"))

        st.session_state.history.append((display_input, collected))

# Render chat history
for user, bot in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(user)
    with st.chat_message("assistant"):
        st.markdown(bot.replace("**", "**").replace("\n", "  \n"))
