from fastapi import FastAPI,HTTPException,BackgroundTasks

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from typing import List,Dict

import asyncio

from models.trend_models import UserPreferences,TrendAnalysis
from services.trend_analyzer import TrendAnalyzer

app = FastAPI(
    title="Cultrend Ai - by Qloo and Gemini",
    description="Cultural Intelligence Trend Prediction Platform using Google Gemini LLM",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

trend_analyzer = TrendAnalyzer()

class TrendRequest(BaseModel):
    preferences: UserPreferences
    timeframe: str = "90d"

class HealthCheck(BaseModel):
    status: str
    message: str

@app.get("/",response_model=HealthCheck)
async def root():
    return HealthCheck(
        status="healthy",
        message="Cultrend API with Gemini LLM is running successfully! "
    )


@app.post("/predict-trends", response_model=TrendAnalysis)
async def predict_trends(request: TrendRequest):
    try:
        print("Received predict-trends request:")
        print(request)

        valid_timeframes = ["30d", "90d", "180d"]
        if request.timeframe not in valid_timeframes:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid timeframe. Must be one of: {valid_timeframes}"
            )

        analysis = await trend_analyzer.predict_trends(
            request.preferences,
            request.timeframe
        )
        print("Prediction result:", analysis)
        return analysis

    except Exception as e:
        print("❌ Error during prediction:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Trend analysis failed: {str(e)}"
        )
@app.get("sample-preferences",response_model=List[UserPreferences])
async def get_sample_preferences():
    samples = [
        UserPreferences(
            music_genres=["indie rock", "folk", "electronic"],
            dining_preferences=["artisanal coffee", "plant-based", "local sourcing"],
            fashion_styles=["minimalist", "sustainable", "vintage"],
            entertainment_types=["indie films", "live music", "podcasts"],
            lifestyle_choices=["sustainable living", "wellness", "remote work"]
        ),
        UserPreferences(
            music_genres=["hip-hop", "jazz", "R&B"],
            dining_preferences=["street food", "fusion cuisine", "craft cocktails"],
            fashion_styles=["streetwear", "luxury brands", "sneakers"],
            entertainment_types=["sports", "gaming", "social media"],
            lifestyle_choices=["fitness", "urban living", "nightlife"]
        ),
        UserPreferences(
            music_genres=["classical", "ambient", "new age"],
            dining_preferences=["fine dining", "wine pairing", "molecular gastronomy"],
            fashion_styles=["luxury", "classic", "designer"],
            entertainment_types=["opera", "art galleries", "theater"],
            lifestyle_choices=["luxury travel", "collecting", "cultural events"]
        )
    ]
    
    return samples

@app.get("/health")
async def health_check():
    from services.gemini_service import GeminiService
    gemini_service = GeminiService()
        
    test_response = gemini_service.model.generate_content("Hello, this is a connection test.")
    gemini_status = "healthy" if test_response else "error"

    return {
            "status": "healthy",
            "services": {
                "qloo_api": "healthy",
                "gemini_llm": gemini_status,
                "trend_analyzer": "healthy"
            },
            "version": "1.0.0",
            "powered_by": "Google Gemini LLM"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )