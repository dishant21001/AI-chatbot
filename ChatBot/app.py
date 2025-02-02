import streamlit as st
from chatbot import Chatbot
import time

# Initialize chatbot
bot = Chatbot()

# Streamlit App Configuration
st.set_page_config(page_title="AI Customer Support Chatbot", page_icon="🤖", layout="wide")

# Apply Custom CSS for chat bubbles and layout
st.markdown(
    """
    <style>
        .chat-container {
            max-width: 700px;
            margin: auto;
        }
        .user-message, .bot-message {
            padding: 12px 15px;
            border-radius: 20px;
            max-width: 75%;
            margin-bottom: 10px;
            display: inline-block;
        }
        .user-message {
            background-color: #0078ff;
            color: white;
            align-self: flex-end;
            text-align: right;
            float: right;
            clear: both;
        }
        .bot-message {
            background-color: #f1f1f1;
            color: black;
            text-align: left;
            float: left;
            clear: both;
        }
        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: inline-block;
        }
        .bot-avatar {
            background: url('https://cdn-icons-png.flaticon.com/512/4712/4712037.png') no-repeat center;
            background-size: cover;
        }
        .user-avatar {
            background: url('https://cdn-icons-png.flaticon.com/512/4825/4825038.png') no-repeat center;
            background-size: cover;
        }
        .message-wrapper {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .bot-message-container {
            justify-content: flex-start;
        }
        .user-message-container {
            justify-content: flex-end;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Chat Title
st.markdown("<h1 style='text-align: center; color: #0078ff;'>💬 AI Customer Support Chatbot</h1>", unsafe_allow_html=True)
st.write("👋 Welcome! Ask me anything about our customer support services.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for sender, message in st.session_state.chat_history:
    if sender == "User":
        st.markdown(
            f"""
            <div class='message-wrapper user-message-container'>
                <div class='user-message'>{message}</div>
                <div class='avatar user-avatar'></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class='message-wrapper bot-message-container'>
                <div class='avatar bot-avatar'></div>
                <div class='bot-message'>{message}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# User input section
user_input = st.text_input("Type your message below and press Enter:", key="input")

if st.button("Send"):
    if user_input:
        st.session_state.chat_history.append(("User", user_input))
        response = bot.get_answer(user_input, user_id="User")

        # Simulate typing effect
        time.sleep(1.5)
        st.session_state.chat_history.append(("Bot", response))
        st.rerun()  # Corrected from experimental_rerun

# Quick Reply Buttons for FAQ
st.subheader("📌 Quick Replies")
faq_questions = [
    "What are your support hours?",
    "How can I reset my password?",
    "Can I get a refund?",
    "How do I track my order?"
]

# Use session state to store button clicks and refresh the UI properly
for question in faq_questions:
    if st.button(question, key=f"faq_{question}"):
        st.session_state.chat_history.append(("User", question))
        response = bot.get_answer(question, user_id="User")
        st.session_state.chat_history.append(("Bot", response))
        st.rerun()
