from src.nlp.sentiment import analyze_sentiment


def test_positive_sentiment():
    sentiment, polarity = analyze_sentiment(
        "The staff was very helpful and friendly."
    )

    assert sentiment == "Positive"
    assert polarity > 0


def test_negative_sentiment():
    sentiment, polarity = analyze_sentiment(
        "The waiting time was too long."
    )

    assert sentiment == "Negative"
    assert polarity < 0