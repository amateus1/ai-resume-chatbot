import re
import streamlit as st
import time
import requests
from me_chatbot import Me

# 🚀 SILENT KEEP-AWAKE (Hidden from users)
if "ping_count" not in st.session_state:
    st.session_state.ping_count = 0
    st.session_state.last_ping = time.time()

# Silent ping every 10th reload or every 30 minutes
current_time = time.time()
if (st.session_state.ping_count % 10 == 0 or 
    (current_time - st.session_state.last_ping) > 1800):  # 30 minutes
    
    try:
        # Silent ping - no user feedback
        requests.get("https://almateus.me", timeout=5)
        st.session_state.last_ping = current_time
    except:
        pass  # Silent fail

st.session_state.ping_count += 1


# 🌐 Layout
st.set_page_config(
    page_title="Meet 'Al' Mateus — AI Resume Agent",
    layout="wide"
)
# 🎨 ALL STYLING IN ONE PLACE (replaces both st.markdown sections)
st.markdown("""
<style>
    /* === HIDE STREAMLIT BANNERS === */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* === CHAT INPUT STYLING === */
    .stChatInput > div > div {
        background-color: #e6f3ff;
        border-radius: 12px;
    }
   
    /* === MAIN LAYOUT === */
    .block-container {
        padding-top: 1rem;   /* Tight top padding */
        padding-bottom: 1rem;
    }
    .main .block-container {
        max-width: 1000px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        margin: auto;
    }
    
    /* === TYPOGRAPHY === */
    h1, h2, h3, h4 {
        font-size: 1.2rem !important;
    }
    p, li {
        font-size: 0.95rem !important;
        line-height: 1.6;
    }
    
    /* === CHAT BUBBLES === */
    .message-container {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 0.5rem;
    }
    .user-bubble {
        background-color: #f0f8ff;
        padding: 8px 12px;
        border-radius: 16px;
        font-size: 16px;
        line-height: 1.4;
        max-width: 85%;
        text-align: right;
        word-break: break-word;
    }
    
    /* === COMPACT UI ELEMENTS === */
    .stSelectbox > div > div {
        padding: 0.2rem 0.5rem;
        min-height: 1.8rem;
        font-size: 0.9rem;
    }
    div[data-testid="column"] .stButton > button {
        min-height: 1.2rem;
        padding: 0.1rem 0.3rem;
        margin: 0;
        font-size: 0.9rem;
        line-height: 1;
    }
    div[data-testid="column"] {
        display: flex;
        justify-content: center;
    }
    /* .stSelectbox > label {
        display: none;
    } */
</style>
""", unsafe_allow_html=True)

# 🌍 Language options
@st.cache_data(ttl=3600)  # ✅ ADD CACHING
def get_language_options():
    return {
        "English": {
            "desc": "👋 Welcome to **Al Mateus Agentic AI & LLM Engineering leadership** world. Ask anything about my career journey. 🚀",
            "input_placeholder": "Ask something about Al's career...",
            "consult_prompt": "💡 If you'd like a consultation with Al, feel free to share your email below. The chat will continue regardless.",
            "consult_input": "📧 Your email (optional)",
            "consult_success": "✅ Thanks! Al has been notified and will reach out to you soon.",
            "menu": ["📊 Projects", "💼 Experience", "🛠 Skills"]
        },
        "中文 (Chinese)": {
            "desc": "👋 欢迎来到 **Al Mateus 的 Agentic AI 与 LLM 工程领导力**世界。探索他的认证、项目或人机协作团队经验。🚀",
            "input_placeholder": "请输入你想了解 Al 的内容...",
            "consult_prompt": "💡 如果您希望与 Al 进行咨询，请在下方留下您的邮箱。聊天将继续进行。",
            "consult_input": "📧 您的邮箱（可选）",
            "consult_success": "✅ 感谢！Al 已经收到通知，很快会与您联系。",
            "menu": ["📊 项目", "💼 经历", "🛠 技能"]
        },
        "Español": {
            "desc": "👋 Bienvenido al mundo de **Agentic AI & Liderazgo en Ingeniería LLM de Al Mateus**. Explora sus certificaciones, proyectos o experiencia en equipos humano-IA. 🚀",
            "input_placeholder": "Haz una pregunta sobre Al...",
            "consult_prompt": "💡 Si deseas una consulta con Al, puedes dejar tu correo abajo. El chat seguirá normalmente.",
            "consult_input": "📧 Tu correo electrónico (opcional)",
            "consult_success": "✅ ¡Gracias! Al ha sido notificado y se pondrá en contacto contigo pronto.",
            "menu": ["📊 Proyectos", "💼 Experiencia", "🛠 Habilidades"]
        }
    }

language_options = get_language_options()  # ✅ USE CACHED FUNCTION



# Initialize selected language
if 'selected_lang' not in st.session_state:
    st.session_state.selected_lang = "English"

# 🌐 Horizontal Language radio buttons
lang_options = ["🇺🇸 English", "🇨🇳 中文", "🇪🇸 Español"]
lang_mapping = {
    "🇺🇸 English": "English",
    "🇨🇳 中文": "中文 (Chinese)",
    "🇪🇸 Español": "Español"
}
selected_lang_option = st.radio(
    "Language",
    options=lang_options,
    horizontal=True,
    label_visibility="collapsed",
    key="lang_radio"
)

# Direct language access
selected_lang = lang_mapping[selected_lang_option]
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
#st.markdown(f"## {ui['title']}")
st.markdown(ui["desc"])

# 📂 Simple Menu Buttons (under intro)
menu_items = ui["menu"]  # comes from the selected language

# Create responsive columns - 4 on desktop, 2x2 on tablet, 1x4 on mobile
cols = st.columns([1, 1, 1, 1])  # Equal width for all columns

for idx, item in enumerate(menu_items):
    with cols[idx]:
        if st.button(item, key=f"menu_{idx}", use_container_width=True):
            st.session_state.user_input = f"Show me {item}"

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

    # ---- multilingual transform after we've done any email capture ----
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

    # 🧠 Generate assistant response WITH STREAMING
    with st.chat_message("assistant", avatar="🤖"):
        stream_box = st.empty()
        full_response = ""
        
        # ✅ USE STREAMING INSTEAD OF REGULAR CHAT
        try:
            stream_generator = me.chat_stream(user_input, [])
            for chunk, current_full in stream_generator:
                full_response = current_full
                stream_box.markdown(full_response + "▌")
            
            # Final render without cursor
            stream_box.markdown(full_response)
            
        except Exception as e:
            # Fallback to non-streaming if streaming fails
            fallback_response = me.chat(user_input, [])
            stream_box.markdown(fallback_response)
            full_response = fallback_response

    # 💾 Save to history
    st.session_state.history.append((display_input, full_response))
