def analyze_sentiment(text):
    text = text.lower()

    positive_words = [
        "good", "great", "excellent", "helpful",
        "friendly", "amazing", "satisfied", "fast"
    ]

    negative_words = [
        "bad", "poor", "slow", "long", "waiting",
        "issue", "problem", "not working", "worst"
    ]

    positive_score = sum(word in text for word in positive_words)
    negative_score = sum(word in text for word in negative_words)

    if positive_score > negative_score:
        return "Positive", 0.8

    if negative_score > positive_score:
        return "Negative", -0.8

    return "Neutral", 0.0