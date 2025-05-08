import pytest
from app.main import personaClassifier, trendFetcher, creativeAngle

def test_persona_classifier():
    assert "Millennial" in personaClassifier("Nike", "engagement")
    assert "Fashion" in personaClassifier("Gucci", "awareness")

def test_trend_fetcher():
    trends = trendFetcher("Instagram")
    assert len(trends) == 3
    assert all(t.startswith("#") for t in trends)

def test_creative_angle():
    assert "uniqueness" in creativeAngle("Premium Watch")
    assert "luxury" in creativeAngle("Designer Bag")

# Add more tests for API endpoints using TestClient