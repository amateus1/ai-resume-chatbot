import streamlit as st
import time
from me_chatbot import Me

# 🌐 Layout
st.set_page_config(
    page_title="Meet Hernan 'Al' Mateus — AI Resume Agent",
    layout="wide"
)

# 🎨 Style
st.markdown("""
    <style>
    .main .block-container {
        max-width: 1000px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        margin: auto;
    }
    h1, h2, h3, h4 {
        font-size: 1.2rem !important;
    }
    p, li {
        font-size: 0.95rem !important;
        line-height: 1.6;
    }
    .message-container {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 0.5rem;
    }
    .user-bubble {
        background-color: #f0f8ff;
        padding: 12px 16px;
        border-radius: 16px;
        font-size: 16px;
        line-height: 1.6;
        max-width: 85%;
        text-align: right;
        word-break: break-word;
    }
    </style>
""", unsafe_allow_html=True)

# 🌍 Language options
language_options = {
    "English": {
        "title": "🤖 Meet Hernan 'Al' Mateus — AI Resume Agent",
        "desc": (
            "Welcome! I'm Hernan's digital twin — trained on his global career, MLOps mastery, "
            "love of Thai food, Star Wars, and GPT-powered systems. Ask me anything about his work, "
            "LLMOps projects, career journey, or how to scale AI across 3 clouds and 9 countries 🌏"
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

# 🌐 Language select
selected_lang = st.selectbox("🌐 Language / 语言 / Idioma", list(language_options.keys()))
ui = language_options[selected_lang]

# 🧠 Session state
if "lang_prev" not in st.session_state:
    st.session_state.lang_prev = selected_lang
if st.session_state.lang_prev != selected_lang:
    st.session_state.history = []
    st.session_state.lang_prev = selected_lang

if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# 🤖 Load bot
me = Me()

# 🧢 Header
st.markdown(f"## {ui['title']}")
st.markdown(ui["desc"])

# 💬 History rendering
for user, bot in st.session_state.history:
    with st.chat_message("user", avatar="🧑"):
        st.markdown(
            f"""
            <div class="message-container">
                <div class="user-bubble">
                    {user}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot, unsafe_allow_html=True)

# 🧾 Input box
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

    # ✅ Right-aligned user bubble
    with st.chat_message("user", avatar="🧑"):
        st.markdown(
            f"""
            <div class="message-container">
                <div class="user-bubble">
                    {display_input}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 🧠 Generate assistant response
    response = me.chat(user_input, [])

    # 📡 Stream assistant response
    with st.chat_message("assistant", avatar="🤖"):
        stream_box = st.empty()
        full_response = ""
        for word in response.split():
            full_response += word + " "
            stream_box.markdown(full_response + "▌", unsafe_allow_html=True)
            time.sleep(0.03)
        stream_box.markdown(response, unsafe_allow_html=True)

    # 💾 Save to history
    st.session_state.history.append((display_input, response))
