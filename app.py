# app.py

import streamlit as st
from chatbot import ChatBot

st.set_page_config(page_title="RAG Chatbot", layout="centered")

st.title("🤖 RAG Chatbot (DeepSeek R1 Assistant)")

# Initialize chatbot once
if "bot" not in st.session_state:
    st.session_state.bot = ChatBot()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
user_input = st.chat_input("Ask something...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get bot response
    response = st.session_state.bot.get_response(user_input)

    # Show bot response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)