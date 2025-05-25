import streamlit as st
from me_chatbot import Me

st.set_page_config(page_title="Al Mateus – Virtual Resume Agent", layout="centered")
st.title("🤖 Meet Hernan 'Al' Mateus – AI Resume Agent")

me = Me()

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Ask something about Hernan's background, work, or projects:")

if user_input:
    response = me.chat(user_input, st.session_state.history)
    st.session_state.history.append((user_input, response))

for q, a in st.session_state.history:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Al:** {a}")
