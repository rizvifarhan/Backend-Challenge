# Backend Challange

## 📌 Chosen Tracks & Rationale

### Section B - AI Brief Generator
**Why chosen**: 
- Implements cutting-edge LLM capabilities with practical marketing applications
- Demonstrates AI integration with caching and resilience patterns
- Solves real-world content creation challenges for marketers

### Section D - Batch ETL & Top-Performer API  
**Why chosen**:
- Handles large-scale data processing requirements
- Showcases performance optimization techniques
- Provides actionable business insights through calculated metrics

**Combined value**: These tracks complement each other by providing both strategic (AI briefs) and tactical (performance analytics) capabilities for influencer marketing campaigns.

## 🚀 Local Execution

### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- MongoDB (included in Docker setup)
- Redis (included in Docker setup)

### Quick Start
```bash
docker-compose up --build
```

This will launch:
1. MongoDB container for data storage
2. Redis container for caching
3. FastAPI services for both ETL and Brief Generation
4. Automatic ETL processing of sample data

### Alternative (Manual Setup)
```bash
# For ETL Service
python -m pip install -r etl_requirements.txt
python etl.py

# For Brief Generator
python -m pip install -r brief_requirements.txt
uvicorn brief_app:app --port 5001
```

## ⚖️ Architectural Decisions

### Trade-offs Made
1. **Chunk Size**: 1000 rows balances memory usage vs I/O overhead
2. **Caching TTL**: 5 minutes for briefs (sweet spot between freshness and performance)
3. **Error Handling**: Skip malformed chunks rather than individual rows
4. **LLM Choice**: Used OpenRouter for model flexibility despite potential latency

### Key Assumptions
1. CSV data follows consistent column structure
2. Views are always positive integers
3. Campaign IDs remain stable post-creation
4. Brief requests with identical parameters should return cached results

### Notable Decisions
1. **MongoDB Schema**: 
   - Flat structure for engagement data
   - No relationships for faster reads
2. **API Design**:
   - Simple GET with required params
   - Default limit of 10 performers
3. **ETL Resilience**:
   - Chunk-based processing
   - Skip-on-error pattern
4. **AI Integration**:
   - Modular prompt templates
   - Retry logic for LLM calls

## 🧪 Testing Procedures

### Unit Tests
```bash
# Run ETL tests
python -m unittest test_etl.py

# Run Brief Generator tests
python -m unittest test_brief.py
```

### API Test Cases

#### ETL Service
1. **Get top performers**:
```bash
curl "http://localhost:8000/top-performers?campaignId=campaign_6&limit=3"
```

2. **Invalid request**:
```bash
curl "http://localhost:8000/top-performers"
```

#### Brief Generator
1. **Generate standard brief**:
```bash
curl -X POST "http://localhost:5001/generate_brief" \
-H "Content-Type: application/json" \
-d '{"brand":"Nike","product":"Air Max","goal":"awareness","platform":"Instagram"}'
```

2. **Cached request**:
```bash
# Run same request twice - second should be faster
curl -X POST "http://localhost:5001/generate_brief" \
-H "Content-Type: application/json" \
-d '{"brand":"Adidas","product":"Ultraboost","goal":"sales","platform":"TikTok"}'
```

### Expected Responses
**ETL Success**:
```json
[
  {
    "campaignId": "campaign_6",
    "influencerId": "influencer_3",
    "engagementRate": 2.25
  },
  ...
]
```

**Brief Generator Success**:
```json
{
  "caption": "Step into style with the new Air Max...",
  "hook_ideas": [
    "Which celeb wore it best?",
    "Before/after comfort test",
    "Hidden design details reveal"
  ],
  "hashtags": ["#sneakerhead", "#justdoit", "#airmax"],
  "cta": "Tap link in bio to shop now!",
  "tone": "Energetic and aspirational"
}
```

## 📚 Additional Resources
- API DOCS

1) Section B

Access the following link:-

lINK = https://.postman.co/workspace/My-Workspace~b4d2860c-5f99-495d-8b52-2e762bc3f9f6/request/42655461-de3f1ba1-be8a-4aeb-82db-ddec8e55a558?action=share&creator=42655461&ctx=documentation&active-environment=42655461-99d25d92-5e55-4059-bce7-a22a8c738319


2) Section D

Access the following link:-

lINK = https://.postman.co/workspace/My-Workspace~b4d2860c-5f99-495d-8b52-2e762bc3f9f6/request/42655461-de3f1ba1-be8a-4aeb-82db-ddec8e55a558?action=share&creator=42655461&ctx=documentation&active-environment=42655461-99d25d92-5e55-4059-bce7-a22a8c738319

   
- Environment template files (`.env.example`) for configuration
- Docker logs provide detailed runtime information
# Femkeeda_challange
