def analyze_sentiment(message: str):
    if any(w in message.lower() for w in ["angry","upset","mad","frustrated"]):
        return "negative"
    return "neutral"
