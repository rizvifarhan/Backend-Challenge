import pandas as pd
from pymongo import MongoClient
from config import MONGO_URI
client = MongoClient(MONGO_URI)

print("🚀 ETL script started...")

def process_data(file_path):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['campaign_db']
    collection = db['engagement_data']
    collection.delete_many({})  # Optional: Clear existing data

    chunksize = 1000
    total_inserted = 0
    total_skipped = 0

    for chunk in pd.read_csv(file_path, chunksize=chunksize):
        try:
            required_cols = ['likes', 'comments', 'shares', 'views', 'campaignId', 'influencerId']
            chunk = chunk.dropna(subset=required_cols)
            chunk = chunk[chunk['views'] != 0]
            chunk['engagementRate'] = (chunk['likes'] + chunk['comments'] + chunk['shares']) / chunk['views'] * 100
            data = chunk[['campaignId', 'influencerId', 'engagementRate']].to_dict(orient='records')
            collection.insert_many(data)
            total_inserted += len(data)

        except Exception as e:
            print(f"Chunk skipped due to error: {e}")
            total_skipped += len(chunk)
            continue

    print(f"✅ Total rows inserted: {total_inserted}")
    print(f"⚠️ Total malformed/skipped rows: {total_skipped}")
    client.close()

if __name__ == "__main__":
    process_data("influencers_data_realistic_malformed.csv")
