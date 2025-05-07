# Backend-Challenge

# Section D: Influencer Engagement Analytics Project

```markdown
# Influencer Engagement Analytics System

## 1) Chosen Tracks
I selected these two tracks from the assignment:
- **Batch ETL Processing**: For efficiently handling large datasets (10k rows) with malformed data
- **Top-Performer API**: To surface the highest-engagement creators in a scalable way

**Why these tracks?**
The combination allows for:
1. Robust data processing that can handle real-world messy data
2. A performant way to query results by campaign
3. Meeting the strict runtime budget (< 2 minutes for 10k rows)
4. Creating a foundation that could scale to much larger datasets

## 2) Running the Project Locally

### Prerequisites
- Docker and Docker Compose installed
- Python 3.8+ (if running without Docker)

### Using Docker (Recommended)
```bash
docker-compose up --build
```
This will:
1. Start MongoDB container
2. Start the FastAPI application
3. Automatically run the ETL process

### Without Docker
```bash
# Install dependencies
pip install -r requirements.txt

# Start MongoDB (ensure it's running locally on port 27017)

# Run ETL process
python etl.py

# Start API server
uvicorn app:app --reload
```

## 3) Trade-offs, Assumptions & Decisions

### Trade-offs Made
1. **Chunk Processing**: Used pandas' chunking to handle memory constraints, trading some speed for memory safety
2. **Simple Engagement Formula**: Used basic (likes+comments+shares)/views for clarity, though real-world might weight different interactions
3. **MongoDB Storage**: Chose MongoDB for flexible schema to handle potential future fields

### Key Assumptions
1. CSV format will always include the required columns (though handles missing values)
2. Views will never be negative (filtered zero views)
3. API consumers need sorted results by default
4. Malformed rows can be skipped without failing the entire process

### Important Decisions
1. **Chunk Size**: Set to 1000 rows as balance between memory and I/O overhead
2. **Data Clearing**: ETL script clears existing data by default (can be commented out)
3. **Error Handling**: Skips entire chunks on errors (could be made more granular)
4. **API Design**: Simple GET endpoint with required `campaignId` parameter

## 4) Testing Instructions

### Unit Tests
```bash
python -m unittest test_etl.py
```
Tests:
1. Engagement rate calculation correctness
2. Sorting logic for top performers

### Manual API Testing
After starting the service:

1. **Get top performers for `campaign_6`**:
```bash
curl "http://localhost:8000/top-performers?campaignId=campaign_6&limit=3"
```

2. **Get top performer for `campaign_10`**:
```bash
curl "http://localhost:8000/top-performers?campaignId=campaign_10&limit=1"
```

3. **Invalid request (missing `campaignId`)**:
```bash
curl "http://localhost:8000/top-performers"
```

### Sample Expected Output
For `campaign_6` (top 3):
```json
[
  {
    "campaignId": "campaign_6",
    "influencerId": "influencer_3",
    "engagementRate": 2.25,
    "_id": "123abc..."
  },
  {
    "campaignId": "campaign_6",
    "influencerId": "influencer_9",
    "engagementRate": 7.14,
    "_id": "456def..."
  },
  {
    "campaignId": "campaign_6",
    "influencerId": "influencer_1",
    "engagementRate": 1.64,
    "_id": "789ghi..."
  }
]
```


```

# Section B: AI-Powered Influencer Brief Generator
```

```markdown
# AI-Powered Influencer Brief Generator

## 📌 Chosen Track: AI Brief Generator
**Why this track?**  
- Combines LLM capabilities with structured marketing workflows  
- Demonstrates practical AI integration (caching, retries, tool-chaining)  
- Solves a real business need for scalable content creation  

---

## 🚀 Quick Start

### Prerequisites
- Docker + Docker Compose  
- OpenAI/OpenRouter API key in `.env`

### Docker Setup (Recommended)
```bash
docker-compose up --build
```
API will be live at: `http://localhost:5001`

---

## 🔧 Manual Installation
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🛠️ Technical Decisions

| Area               | Implementation                 | Rationale                          |
|--------------------|--------------------------------|------------------------------------|
| LLM Orchestration  | OpenRouter + JSON mode         | Cost-effective, reliable JSON output |
| Tools System       | Simple Python functions        | Mockable for testing               |
| Caching            | Redis (request-hash keyed)     | 100ms cache hits for repeat requests |
| Resilience         | Exponential backoff retries    | Handles LLM timeouts gracefully    |

---

## 🧪 Testing

### Unit Tests
```bash
pytest tests/
```
Validates:
- Tool functions (`trendFetcher`, `personaClassifier`)  
- Creative angle generation  
- *(Expand with API tests)*  

### API Example
```bash
curl -X POST "http://localhost:5001/generate_brief" \
-H "Content-Type: application/json" \
-d '{
    "brand": "Nike",
    "product": "Air Max",
    "goal": "engagement",
    "platform": "Instagram"
}'
```

Sample Response:
```json
{
  "caption": "Step into the future with #AirMax...",
  "hook_ideas": [
    "Close-up of sneaker details",
    "Before/after workout transition",
    "Celebrity endorsement mockup"
  ],
  "hashtags": ["#Trending1", "#Sneakerhead", "#JustDoIt"],
  "cta": "Tag us in your photos!",
  "tone": "Energetic and aspirational"
}
```

---

## 🔄 Workflow Diagram
```
Client → [FastAPI] → Check Cache → Call Tools → LLM → Cache → Response
                ↑____________Retry_3x_________↑
```

---

## 📜 Key Components

✅ **Core Tools**  
- `trendFetcher()`: Generates platform-relevant hashtags  
- `personaClassifier()`: Matches brand to target audience  
- `creativeAngle()`: Product-specific content direction  

✅ **Prompt Engineering**  
- Structured template in `prompts.py`  
- Enforced JSON output via LLM directives  

✅ **Production Ready**  
- Redis caching (300s TTL)  
- Exponential backoff retries  
- Detailed logging  

---

## 🌟 Sample Use Case
1. Marketing team submits brand/product details  
2. System auto-generates:  
   - Audience persona  
   - Hashtag recommendations  
   - Creative direction  
3. Returns polished brief in <1s (cached)  

```python
# Example Python client
import requests
response = requests.post("http://localhost:5001/generate_brief", json={
    "brand": "Sephora",
    "product": "Vitamin C Serum",
    "goal": "sales",
    "platform": "TikTok"
})
```
