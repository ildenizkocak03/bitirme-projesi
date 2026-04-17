from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.analyzer import SentimentAnalyzer
from src.topic_engine import TopicEngine
from src.risk_engine import RiskEngine

app = FastAPI(title="Customer Review AI API", version="1.0.0")

# Initialize analyzers
sentiment_analyzer = SentimentAnalyzer()
topic_engine = TopicEngine()
risk_engine = RiskEngine()

class ReviewRequest(BaseModel):
    text: str

class BatchReviewRequest(BaseModel):
    reviews: List[str]

class AnalysisResponse(BaseModel):
    sentiment: str
    sentiment_score: float
    topic: str
    topic_confidence: float
    risk_level: str
    risk_score: float
    explanation: str

class BatchAnalysisResponse(BaseModel):
    results: List[AnalysisResponse]

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Customer Review AI API is running"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_review(request: ReviewRequest):
    try:
        sentiment = sentiment_analyzer.analyze(request.text)
        topic = topic_engine.classify_topic(request.text)
        risk = risk_engine.assess_risk(request.text, sentiment)
        
        return AnalysisResponse(
            sentiment=sentiment['label'],
            sentiment_score=sentiment['score'],
            topic=topic['topic'],
            topic_confidence=topic['confidence'],
            risk_level=risk['level'],
            risk_score=risk['score'],
            explanation=risk['explanation']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze-batch", response_model=BatchAnalysisResponse)
async def analyze_batch_reviews(request: BatchReviewRequest):
    try:
        results = []
        for text in request.reviews:
            sentiment = sentiment_analyzer.analyze(text)
            topic = topic_engine.classify_topic(text)
            risk = risk_engine.assess_risk(text, sentiment)
            
            result = AnalysisResponse(
                sentiment=sentiment['label'],
                sentiment_score=sentiment['score'],
                topic=topic['topic'],
                topic_confidence=topic['confidence'],
                risk_level=risk['level'],
                risk_score=risk['score'],
                explanation=risk['explanation']
            )
            results.append(result)
        
        return BatchAnalysisResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")