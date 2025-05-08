# app_fastapi.py
from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)



from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from bson import ObjectId
from typing import Any

# Initialize FastAPI app
app = FastAPI()

client = MongoClient('mongodb://localhost:27017/')
db = client['campaign_db']
collection = db['engagement_data']

# Helper function to convert ObjectId to string
def mongo_to_dict(obj: Any):
    """Recursively converts ObjectId to string in a dictionary"""
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: mongo_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [mongo_to_dict(i) for i in obj]
    else:
        return obj

@app.get("/top-performers")
def top_performers(campaignId: str = Query(...), limit: int = Query(10)):
    if not campaignId:
        raise HTTPException(status_code=400, detail="campaignId is required")

    # Fetch data from MongoDB
    data = collection.find({"campaignId": campaignId})

    # Convert MongoDB data to JSON-serializable format
    data = [mongo_to_dict(item) for item in data]

    # Sort by engagementRate in descending order
    sorted_data = sorted(data, key=lambda x: x['engagementRate'], reverse=True)

    # Limit the results
    top_performers = sorted_data[:limit]

    return JSONResponse(content=top_performers)
