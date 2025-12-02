import psycopg2
import pandas as pd

DB_NAME = "fintech_reviews"
DB_USER = "postgres"
DB_PASSWORD = r"""Ay2@nimran"""
DB_HOST = "localhost"
DB_PORT = 5432


INPUT_FILE = "data/processed/processed_reviews_sentiment.csv"

def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def create_tables(conn):
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS banks (
            bank_id SERIAL PRIMARY KEY,
            bank_name TEXT UNIQUE,
            app_name TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id TEXT PRIMARY KEY,
            bank_id INTEGER REFERENCES banks(bank_id),
            review_text TEXT,
            rating INTEGER,
            review_date DATE,
            sentiment_label TEXT,
            sentiment_score FLOAT,
            source TEXT
        );
    """)

    conn.commit()
    cur.close()

def load_banks(conn):
    cur = conn.cursor()
    banks = [("CBE", "Commercial Bank of Ethiopia App"),
             ("Abyssinia", "Bank of Abyssinia App"),
             ("Dashen", "Dashen SuperApp")]

    for b in banks:
        cur.execute("""
            INSERT INTO banks(bank_name, app_name)
            VALUES (%s, %s) ON CONFLICT (bank_name) DO NOTHING;
        """, b)

    conn.commit()
    cur.close()

def load_reviews(conn):
    df = pd.read_csv(INPUT_FILE)
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO reviews(
                review_id, bank_id, review_text, rating,
                review_date, sentiment_label, sentiment_score, source
            )
            VALUES (
                %s,
                (SELECT bank_id FROM banks WHERE bank_name=%s),
                %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (review_id) DO NOTHING;
        """, (
            row["review_id"],
            row["bank"],
            row["review"],
            row["rating"],
            row["date"],
            row["sentiment_label"],
            row["sentiment_score"],
            "google_play"
        ))

    conn.commit()
    cur.close()

def main():
    print("Connecting to PostgreSQL...")
    conn = connect_db()

    print("Creating tables...")
    create_tables(conn)

    print("Inserting banks...")
    load_banks(conn)

    print("Inserting reviews...")
    load_reviews(conn)

    conn.close()
    print("✅ DONE — Data Loaded Successfully!")

if __name__ == "__main__":
    main()
