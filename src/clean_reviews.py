import os
import pandas as pd
import re
from datetime import datetime

# ---------------- CONFIG ----------------
RAW_DIR = "../data/raw"
PROCESSED_DIR = "../data/processed"
# ---------------------------------------

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+", "", text)          # remove urls
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # remove special chars
    text = re.sub(r"\s+", " ", text).strip()    # remove extra spaces
    return text

def process_file(file_path):
    df = pd.read_csv(file_path)
    
    # Keep relevant columns
    cols = ['reviewId', 'userName', 'content', 'score', 'at']
    df = df[cols]
    
    # Rename columns
    df.columns = ['review_id', 'user', 'review', 'rating', 'date']
    
    # Add bank column based on filename
    fname = os.path.basename(file_path).lower()
    if "cbe" in fname:
        df['bank'] = "CBE"
    elif "boa" in fname:
        df['bank'] = "Abyssinia"
    else:
        df['bank'] = "Dashen"
    # Clean text
    df['review'] = df['review'].apply(clean_text)
    
    # Normalize date
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    # Remove duplicates & missing reviews
    df.drop_duplicates(subset='review_id', inplace=True)
    df.dropna(subset=['review'], inplace=True)
    
    return df

def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    all_files = [f"{RAW_DIR}/{f}" for f in os.listdir(RAW_DIR) if f.endswith(".csv")]
    cleaned_dfs = []
    
    for file in all_files:
        df = process_file(file)
        cleaned_dfs.append(df)
    
    final_df = pd.concat(cleaned_dfs, ignore_index=True)
    
    # Save cleaned CSV
    output_file = f"{PROCESSED_DIR}/cleaned_reviews.csv"
    final_df.to_csv(output_file, index=False)
    print(f"Saved cleaned reviews → {output_file}")
    print(final_df.head())

if __name__ == "__main__":
    main()
