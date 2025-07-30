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
        background-color: #eef6ff;
        padding: 10px 16px;
        border-radius: 12px;
        font-size: 0.95rem;
        max-width: 85%;
        text-align: right;
        word-break: break-word;
    }
    .assistant-bubble {
        background-color: #f8f8f8;
        padding: 10px 16px;
        border-radius: 12px;
        font-size: 0.95rem;
        max-width: 85%;
        text-align: left;
        word-break: break-word;
    }
    </style>
""", unsafe_allow_html=True)

# 🌍 Language options
language_options = {
    "English": {
        "title": "🤖 Meet 'Al' Mateus — AI Resume Agent",
        "desc": (
            "Welcome! I'm Al's digital twin — trained on his global career, Agile Product Management, Agentic LLM Engineering experience, MLOps mastery, "
            "love of Thai food, Star Wars, and GPT-powered systems. Ask me anything about his work or education, "
            "such as: Certifications, LLM engineering projects, MLOps tools used in projects, career journey, or how to create an Agentic workforce."
        ),
        "input_placeholder": "Ask something about Al's career..."
    },
    "中文 (Chinese)": {
        "title": "🤖 认识 'Al' Mateus —— AI 简历助手",
        "desc": (
            "欢迎！我是 Al 的数字分身 —— 基于他在全球范围内的职业经历、敏捷产品管理、Agentic 大语言模型工程、MLOps 精通程度、 🧠🌏"
            "对泰国美食、星球大战以及基于 GPT 的系统的热爱训练而成。你可以向我询问他在工作或教育方面的任何内容，"
            "比如：认证资质、LLM 工程项目、项目中使用的 MLOps 工具、职业发展历程，或者如何打造一个 Agentic 人工智能团队。"
        ),
        "input_placeholder": "请输入你想了解 Al 的内容..."
    },
    "Español": {
        "title": "🤖 Conoce a 'Al' Mateus — Asistente AI",
        "desc": (
            "¡Bienvenido! Soy el gemelo digital de Al — entrenado con base en su trayectoria profesional global, experiencia en Gestión Ágil de Productos, "
            "Ingeniería de LLMs Agénticos, dominio de MLOps, amor por la comida tailandesa, Star Wars y sistemas potenciados por GPT. "
            "Pregúntame lo que quieras sobre su trabajo o formación, como por ejemplo: certificaciones, proyectos de ingeniería con LLMs, "
            "herramientas de MLOps utilizadas en proyectos, trayectoria profesional o cómo crear una fuerza laboral agéntica. 🚀"
        ),
        "input_placeholder": "Haz una pregunta sobre Al..."
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
    st.markdown(
        f"""
        <div class="message-container">
            <div class="user-bubble">{user}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div class="assistant-bubble">{bot}</div>
        """,
        unsafe_allow_html=True
    )

# 🧾 Input box
user_input = st.chat_input(ui["input_placeholder"])

if st.session_state.user_input:
    user_input = st.session_state.user_input
    st.session_state.user_input = ""

if user_input:
    display_input = user_input

    # 🌐 Multilingual Prompt Handling
    if selected_lang == "中文 (Chinese)":
        user_input = f"请用中文回答：{user_input}"
    elif selected_lang == "Español":
        user_input = f"Por favor responde en español: {user_input}"

    # 👉 Check for greeting trigger
    if user_input.lower() in ["hello", "hi", "你好", "hola"]:
        response = (
            "👋 Hello there! I’m “Al” Mateus’ digital twin — your playful, insightful guide to all things "
            "**Agentic AI, Agile Product Management**, and **MLOps wizardry**.\n\n"
            "### 🤖 What can I do for you?\n"
            "I'm built to help you understand Al’s:\n"
            "• **Career path** — from leading Agile transformations to building autonomous AI systems\n"
            "• **Engineering expertise** — including **CrewAI, LangGraph, LangChain, AutoGen**, and more\n"
            "• **Project insights** — real-world stories, challenges, and results from finance, pharma, e-commerce, etc.\n"
            "• **Fun stuff** — from Star Wars geek-outs to how he uses AI in everyday life\n\n"
            "### 💬 Ask me about:\n"
            "• Certifications or engineering projects\n"
            "• MLOps tools used in production\n"
            "• Building an Agentic AI team\n"
            "• Or even *why GPT-4o is like the Millennium Falcon of LLMs* 🛸\n\n"
            "Let’s dive in — what would you like to explore first?"
        )
    else:
        # 🧠 Generate assistant response
        response = me.chat(user_input, [])

    # ✅ Display user message
    st.markdown(
        f"""
        <div class="message-container">
            <div class="user-bubble">{display_input}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 📡 Stream assistant response
    stream_box = st.empty()
    full_response = ""
    for word in response.split():
        full_response += word + " "
        stream_box.markdown(
            f"<div class='assistant-bubble'>{full_response}▌</div>",
            unsafe_allow_html=True
        )
        time.sleep(0.03)
    stream_box.markdown(
        f"<div class='assistant-bubble'>{response}</div>",
        unsafe_allow_html=True
    )

    # 💾 Save to history
    st.session_state.history.append((display_input, response))
