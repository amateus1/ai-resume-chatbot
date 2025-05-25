import streamlit as st
from me_chatbot import Me

st.set_page_config(
    page_title="Meet Hernan 'Al' Mateus — AI Resume Agent",
    layout="centered",
)

# Custom CSS for ChatGPT-style layout
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
        background-color: #f4f4f4;
        margin-bottom: 1rem;
        font-size: 15px;
    }
    .chat-avatar {
        width: 22px;
        vertical-align: middle;
        margin-right: 8px;
    }
    .user-block {
        background-color: #eaf2ff;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Language support
language_options = {
    "English": {
        "title": "🤖 Meet Hernan 'Al' Mateus — AI Resume Agent",
        "desc": "Welcome! I'm Hernan's digital twin — trained on his global career, MLOps mastery, and GPT-powered systems. Ask me about his projects, career, or cloud AI strategies 🌏",
        "input_placeholder": "Ask something about Hernan...",
        "examples": [
            "Tell about his experience building a consulting practice?",
            "What kind of projects does Hernan lead?",
            "Tell me something personal about Hernan.",
            "What is Hernan’s favorite tech stack?"
        ]
    },
    "中文 (Chinese)": {
        "title": "🤖 认识 Hernan 'Al' Mateus —— AI 简历助手",
        "desc": "欢迎！我是 Hernan 的数字分身，了解他的职业背景、MLOps 专业经验、GPT 系统等。你可以问我有关他的项目、职业发展或 AI 战略 🌏",
        "input_placeholder": "请输入你想了解 Hernan 的内容...",
        "examples": [
            "请介绍他创建咨询实践的经验。",
            "Hernan 领导了哪些类型的项目？",
            "讲一个关于 Hernan 的个人故事。",
            "Hernan 最喜欢的技术栈是什么？"
        ]
    },
    "Español": {
        "title": "🤖 Conoce a Hernan 'Al' Mateus — Asistente de Currículum AI",
        "desc": "¡Bienvenido! Soy el gemelo digital de Hernan, entrenado en su carrera global, experiencia en MLOps y sistemas impulsados por GPT. Pregunta sobre sus proyectos, trayectoria o estrategias de IA en la nube 🌏",
        "input_placeholder": "Haz una pregunta sobre Hernan...",
        "examples": [
            "¿Cómo construyó su práctica de consultoría?",
            "¿Qué tipo de proyectos lidera Hernan?",
            "Cuéntame algo personal sobre Hernan.",
            "¿Cuál es su stack tecnológico favorito?"
        ]
    }
}

# Language selection
selected_lang = st.selectbox("🌐 Select Language / 选择语言 / Selecciona idioma", list(language_options.keys()))

# UI content for selected language
ui = language_options[selected_lang]

# Header and welcome
st.markdown(f"## {ui['title']}")
st.markdown(ui['desc'])

# Chatbot
me = Me()

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Sample questions
with st.expander("💡 Example Questions / 示例问题 / Ejemplos", expanded=True):
    cols = st.columns(2)
    for i, prompt in enumerate(ui['examples']):
        with cols[i % 2]:
            if st.button(prompt):
                st.session_state.user_input = prompt

# User input
user_input = st.text_input(ui["input_placeholder"])

# Handle button-driven input
if st.session_state.user_input:
    user_input = st.session_state.user_input
    st.session_state.user_input = ""

# Prompt + response logic
if user_input:
    prompt_for_llm = user_input
    if selected_lang == "中文 (Chinese)":
        prompt_for_llm = f"请用中文回答：{user_input}"
    elif selected_lang == "Español":
        prompt_for_llm = f"Por favor responde en español: {user_input}"

    response = me.chat(prompt_for_llm, st.session_state.history)
    st.session_state.history.append((user_input, response))

# Display chat history in reverse
for user, bot in reversed(st.session_state.history):
    st.markdown(f"<div class='user-block'>🧑 <strong>You:</strong> {user}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='message-box'><img class='chat-avatar' src='https://img.icons8.com/color/48/000000/robot-2.png'/> <strong>🤖 Al:</strong> {bot}</div>", unsafe_allow_html=True)
