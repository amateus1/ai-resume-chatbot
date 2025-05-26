import streamlit as st
from me_chatbot import Me

st.set_page_config(
    page_title="Meet Hernan 'Al' Mateus — AI Resume Agent",
    layout="centered",
)

# Language selector UI
language_options = {
    "English": {
        "title": "🤖 Meet Hernan 'Al' Mateus — AI Resume Agent",
        "desc": "I'm Hernan's digital twin — ask me anything about AI, MLOps, cloud strategy, or why cats > meetings 🐾",
        "input_placeholder": "Ask something about Hernan...",
        "examples": [
            "What projects has Hernan led?",
            "What’s his MLOps experience?",
            "OpenAI, DeepSeek experience?",
            "What’s his favorite tech stack?"
        ]
    },
    "中文 (Chinese)": {
        "title": "🤖 认识 Hernan 'Al' Mateus —— AI 简历助手",
        "desc": "我是 Hernan 的数字分身——欢迎咨询他的 AI 项目、技术战略或职业旅程 🧠🌏",
        "input_placeholder": "请输入你想了解 Hernan 的内容...",
        "examples": [
            "他领导过哪些项目？",
            "他有 MLOps 经验吗？",
            "OpenAI、DeepSeek 的经验？",
            "他最喜欢的技术栈是？"
        ]
    },
    "Español": {
        "title": "🤖 Conoce a Hernan 'Al' Mateus — Asistente AI",
        "desc": "Soy el gemelo digital de Hernan — pregúntame sobre sus proyectos, trayectoria y pasión por la IA 🚀",
        "input_placeholder": "Haz una pregunta sobre Hernan...",
        "examples": [
            "¿Qué proyectos ha liderado?",
            "¿Tiene experiencia en MLOps?",
            "¿Experiencia con OpenAI y DeepSeek?",
            "¿Cuál es su stack favorito?"
        ]
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
st.markdown(ui["desc"])

me = Me()

if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

with st.expander("💡 Examples", expanded=True):
    cols = st.columns(2)
    for i, example in enumerate(ui["examples"]):
        with cols[i % 2]:
            if st.button(example):
                st.session_state.user_input = example

user_input = st.chat_input(ui["input_placeholder"])

if st.session_state.user_input:
    user_input = st.session_state.user_input
    st.session_state.user_input = ""

if user_input:
    display_input = user_input
    if selected_lang == "中文 (Chinese)":
        user_input = f"请用中文回答：{user_input}"
    elif selected_lang == "Español":
        user_input = f"Por favor responde en español: {user_input}"

    response = me.chat(user_input, [])
    st.session_state.history.append((display_input, response))

for user, bot in reversed(st.session_state.history):
    st.markdown(f"**🧑 You:** {user}")
    st.markdown(f"**🤖 Al:** {bot}")
