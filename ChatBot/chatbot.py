import json
import os
import random
import time
import numpy as np
from textblob import TextBlob
from sentence_transformers import SentenceTransformer
import faiss

class Chatbot:
    def __init__(self, faq_file="faq_data.json"):
        # Load FAQ data
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, faq_file)
        self.faq_data = self.load_faq(file_path)

        # Load NLP model for FAQ matching
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Store conversation memory
        self.conversation_history = []

        # Precompute FAQ embeddings and build FAISS index
        self.faq_index, self.questions = self.build_faq_index()

    def load_faq(self, file_path):
        """Loads the FAQ JSON file."""
        with open(file_path, "r") as file:
            return json.load(file)

    def build_faq_index(self):
        """Builds a FAISS index for fast FAQ retrieval."""
        questions = []
        for faq in self.faq_data:
            questions.append(faq["question"])
            questions.extend(faq.get("variations", []))

        # Compute sentence embeddings for FAQs
        embeddings = self.model.encode(questions)

        # Create FAISS index for fast nearest neighbor search
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        return index, questions

    def analyze_sentiment(self, user_input):
        """Analyzes user sentiment using TextBlob."""
        analysis = TextBlob(user_input)
        if analysis.sentiment.polarity < -0.2:
            return "negative"
        return "neutral/positive"

    def find_best_match(self, user_query):
        """Finds the best FAQ match using FAISS similarity search."""
        query_embedding = self.model.encode([user_query])
        _, idx = self.faq_index.search(query_embedding, 1)

        best_match_question = self.questions[idx[0][0]]

        for faq in self.faq_data:
            if best_match_question == faq["question"] or best_match_question in faq.get("variations", []):
                return faq["answer"]

        return None

    def generate_general_response(self, user_query):
        """Handles general customer support queries without external APIs."""
        general_knowledge = {
            "order tracking": "To track your order, please visit our order tracking page and enter your order ID.",
            "refund policy": "Refunds are available within 30 days of purchase. Please contact support for assistance.",
            "shipping time": "Standard shipping takes 5-7 business days. Express shipping is available for an additional charge.",
            "product warranty": "All our products come with a one-year warranty. If you experience issues, contact support.",
            "payment methods": "We accept credit cards, PayPal, and Apple Pay."
        }

        # Search for a predefined response
        for key, response in general_knowledge.items():
            if key in user_query.lower():
                return response

        return "I'm sorry, I don't have an answer for that. Please check our help center or contact support."

    def get_answer(self, user_query, user_id="Guest"):
        """Handles customer support requests using FAQ, sentiment analysis, and general responses."""
        sentiment = self.analyze_sentiment(user_query)

        if sentiment == "negative":
            return f"😟 I understand this might be frustrating, {user_id}. Let me escalate your request to a human agent."

        # Store user input in conversation history
        self.conversation_history.append(f"{user_id}: {user_query}")

        # Find best FAQ match
        best_answer = self.find_best_match(user_query)
        if best_answer:
            return f"✅ {user_id}, {best_answer}"

        # If no FAQ match, generate a general response
        return f"🤖 {user_id}, {self.generate_general_response(user_query)}"

if __name__ == "__main__":
    bot = Chatbot()
    print("🤖 AI Customer Support Chatbot - Type 'exit' to stop\n")

    user_id = input("👋 Before we begin, may I have your name? ")
    print(f"Hello {user_id}! How can I assist you today? 😊")

    while True:
        query = input(f"{user_id}: ")
        if query.lower() == "exit":
            print(f"Bot: Thank you for using our service, {user_id}. Goodbye! 👋")
            break
        response = bot.get_answer(query, user_id)
        print("Bot:", response)
