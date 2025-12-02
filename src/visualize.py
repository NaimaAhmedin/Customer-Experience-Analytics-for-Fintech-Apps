import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import os

# Load processed data
df = pd.read_csv("data/processed/processed_reviews_sentiment.csv")

# Ensure output directory exists
os.makedirs("reports/figures", exist_ok=True)

# -----------------------
# 1. Sentiment Distribution per Bank
# -----------------------
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="bank", hue="sentiment_label")
plt.title("Sentiment Distribution per Bank")
plt.xlabel("Bank")
plt.ylabel("Count")
plt.legend(title="Sentiment")
plt.tight_layout()
plt.savefig("../reports/figures/sentiment_distribution_per_bank.png")
plt.close()

# -----------------------
# 2. Average Sentiment Score per Bank
# -----------------------
plt.figure(figsize=(8, 5))
df.groupby("bank")["sentiment_score"].mean().plot(kind="bar")
plt.title("Average Sentiment Score per Bank")
plt.ylabel("Average Score")
plt.tight_layout()
plt.savefig("../reports/figures/avg_sentiment_score_per_bank.png")
plt.close()

# -----------------------
# 3. WordCloud for Each Bank
# -----------------------
banks = df["bank"].unique()

for bank in banks:
    # FIX: Use 'review' instead of 'cleaned_review'
    text = " ".join(df[df["bank"] == bank]["review"].astype(str))

    if len(text.strip()) < 5:
        continue

    wc = WordCloud(width=800, height=400, background_color="white").generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"WordCloud for {bank} Bank")
    plt.savefig(f"../reports/figures/wordcloud_{bank}.png")
    plt.close()

print("🎉 Visualization completed! Check the reports/figures folder.")
