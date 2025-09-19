import streamlit as st
import time
from me_chatbot import Me

# 🌐 Layout
st.set_page_config(
    page_title="Meet Al Mateus — AI Career Agent",
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
        "title": "🤖 Meet 'Al' Mateus — AI Career Agent",
        "desc": (
            "👋 Welcome! I’m Al’s digital twin — part strategist, part engineer, and a little bit of Star Wars geek.  \n\n"
            "I’ve been trained on his journey as a **Global AI/MLOps Architect**, **LLM Engineering leader**, and **Scrum 2.0 pioneer**. "
            "I can walk you through how he builds multi-agent AI systems, scales MLOps pipelines, or even how he’s shaping the next era of work with **Agentic AI teams managed by Agile Product Management tools**.  \n\n"
            "Curious where to start? Ask me about his certifications, engineering projects, leadership style, or how to create an Agentic workforce that blends humans and AI.  \n\n"
            "And if you just want the fun stuff — yes, I’ll happily tell you about Thai food, Teslas, or why GPT-5 and DeepSeek are basically the Millennium Falcon of LLMs. 🚀"
)
        ),
        "input_placeholder": "Ask something about Al's career..."
    },
    "中文 (Chinese)": {
        "title": "🤖 认识 'Al' Mateus —— AI 简历助手",
        "desc": (
            "👋 欢迎！我是 Al 的数字分身 —— 既是战略家，也是工程师，还带点星球大战极客的味道。  \n\n"
            "我基于他作为 **全球 AI/MLOps 架构师**、**LLM 工程领导者** 和 **Scrum 2.0 先行者** 的职业旅程而训练。 "
            "我可以向你展示他如何构建多智能体 AI 系统、扩展 MLOps 流水线，甚至如何通过 **由敏捷产品管理工具驱动的 Agentic AI 团队** 来塑造工作的下一个时代。  \n\n"
            "想知道从哪里开始吗？可以问我他的认证、工程项目、领导风格，或者如何打造一个融合人类与 AI 的 Agentic 团队。  \n\n"
            "当然，如果你只是想聊轻松点的 —— 我也可以分享他对泰国美食、特斯拉赛道体验的热爱，或者为什么 DeepSeek 就像 LLM 世界里的千年隼号。 🚀"
        ),
        "input_placeholder": "请输入你想了解 Al 的内容..."
    },
    "Español": {
        "title": "🤖 Conoce a 'Al' Mateus — Asistente AI",
        "desc": (
            "👋 ¡Bienvenido! Soy el gemelo digital de Al — parte estratega, parte ingeniero y con un toque de fanático de Star Wars.  \n\n"
            "He sido entrenado en su trayectoria como **Arquitecto Global de AI/MLOps**, **líder en Ingeniería de LLMs** y **pionero de Scrum 2.0**. "
            "Puedo mostrarte cómo construye sistemas de IA multi-agente, cómo escala pipelines de MLOps, o incluso cómo está dando forma a la próxima era del trabajo con **equipos Agentic AI gestionados por herramientas de Agile Product Management**.  \n\n"
            "¿Con qué quieres empezar? Pregúntame sobre sus certificaciones, proyectos de ingeniería, estilo de liderazgo o cómo crear una fuerza laboral agéntica que combine humanos y AI.  \n\n"
            "Y si prefieres lo divertido — claro, puedo contarte sobre su pasión por la comida tailandesa, las carreras con Tesla o por qué GPT-5 and DeepSeek son básicamente el Halcón Milenario de los LLMs. 🚀"
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
    for line in response.split("\n"):
        full_response += line + "\n"
        stream_box.markdown(full_response + " ▌")
        time.sleep(0.2)  # simulate typing effect per line
    stream_box.markdown(response)

    # 💾 Save to history
    st.session_state.history.append((display_input, response))
