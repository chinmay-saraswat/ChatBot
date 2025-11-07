import streamlit as st
from groq import Groq
from dotenv import load_dotenv, find_dotenv
import os
import time

# -----------------------------
# 🔹 Setup
# -----------------------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# Load .env file for API key
load_dotenv(find_dotenv())
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🤖 AI Chatbot")
st.caption("built by **Chinmay Saraswat** 💫")

# -----------------------------
# 🔹 Sidebar
# -----------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=100)
    st.header("About 🤖")
    st.markdown("""
   Just a chat buddy who never sleeps and always answers (mostly right 😅).
    Made with caffeine & code by Chinmay Saraswat 💫
    """)
    mode = st.radio("🧠 Choose Chat Mode", ["Friendly", "Professional", "Coder"])
    st.divider()
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# 🔹 Initialize chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# 🔹 Display chat history
# -----------------------------
for msg in st.session_state.messages:
    avatar = "💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# -----------------------------
# 🔹 User input
# -----------------------------
prompt = st.chat_input("Type your message...")

if prompt:
    # Show user message
    st.chat_message("user", avatar="💻").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Typing animation while waiting
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.markdown("💭 Thinking...")
        time.sleep(0.4)

        # Choose behavior based on sidebar mode
        if mode == "Friendly":
            system_prompt = "You are a kind and friendly assistant who responds casually."
        elif mode == "Professional":
            system_prompt = "You are a polite and formal AI assistant for professional users."
        else:
            system_prompt = "You are a coding expert who explains technical topics clearly and simply."

        # Generate assistant response
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages
                ],
            )
            # ✅ Initialize full_response before using it
            full_response = response.choices[0].message.content.strip()

            # Typing effect
            displayed_text = ""
            for word in full_response.split():
                displayed_text += word + " "
                message_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.03)

            # Final clean response
            message_placeholder.markdown(full_response)

            # Save assistant response
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
