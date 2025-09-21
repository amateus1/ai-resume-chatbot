import re
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
        padding-top: 0.5rem;  
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

    /* Desktop: nav column */
    @media (min-width: 769px) {
        [data-testid="column"]:last-of-type {
            max-width: 180px !important;
        }
    }

    /* Mobile: hide nav completely */
    @media (max-width: 768px) {
        [data-testid="column"]:last-of-type {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            overflow: hidden !important;
        }
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
        ),
        "menu": ["📊 Projects", "💼 Experience", "🛠 Skills", "🎓 Certifications"],
        "input_placeholder": "Ask something about Al's career...",
        "consult_prompt": "💡 If you'd like a consultation with Al, feel free to share your email below. The chat will continue regardless.",
        "consult_input": "📧 Your email (optional)",
        "consult_success": "✅ Thanks! Al has been notified and will reach out to you soon."        
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
        "menu": ["📊 项目", "💼 经历", "🛠 技能", "🎓 认证"],
        "input_placeholder": "请输入你想了解 Al 的内容...",
        "consult_prompt": "💡 如果您希望与 Al 进行咨询，请在下方留下您的邮箱。聊天将继续进行。",
        "consult_input": "📧 您的邮箱（可选）",
        "consult_success": "✅ 感谢！Al 已经收到通知，很快会与您联系。"
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
        "menu": ["📊 Proyectos", "💼 Experiencia", "🛠 Habilidades", "🎓 Certificaciones"],
        "input_placeholder": "Haz una pregunta sobre Al...",
        "consult_prompt": "💡 Si deseas una consulta con Al, puedes dejar tu correo abajo. El chat seguirá normalmente.",
        "consult_input": "📧 Tu correo electrónico (opcional)",
        "consult_success": "✅ ¡Gracias! Al ha sido notificado y se pondrá en contacto contigo pronto."
    }
}

# ✅ Initialize session_state variables safely
if "history" not in st.session_state:
    st.session_state.history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "prompt_count" not in st.session_state:
    st.session_state.prompt_count = 0
if "email" not in st.session_state:
    st.session_state.email = None

# 🌐 Language select
selected_lang = st.radio(
    "",
    list(language_options.keys()),
    horizontal=True
)
ui = language_options[selected_lang]

# 🤖 Load bot
me = Me()

# 🧢 Intro + Nav (render nav only on desktop)
col_intro, col_nav = st.columns([4, 1])

with col_intro:
    st.markdown(f"## {ui['title']}")
    st.markdown(ui["desc"])

# ✅ Render nav only if desktop (>=769px) by injecting a JS width check
is_mobile = st.session_state.get("is_mobile", None)
if is_mobile is None:
    st.markdown(
        """
        <script>
        const width = window.innerWidth;
        const isMobile = width <= 768;
        window.parent.postMessage({isMobile: isMobile}, "*");
        </script>
        """,
        unsafe_allow_html=True
    )
    st.session_state.is_mobile = False  # fallback default

# Only render nav if not mobile
if not st.session_state.get("is_mobile", False):
    with col_nav:
        st.markdown("### 📂 Menu")
        for idx, item in enumerate(ui["menu"]):
            if st.button(item, key=f"menu_{idx}"):
                st.session_state.user_input = f"Show me {item}"


# 💬 History
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

# 🧾 Input
user_input = st.chat_input(ui["input_placeholder"])

# === Chat logic continues (unchanged) ===
if st.session_state.user_input:
    user_input = st.session_state.user_input
    st.session_state.user_input = ""

if user_input:
    st.session_state.prompt_count += 1
    display_input = user_input

    contact_keywords = ["contact", "reach", "connect", "talk", "email", "get in touch"]

    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", user_input)
    if email_match and not st.session_state.get("email"):
        from me_chatbot import send_email_alert
        user_email = email_match.group(0)
        try:
            send_email_alert(user_email)
            st.success(f"✅ Thanks! Al has been notified of your email: {user_email}")
            st.session_state.email = user_email
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")

    if selected_lang == "中文 (Chinese)":
        user_input = f"请用中文回答：{user_input}"
    elif selected_lang == "Español":
        user_input = f"Por favor responde en español: {user_input}"

    should_suggest_email = (
        (st.session_state.prompt_count >= 3 or any(
            kw in display_input.lower() for kw in contact_keywords
        ))
        and not st.session_state.email
        and not st.session_state.get("email_prompt_shown", False)
    )

    if should_suggest_email:
        st.markdown(ui["consult_prompt"])
        st.session_state.email_prompt_shown = True
            

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

    response = me.chat(user_input, [])

    with st.chat_message("assistant", avatar="🤖"):
        stream_box = st.empty()
        full_response = ""
        for char in response:
            full_response += char
            stream_box.markdown(full_response + "▌")
            time.sleep(0.01)
        stream_box.markdown(response)

    st.session_state.history.append((display_input, response))
