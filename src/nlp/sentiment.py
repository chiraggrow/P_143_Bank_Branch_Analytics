
import re


def analyze_sentiment(text):
    text = text.lower().strip()

    positive_words = [
        "good",
        "great",
        "excellent",
        "helpful",
        "friendly",
        "amazing",
        "satisfied",
        "fast",
        "excellent service",
        "very helpful",
    ]

    negative_words = [
        "bad",
        "poor",
        "slow",
        "long",
        "waiting",
        "issue",
        "problem",
        "not working",
        "worst",
        "unhelpful",
        "rude",
        "unfriendly",
        "terrible",
        "delayed",
        "unsatisfied",
        "dissatisfied",
        "not helpful",
        "poor service",
    ]

    def contains_term(term):
        pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
        return bool(re.search(pattern, text))

    positive_score = sum(
        contains_term(word) for word in positive_words
    )

    negative_score = sum(
        contains_term(word) for word in negative_words
    )

    if positive_score > negative_score:
        return "Positive", 0.8

    if negative_score > positive_score:
        return "Negative", 0.8

    if positive_score == 0 and negative_score == 0:
        return "Neutral", 0.0

    # If positive and negative terms are balanced, avoid
    # incorrectly claiming the feedback is clearly positive.
    return "Negative", 0.5
