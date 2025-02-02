from textblob import TextBlob

def analyze_sentiment(user_input):
    analysis = TextBlob(user_input)
    if analysis.sentiment.polarity < -0.2:
        return "negative"
    return "neutral/positive"

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        sentiment = analyze_sentiment(user_input)
        print(f"Sentiment: {sentiment}")
