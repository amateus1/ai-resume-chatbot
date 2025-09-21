import re
import streamlit as st
import time
from me_chatbot import Me

# 🌐 Layout
st.set_page_config(
    page_title="Meet 'Al' Mateus — AI Resume Agent",
    layout="wide"
)
# tighten top padding
st.markdown("""
<style>
.block-container {
    padding-top: 0rem;   /* default is ~6rem */
}
</style>
""", unsafe_allow_html=True)

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
/* COMPACT DROPDOWN */
.stSelectbox > div > div {
    padding: 0.2rem 0.5rem;
    min-height: 1.8rem;
    font-size: 0.9rem;
}
.stSelectbox > label {
    display: none;
}
    </style>
""", unsafe_allow_html=True)

# 🌍 Language options
language_options = {
    "English": {
        "title": "🤖 Al Mateus Career Agent",
        "desc": "👋 Agentic AI & LLM Engineering leader. Explore his certifications, projects, or human-AI workforce experience. 🚀",
        "input_placeholder": "Ask something about Al's career...",
        "consult_prompt": "💡 If you'd like a consultation with Al, feel free to share your email below. The chat will continue regardless.",
        "consult_input": "📧 Your email (optional)",
        "consult_success": "✅ Thanks! Al has been notified and will reach out to you soon.",
        "menu": ["📊 Projects", "💼 Experience", "🛠 Skills", "🎓 Certifications"]        
    },
    "中文 (Chinese)": {
        "title": "🤖 认识 'Al' Mateus —— AI 简历助手",
        "desc": (
            "👋 欢迎！我是 Al 的数字分身 —— 既是战略家，也是工程师，还带点星球大战极客的味道。  \n\n"
            "我基于他作为 **全球 AI/MLOps 架构师**、**LLM 工程领导者** 和 **Scrum 2.0 先行者** 的职业旅程而训练。 "
            "我可以向你展示他如何构建多智能体 AI 系统、扩展 MLOps 流水线，甚至如何通过 **由敏捷产品管理工具驱动的 Agentic AI 团队** 来塑造工作的下一个时代。  \n\n"
            "想知道从哪里开始吗？可以问我他的认证、工程项目、领导风格，或者如何打造一个融合人类与 AI 的 Agentic 团队  🚀。"            
        ),
        "input_placeholder": "请输入你想了解 Al 的内容...",
        "consult_prompt": "💡 如果您希望与 Al 进行咨询，请在下方留下您的邮箱。聊天将继续进行。",
        "consult_input": "📧 您的邮箱（可选）",
        "consult_success": "✅ 感谢！Al 已经收到通知，很快会与您联系。",
        "menu": ["📊 项目", "💼 经历", "🛠 技能", "🎓 认证"]
    },
    "Español": {
        "title": "🤖 Conoce a 'Al' Mateus — Asistente AI",
        "desc": (
            "👋 ¡Bienvenido! Soy el gemelo digital de Al — parte estratega, parte ingeniero y con un toque de fanático de Star Wars.  \n\n"
            "He sido entrenado en su trayectoria como **Arquitecto Global de AI/MLOps**, **líder en Ingeniería de LLMs** y **pionero de Scrum 2.0**. "
            "Puedo mostrarte cómo construye sistemas de IA multi-agente, cómo escala pipelines de MLOps, o incluso cómo está dando forma a la próxima era del trabajo con **equipos Agentic AI gestionados por herramientas de Agile Product Management**.  \n\n"
            "¿Con qué quieres empezar? Pregúntame sobre sus certificaciones, proyectos de ingeniería, estilo de liderazgo o cómo crear una fuerza laboral agéntica que combine humanos y AI 🚀."            
        ),
        "input_placeholder": "Haz una pregunta sobre Al...",
        "consult_prompt": "💡 Si deseas una consulta con Al, puedes dejar tu correo abajo. El chat seguirá normalmente.",
        "consult_input": "📧 Tu correo electrónico (opcional)",
        "consult_success": "✅ ¡Gracias! Al ha sido notificado y se pondrá en contacto contigo pronto.",
        "menu": ["📊 Proyectos", "💼 Experiencia", "🛠 Habilidades", "🎓 Certificaciones"]
    }
}
# 🌐 Simple Language select - dropdown approach
language_options_map = {
    "🇺🇸 English": "English",
    "🇨🇳 中文": "中文 (Chinese)", 
    "🇪🇸 Español": "Español"
}

# Initialize selected language
if 'selected_lang' not in st.session_state:
    st.session_state.selected_lang = "English"

# Display compact dropdown
selected_option = st.selectbox(
    "",
    options=list(language_options_map.keys()),
    label_visibility="collapsed",
    key="lang_select"
)

# Map back to actual language key
selected_lang = language_options_map[selected_option]
st.session_state.selected_lang = selected_lang
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

if "prompt_count" not in st.session_state:
    st.session_state.prompt_count = 0

# >>> START CHANGE 1: add flags for email tracking <<<
if "email" not in st.session_state:
    st.session_state.email = None
if "email_prompt_shown" not in st.session_state:
    st.session_state.email_prompt_shown = False
# >>> END CHANGE 1 <<<

# 🤖 Load bot
me = Me()

# 🧢 Header
st.markdown(f"## {ui['title']}")
st.markdown(ui["desc"])

# 📂 Simple Menu Buttons (under intro)
menu_items = ui["menu"]  # comes from the selected language

# Create responsive columns - 4 on desktop, 2x2 on tablet, 1x4 on mobile
cols = st.columns([1, 1, 1, 1])  # Equal width for all columns

for idx, item in enumerate(menu_items):
    with cols[idx]:
        if st.button(item, key=f"menu_{idx}", use_container_width=True):
            st.session_state.user_input = f"Show me {item}"
#cols = st.columns(len(menu_items))
#for idx, item in enumerate(menu_items):
#    with cols[idx]:
#        if st.button(item, key=f"menu_{idx}"):
#            st.session_state.user_input = f"Show me {item}"

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
    st.session_state.prompt_count += 1
    display_input = user_input

    contact_keywords = ["contact", "reach", "connect", "talk", "email", "get in touch"]

    # 📧 Capture email typed directly in chat
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

    # ---- multilingual transform after we’ve done any email capture ----
    if selected_lang == "中文 (Chinese)":
        user_input = f"请用中文回答：{user_input}"
    elif selected_lang == "Español":
        user_input = f"Por favor responde en español: {user_input}"

    # ---- show email input ONCE if conditions match and we don't have an email yet ----
    should_suggest_email = (
        (st.session_state.prompt_count >= 3 or any(
            kw in display_input.lower() for kw in contact_keywords
        ))
        and not st.session_state.email
        and not st.session_state.get("email_prompt_shown", False)
    )

    if should_suggest_email:
        st.markdown(ui["consult_prompt"])
        st.session_state.email_prompt_shown = True  # ✅ only show once
            

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
        for char in response:
            full_response += char
            stream_box.markdown(full_response + "▌")   # ✅ no unsafe_allow_html
            time.sleep(0.01)
        stream_box.markdown(response)  # ✅ final clean render with Markdown

    # 💾 Save to history
    st.session_state.history.append((display_input, response))
