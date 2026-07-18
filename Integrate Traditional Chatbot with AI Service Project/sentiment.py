from transformers import pipeline
# Load Hugging Face sentiment analysis model
sentiment_analyzer = pipeline(
    "sentiment-analysis"
)

def analyze_sentiment(message):
    try:
        result = sentiment_analyzer(message)[0]
        label = result["label"]
        confidence = result["score"]

        if label == "LABEL_1":
            sentiment = "Positive"
        elif label == "LABEL_0":
            sentiment = "Negative"
        else:
            sentiment = label
        return sentiment, confidence
    except Exception as e:
        print("Sentiment Error:", e)
        return "Unknown", 0