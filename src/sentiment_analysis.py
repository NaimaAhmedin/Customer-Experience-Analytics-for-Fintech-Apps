import os
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ---------------- CONFIG ----------------
PROCESSED_DIR = "../data/processed"
INPUT_FILE = f"{PROCESSED_DIR}/cleaned_reviews.csv"
OUTPUT_FILE = f"{PROCESSED_DIR}/processed_reviews_sentiment.csv"
# ---------------------------------------

def analyze_sentiment(text, analyzer):
    """Compute sentiment label and score using VADER"""
    if not isinstance(text, str) or text.strip() == "":
        return "neutral", 0.0
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return label, compound

def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    df = pd.read_csv(INPUT_FILE)
    analyzer = SentimentIntensityAnalyzer()
    
    # Apply sentiment analysis
    sentiments = df['review'].apply(lambda x: analyze_sentiment(x, analyzer))
    df['sentiment_label'] = sentiments.apply(lambda x: x[0])
    df['sentiment_score'] = sentiments.apply(lambda x: x[1])
    
    # Save to new CSV
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved sentiment-analyzed reviews → {OUTPUT_FILE}")
    print(df.head())

if __name__ == "__main__":
    main()
