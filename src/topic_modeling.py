import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import spacy
import json
import sys
import glob

# CONFIG
INPUT = "data/processed/processed_reviews_sentiment.csv" 
OUT_DIR = "../data/processed/topics"
N_TOPICS = 5         # change to 3-5 per bank as needed
TOP_N_WORDS = 12

nlp = spacy.load("en_core_web_sm", disable=["parser","ner"])

def preprocess_texts(texts):
    docs = []
    for doc in nlp.pipe(texts, batch_size=50):
        toks = [t.lemma_.lower() for t in doc if (t.is_alpha and not t.is_stop and len(t)>2)]
        docs.append(" ".join(toks))
    return docs

def topic_model_for_bank(df_bank, bank_name, n_topics=N_TOPICS):
    texts = df_bank["review"].astype(str).tolist()
    pre = preprocess_texts(texts)
    # Use CountVectorizer for LDA
    cv = CountVectorizer(max_df=0.95, min_df=5, max_features=5000, ngram_range=(1,2))
    X = cv.fit_transform(pre)
    if X.shape[0] == 0 or X.shape[1] == 0:
        return None
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42, learning_method="batch", max_iter=15)
    lda.fit(X)
    features = cv.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_indices = topic.argsort()[-TOP_N_WORDS:][::-1]
        top_terms = [features[i] for i in top_indices]
        topics.append({"topic_id": topic_idx, "terms": top_terms})
    # Assign dominant topic to each doc
    doc_topics = lda.transform(X).argmax(axis=1)
    df_bank = df_bank.reset_index(drop=True)
    df_bank["topic_id"] = doc_topics
    return topics, df_bank

def save_topics(bank_name, topics):
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, f"{bank_name}_topics.json"), "w", encoding="utf-8") as f:
        json.dump(topics, f, indent=2)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    # Helpful check: ensure the input CSV exists and has the expected columns
    if not os.path.exists(INPUT):
        # try to find similarly named files in data/processed
        alt = glob.glob(os.path.join(os.path.dirname(INPUT), "*sentiment*.csv"))
        msg_lines = [f"Required input file not found: {INPUT}"]
        if alt:
            msg_lines.append("Found similar processed files:")
            for p in alt:
                msg_lines.append(f"  - {p}")
            msg_lines.append("If one of these is the correct file, set INPUT in this script or pass the path via environment variable TOPIC_INPUT.")
        else:
            msg_lines.append("No candidate processed files found in data/processed.")
        msg_lines.append("")
        msg_lines.append("This script expects a processed CSV with at least these columns: review_id, review, bank, sentiment_label")
        msg_lines.append("Run the preprocessing and sentiment scripts first to generate: ../data/processed/processed_reviews_sentiment.csv")
        msg_lines.append("")
        msg_lines.append("Example (PowerShell):")
        msg_lines.append("  pip install -r requirements.txt")
        msg_lines.append("  python src/scrape_reviews.py")
        msg_lines.append("  # run your preprocessing/sentiment scripts to produce processed_reviews_sentiment.csv")
        print("\n".join(msg_lines))
        sys.exit(2)

    df = pd.read_csv(INPUT)
    banks = df["bank"].unique()
    all_examples = []
    for bank in banks:
        print(f"Running topics for {bank} ...")
        df_bank = df[df["bank"] == bank].copy()
        if df_bank.empty:
            print(" no data for", bank); continue
        result = topic_model_for_bank(df_bank, bank, n_topics=N_TOPICS)
        if result is None:
            print("Not enough data for LDA on", bank)
            continue
        topics, df_with_topics = result
        save_topics(bank, topics)
        # Save labeled reviews
        df_with_topics.to_csv(os.path.join(OUT_DIR, f"{bank}_reviews_with_topics.csv"), index=False)
        # Collect a few examples per topic for manual labeling
        for t in range(N_TOPICS):
            ex = df_with_topics[df_with_topics["topic_id"]==t].head(5)[["review_id","review","sentiment_label"]].to_dict(orient="records")
            all_examples.append({"bank":bank,"topic_id":t,"examples":ex})
    # Save examples for manual grouping
    pd.DataFrame(all_examples).to_json(os.path.join(OUT_DIR, "topic_examples.json"), orient="records", indent=2)
    print("Topic modeling finished. Results in", OUT_DIR)

if __name__ == "__main__":
    main()
