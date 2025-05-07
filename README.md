# Backend-Challenge

# Section D: Influencer Engagement Analytics Project

```markdown
# Influencer Engagement Analytics Project

## 📌 Chosen Tracks
1. **Batch ETL Pipeline**  
   - Processes 10k+ rows of influencer data with malformed entries  
   - Calculates engagement rates (`(likes + comments + shares) / views * 100`)  
   - Optimized for performance (<2 min runtime)  

2. **Top-Performer API**  
   - REST endpoint to query influencers by campaign  
   - Returns results sorted by engagement rate (descending)  
   - Supports pagination via `limit` parameter  

---

## 🚀 Quick Start

### Prerequisites
- Docker + Docker Compose  
- (Optional) Python 3.8+ for native execution  

### Docker Setup (Recommended)
```bash
git clone [your-repo-url]
cd [repo-directory]
docker-compose up --build
```
API will be live at: `http://localhost:8000`

---

## 🔧 Manual Installation
```bash
pip install -r requirements.txt
python etl.py  # Run ETL pipeline
uvicorn app:app --reload  # Start API
```

---

## 🛠️ Technical Decisions

| Area               | Choice                          | Rationale                          |
|--------------------|---------------------------------|------------------------------------|
| Data Processing    | Pandas chunked CSV reads        | Memory efficiency for large files  |
| Error Handling     | Skip malformed rows             | Meet runtime budget (<2 min)       |
| Storage            | MongoDB                         | Flexible schema for engagement data|
| API Design         | Single endpoint with filters    | Simplicity + clear use case        |

---

## 🧪 Testing

### Unit Tests
```bash
python -m unittest test_etl.py
```
Validates:
- Engagement rate calculations
- Sorting logic correctness

### API Examples
```bash
# Top 3 performers for campaign_6
curl "http://localhost:8000/top-performers?campaignId=campaign_6&limit=3"

# Default (10) results for campaign_10
curl "http://localhost:8000/top-performers?campaignId=campaign_10"
```

Sample Response:
```json
[
  {
    "campaignId": "campaign_6",
    "influencerId": "influencer_3",
    "engagementRate": 2.25,
    "_id": "665a..."
  }
]
```

---

## 🎯 Key Features
✅ **ETL Pipeline**  
- Processes data in 1000-row chunks  
- Auto-skips rows with missing/zero-view data  
- Logs processed/skipped counts  

✅ **API Endpoint**  
- Fast lookup by `campaignId`  
- Configurable result limit  
- Descending engagement sort  

---

## 📜 Sample Data Structure
```csv
influencerId,campaignId,views,likes,comments,shares
influencer_1,campaign_6,16795,213,48,14
influencer_2,campaign_6,1860,31,6,6
...
``` 
*(See full sample in repository)*


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
