import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import redis
from openai import OpenAI
import hashlib
import json
from dotenv import load_dotenv
import logging
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential
from app.prompts import BRIEF_TEMPLATE  # Import from separate file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI()

# Redis connection
try:
    cache = redis.StrictRedis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=6379, 
        db=0, 
        decode_responses=True,
        socket_timeout=5
    )
    cache.ping()
    logger.info("Redis connection successful")
except redis.ConnectionError:
    logger.warning("Redis connection failed, proceeding without cache")
    cache = None

# OpenRouter setup
try:
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
    )
    logger.info("OpenRouter connection initialized")
except Exception as e:
    logger.error(f"Failed to initialize OpenRouter client: {str(e)}")
    raise

# Pydantic models
class BriefRequest(BaseModel):
    brand: str
    product: str
    goal: str
    platform: str
    persona: Optional[str] = None
    creative_angle: Optional[str] = None
    hashtags: Optional[List[str]] = None

class BriefResponse(BaseModel):
    caption: str
    hook_ideas: List[str]
    hashtags: List[str]
    cta: str
    tone: str

# Helper functions
def hash_request(data: Dict[str, Any]) -> str:
    return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

def trendFetcher(platform: str) -> List[str]:
    return ["#Trending1", "#Trending2", "#Trending3"]

def personaClassifier(brand: str, goal: str) -> str:
    return "Millennial, Fashion Enthusiast"

def creativeAngle(product: str) -> str:
    return "Highlight the uniqueness and luxury of the product."

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_brief(data: Dict[str, Any]) -> Dict[str, Any]:
    prompt = BRIEF_TEMPLATE.format(
        brand=data["brand"],
        product=data["product"],
        goal=data["goal"],
        platform=data["platform"],
        persona=data.get("persona", personaClassifier(data["brand"], data["goal"])),
        creative_angle=data.get("creative_angle", creativeAngle(data["product"])),
        hashtags=", ".join(data.get("hashtags", trendFetcher(data["platform"])))
    )
    
    response = client.chat.completions.create(
        model="qwen/qwen2.5-vl-72b-instruct:free",
        messages=[
            {"role": "system", "content": "You are a creative marketing assistant. Return valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500,
        response_format={"type": "json_object"}
    )
    
    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        logger.error("Failed to parse LLM response as JSON")
        raise ValueError("Invalid JSON response from LLM")

@app.post("/generate_brief", response_model=BriefResponse)
async def generate_influencer_brief(request: BriefRequest):
    try:
        logger.info(f"Received request for {request.brand}")
        data = request.dict()
        cache_key = hash_request(data)
        
        if cache and (cached := cache.get(cache_key)):
            logger.info("Returning cached result")
            return JSONResponse(content=json.loads(cached))

        extended_data = {
            **data,
            "hashtags": data.get("hashtags", trendFetcher(data["platform"])),
            "persona": data.get("persona", personaClassifier(data["brand"], data["goal"])),
            "creative_angle": data.get("creative_angle", creativeAngle(data["product"]))
        }

        brief = generate_brief(extended_data)
        
        if cache:
            cache.set(cache_key, json.dumps(brief), ex=300)

        return brief

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/")
    def read_root():
        return {"message": "AI Brief Generator is running!"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)


#To run:  python3 -m uvicorn app.main:app --reload