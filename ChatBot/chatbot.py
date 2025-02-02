import json
import os
import random
import time
import numpy as np
from textblob import TextBlob
from sentence_transformers import SentenceTransformer

class Chatbot:
    def __init__(self, faq_file="faq_data.json"):
        # Load FAQ data
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, faq_file)
        self.faq_data = self.load_faq(file_path)

        # Load NLP model for sentence embeddings
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Precompute embeddings for all FAQ questions and variations
        self.faq_embeddings, self.questions = self.precompute_faq_embeddings()

    def load_faq(self, file_path):
        """Loads the FAQ JSON file."""
        with open(file_path, "r") as file:
            return json.load(file)

    def precompute_faq_embeddings(self):
        """Precomputes embeddings for all FAQ questions and their variations."""
        questions = []
        for faq in self.faq_data:
            # Include the main question and all variations
            questions.append(faq["question"])
            questions.extend(faq.get("variations", []))

        # Compute embeddings
        embeddings = self.model.encode(questions)
        return embeddings, questions

    def analyze_sentiment(self, user_input):
        """Analyzes the sentiment of user input using TextBlob."""
        analysis = TextBlob(user_input)
        if analysis.sentiment.polarity < -0.2:
            return "negative"
        return "neutral/positive"

    def get_fun_response(self):
        """Returns a fun reaction before answering a query."""
        fun_responses = [
            "Great question! 🤔 Let me find the best answer for you...",
            "I'm on it! 🚀 Give me a second...",
            "You're asking the right questions! 🧐 Let me help...",
            "Good one! 🤓 Checking my knowledge base...",
        ]
        return random.choice(fun_responses)

    def type_effect(self, text):
        """Simulates a typing effect for responses."""
        for char in text:
            print(char, end="", flush=True)
            time.sleep(0.03)
        print("\n")

    def find_best_match(self, user_query):
        """Finds the best FAQ match using cosine similarity."""
        user_embedding = self.model.encode([user_query])[0]
        similarities = np.dot(self.faq_embeddings, user_embedding)

        # Get the best matching question index
        best_match_idx = np.argmax(similarities)
        best_match_question = self.questions[best_match_idx]

        # Find corresponding answer
        for faq in self.faq_data:
            if best_match_question == faq["question"] or best_match_question in faq.get("variations", []):
                return faq["answer"]

        return None

    def get_answer(self, user_query, user_id="Guest"):
        """Finds the best response based on user input and sentiment analysis."""
        sentiment = self.analyze_sentiment(user_query)

        # Escalate to human agent if sentiment is negative
        if sentiment == "negative":
            return f"😟 I understand this might be frustrating, {user_id}. Let me escalate your request to a human agent."

        # Fun reaction before answering
        fun_message = self.get_fun_response()

        # Find best FAQ match
        best_answer = self.find_best_match(user_query)
        if best_answer:
            return f"{fun_message}\n\n✅ {user_id}, {best_answer}"

        return f"🤖 I'm sorry, {user_id}. I don't have an answer for that. Let me connect you with an agent."

if __name__ == "__main__":
    bot = Chatbot()
    print("🤖 AI Customer Support Chatbot - Type 'exit' to stop\n")

    user_id = input("👋 Before we begin, may I have your name? ")
    print(f"Hello {user_id}! How can I assist you today? 😊")

    while True:
        query = input(f"{user_id}: ")
        if query.lower() == "exit":
            bot.type_effect(f"Bot: Thank you for using our service, {user_id}. Goodbye! 👋")
            break
        response = bot.get_answer(query, user_id)
        bot.type_effect(f"Bot: {response}")
