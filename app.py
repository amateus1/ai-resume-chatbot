import streamlit as st
from me_chatbot import Me

st.set_page_config(
    page_title="Meet Hernan 'Al' Mateus – AI Resume Agent",
    layout="centered",
)

# Custom styling
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

# Page title and intro
st.markdown("## 🤖 Meet Hernan 'Al' Mateus — AI Resume Agent")
st.markdown(
    "Welcome! I'm Hernan's digital twin — trained on his global career, MLOps mastery, love of Thai food, "
    "Star Wars, and GPT-powered systems. Ask me anything about his work, LLMOps projects, career journey, "
    "or how to scale AI across 3 clouds and 9 countries 🌏"
)

# Language selector
lang = st.radio("🌐 Language", ["English", "中文 (Chinese)"], horizontal=True)

# Initialize chatbot
me = Me()

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Sample prompts
with st.expander("💡 Example questions", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Tell about his consulting practice"):
            st.session_state.user_input = "Tell about his experience building a consulting practice?"
        if st.button("What kind of projects does he lead?"):
            st.session_state.user_input = "What kind of projects does Hernan lead?"
    with col2:
        if st.button("Tell me something personal"):
            st.session_state.user_input = "Tell me something personal about Hernan."
        if st.button("Favorite tech stack?"):
            st.session_state.user_input = "What is Hernan’s favorite tech stack?"

# Input
user_input = st.text_input("Ask something about Hernan's background, work, or projects:")

if st.session_state.user_input:
    user_input = st.session_state.user_input
    st.session_state.user_input = ""

# Respond
if user_input:
    if lang == "中文 (Chinese)":
        user_input = f"请用中文回答：{user_input}"
    response = me.chat(user_input, st.session_state.history)
    st.session_state.history.append((user_input, response))

# Display messages
for user, bot in reversed(st.session_state.history):
    st.markdown(f"**🧑 You:** {user}")
    st.markdown(f"<div class='message-box'><img class='chat-avatar' src='https://img.icons8.com/color/48/000000/robot-2.png'/> <strong>🤖 Al:</strong> {bot}</div>", unsafe_allow_html=True)
