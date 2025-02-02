import streamlit as st
from chatbot import Chatbot

bot = Chatbot()

st.title("🤖 AI Customer Support Bot")

if "user_id" not in st.session_state:
    st.session_state["user_id"] = st.text_input("Enter your name:", key="name_input")

user_input = st.text_input("Ask me a question:")

if st.button("Get Answer"):
    response = bot.get_answer(user_input, st.session_state["user_id"])
    st.write(f"**Bot:** {response}")

# Quick reply buttons for common questions
st.subheader("Quick Replies")
faq_questions = [
    "What are your support hours?",
    "How can I reset my password?",
    "Can I get a refund?"
]

for question in faq_questions:
    if st.button(question):
        response = bot.get_answer(question, st.session_state["user_id"])
        st.write(f"**Bot:** {response}")
