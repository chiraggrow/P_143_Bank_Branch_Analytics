from textblob import TextBlob


def analyze_sentiment(text):
    """
    Analyze sentiment of customer feedback.
    """

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, polarity