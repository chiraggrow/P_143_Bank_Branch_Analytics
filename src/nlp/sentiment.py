from transformers import pipeline

sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


def analyze_sentiment(text):
    result = sentiment_model(text)[0]

    label = result["label"]
    confidence = result["score"]

    if label == "POSITIVE":
        sentiment = "Positive"
    else:
        sentiment = "Negative"

    polarity = confidence if sentiment == "Positive" else -confidence

    return sentiment, polarity