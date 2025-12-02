import pandas as pd
import numpy as np
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
df = pd.read_csv("data/processed/processed_reviews_sentiment.csv")

# Clean missing reviews
df['review'] = df['review'].fillna('')

print("=== STEP 2: BASIC INSIGHTS GENERATION ===\n")

# Function to extract common words from reviews
def extract_keywords(text_series, top_n=10):
    """Extract most common meaningful words from reviews"""
    all_text = ' '.join(text_series.astype(str).tolist()).lower()
    
    # Remove special characters and split into words
    words = re.findall(r'\b[a-z]{3,}\b', all_text)
    
    # Common stopwords to remove
    stopwords = {
        'the', 'and', 'for', 'this', 'that', 'with', 'have', 'has', 'had',
        'was', 'were', 'are', 'but', 'not', 'you', 'your', 'they', 'their',
        'what', 'from', 'been', 'has', 'had', 'will', 'would', 'could',
        'should', 'about', 'when', 'where', 'which', 'there', 'here',
        'just', 'like', 'very', 'much', 'many', 'some', 'then', 'than',
        'also', 'only', 'even', 'well', 'good', 'bad', 'app', 'bank'
    }
    
    # Filter out stopwords
    filtered_words = [word for word in words if word not in stopwords]
    
    # Count word frequency
    word_counts = Counter(filtered_words)
    
    return word_counts.most_common(top_n)

# Function to analyze sentiment by rating
def analyze_sentiment_by_rating(bank_df):
    """Analyze how sentiment varies with rating"""
    results = {}
    for rating in [1, 2, 3, 4, 5]:
        rating_df = bank_df[bank_df['rating'] == rating]
        if len(rating_df) > 0:
            avg_sentiment = rating_df['sentiment_score'].mean()
            results[rating] = avg_sentiment
    return results

# Analyze each bank
banks = df['bank'].unique()
bank_insights = {}

for bank in banks:
    print(f"\n{'='*50}")
    print(f"ANALYSIS FOR {bank.upper()} BANK")
    print(f"{'='*50}")
    
    bank_df = df[df['bank'] == bank]
    
    # 1. Basic metrics
    total_reviews = len(bank_df)
    avg_rating = bank_df['rating'].mean()
    avg_sentiment = bank_df['sentiment_score'].mean()
    positive_pct = (bank_df['sentiment_label'] == 'positive').sum() / total_reviews * 100
    negative_pct = (bank_df['sentiment_label'] == 'negative').sum() / total_reviews * 100
    
    print(f"\nBasic Metrics:")
    print(f"- Total Reviews: {total_reviews}")
    print(f"- Average Rating: {avg_rating:.2f}/5")
    print(f"- Average Sentiment: {avg_sentiment:.3f}")
    print(f"- Positive Reviews: {positive_pct:.1f}%")
    print(f"- Negative Reviews: {negative_pct:.1f}%")
    
    # 2. Rating distribution
    rating_dist = bank_df['rating'].value_counts().sort_index()
    print(f"\nRating Distribution:")
    for rating in range(1, 6):
        count = rating_dist.get(rating, 0)
        pct = (count / total_reviews) * 100
        print(f"  {rating} stars: {count} reviews ({pct:.1f}%)")
    
    # 3. Analyze positive reviews (DRIVERS)
    positive_reviews = bank_df[bank_df['sentiment_label'] == 'positive']
    if len(positive_reviews) > 0:
        positive_keywords = extract_keywords(positive_reviews['review'], top_n=8)
        print(f"\nTop Keywords in POSITIVE Reviews:")
        for word, count in positive_keywords:
            print(f"  - {word}: {count} times")
    
    # 4. Analyze negative reviews (PAIN POINTS)
    negative_reviews = bank_df[bank_df['sentiment_label'] == 'negative']
    if len(negative_reviews) > 0:
        negative_keywords = extract_keywords(negative_reviews['review'], top_n=8)
        print(f"\nTop Keywords in NEGATIVE Reviews:")
        for word, count in negative_keywords:
            print(f"  - {word}: {count} times")
    
    # 5. Analyze low ratings specifically (1-2 stars)
    low_ratings = bank_df[bank_df['rating'] <= 2]
    if len(low_ratings) > 0:
        low_rating_keywords = extract_keywords(low_ratings['review'], top_n=6)
        print(f"\nTop Keywords in LOW RATINGS (1-2 stars):")
        for word, count in low_rating_keywords:
            print(f"  - {word}: {count} times")
    
    # 6. Analyze high ratings specifically (4-5 stars)
    high_ratings = bank_df[bank_df['rating'] >= 4]
    if len(high_ratings) > 0:
        high_rating_keywords = extract_keywords(high_ratings['review'], top_n=6)
        print(f"\nTop Keywords in HIGH RATINGS (4-5 stars):")
        for word, count in high_rating_keywords:
            print(f"  - {word}: {count} times")
    
    # 7. Sentiment by rating analysis
    sentiment_by_rating = analyze_sentiment_by_rating(bank_df)
    print(f"\nAverage Sentiment by Rating:")
    for rating, sentiment in sentiment_by_rating.items():
        print(f"  {rating} stars: {sentiment:.3f}")
    
    # Store insights for later use
    bank_insights[bank] = {
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
        'avg_sentiment': avg_sentiment,
        'positive_pct': positive_pct,
        'negative_pct': negative_pct,
        'positive_keywords': positive_keywords if 'positive_keywords' in locals() else [],
        'negative_keywords': negative_keywords if 'negative_keywords' in locals() else []
    }

print(f"\n{'='*60}")
print("COMPARATIVE ANALYSIS ACROSS BANKS")
print(f"{'='*60}")

# Create comparison table
comparison_df = pd.DataFrame({
    'Bank': banks,
    'Avg Rating': [bank_insights[bank]['avg_rating'] for bank in banks],
    'Avg Sentiment': [bank_insights[bank]['avg_sentiment'] for bank in banks],
    'Positive %': [bank_insights[bank]['positive_pct'] for bank in banks],
    'Negative %': [bank_insights[bank]['negative_pct'] for bank in banks]
})

print("\nPerformance Comparison:")
print(comparison_df.round(2))

# Find best and worst performing
best_rating = comparison_df.loc[comparison_df['Avg Rating'].idxmax()]
worst_rating = comparison_df.loc[comparison_df['Avg Rating'].idxmin()]

print(f"\nBest Rated Bank: {best_rating['Bank']} ({best_rating['Avg Rating']:.2f})")
print(f"Worst Rated Bank: {worst_rating['Bank']} ({worst_rating['Avg Rating']:.2f})")

# Save insights to file
print(f"\n✅ Analysis complete! Next step: Creating visualizations for these insights.")
print(f"📊 You now have basic insights about drivers and pain points for each bank.")