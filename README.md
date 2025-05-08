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
python3 -m uvicorn app.main:app --reload
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
python3 -m pytest tests/test_etl.py

# Run Brief Generator tests
python3 -m pytest tests/test_app.py
```

### API Test Cases

#### ETL Service
1. **Get top performers**:
```bash
curl "http://localhost:8000/top-performers?campaignId=campaign_1&limit=5"
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
-d '{"brand":"Nike","product":"Air Max Running Shoes","goal":"Increase engagement among young athletes","platform":"Instagram","persona": "Millennial, Fitness Enthusiast","creative_angle": "Highlight the shoe\'s innovative cushioning technology","hashtags": ["#LuxuryWatch", "#TimelessElegance", "#Craftsmanship"]}'
```

2. **Cached request**:
```bash
# Run same request twice - second should be faster
curl -X POST "http://localhost:5001/generate_brief" \
-H "Content-Type: application/json" \
-d '{"brand":"Adidas","product":"Ultraboost","goal":"sales","platform":"TikTok", "persona": "Millennial, Fitness Enthusiast","creative_angle": "Highlight the shoe\'s innovative cushioning technology","hashtags": ["#LuxuryWatch", "#TimelessElegance", "#Craftsmanship"]}'
```

### Expected Responses
**ETL Success**:
```json
[
  {
    "_id": "681b7850cc95e0aa6d46701b",
    "campaignId": "campaign_1",
    "influencerId": "influencer_3764",
    "engagementRate": 9.984033367004464
  },
  {
    "_id": "681b7850cc95e0aa6d4674a6",
    "campaignId": "campaign_1",
    "influencerId": "influencer_4927",
    "engagementRate": 9.972533570081012
  },
 .... more 3
]
```

**Brief Generator Success**:
```json
{
    "caption": "Step into the future of running with Nike Air Max. Experience unparalleled comfort and performance with our innovative cushioning technology. Perfect for the millennial fitness enthusiast who demands the best. Lace up and feel the difference!",
    "hook_ideas": [
        "Feel the cushioning revolution under your feet.",
        "Transform your running game with every step.",
        "Elevate your fitness journey with the ultimate in comfort."
    ],
    "hashtags": [
        "#NikeAirMax",
        "#InnovativeCushioning",
        "#YoungAthletes"
    ],
    "cta": "Tap to learn more about the game-changing Air Max technology!",
    "tone": "Exciting and motivational, inspiring young athletes to push their limits."
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

   
# Femkeeda_challange
