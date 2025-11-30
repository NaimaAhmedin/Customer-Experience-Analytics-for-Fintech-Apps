import os
import pandas as pd
from tqdm import tqdm
from google_play_scraper import reviews, Sort
from datetime import datetime


# --------- CONFIG ---------
APPS = {
    "CBE": "com.combanketh.mobilebanking",      
    "Abyssinia": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

OUTPUT_DIR = "../data/raw"
REVIEWS_PER_APP = 400   # You can increase later
# --------------------------


def fetch_reviews(app_name, package_id, count=REVIEWS_PER_APP):
    print(f"\nScraping {app_name} ({package_id})...")

    all_reviews = []
    next_token = None

    pbar = tqdm(total=count, desc=f"Fetching {app_name}")

    while len(all_reviews) < count:
        batch, next_token = reviews(
            package_id,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=200,
            continuation_token=next_token
        )

        if not batch:
            break

        all_reviews.extend(batch)
        pbar.update(len(batch))

        if next_token is None:
            break

    pbar.close()
    return all_reviews[:count]


def save_reviews(app_name, data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.DataFrame(data)
    filename = f"{OUTPUT_DIR}/{app_name.lower()}_{datetime.now().date()}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} reviews → {filename}")


def main():
    for app_name, package_id in APPS.items():
        data = fetch_reviews(app_name, package_id)
        save_reviews(app_name, data)


if __name__ == "__main__":
    main()
