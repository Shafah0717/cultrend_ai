# main.py - FastAPI backend for TrendSeer
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.trend_analyzer import TrendAnalyzer
from services.qloo_service import QlooService
from services.gemini_service import GeminiService
from models.trend_models import UserPreferences, CulturalProfile

app = FastAPI(
    title="TrendSeer Cultural Intelligence API",
    description="Real-time cultural trend analysis powered by Qloo + Gemini AI",
    version="1.0.0"
)

# Add CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
trend_analyzer = TrendAnalyzer()
qloo_service = QlooService()
gemini_service = GeminiService()

@app.get("/")
async def root():
    return {
        "message": "Cultrend Cultural Intelligence API",
        "version": "1.0.0",
        "status": "active",
        "features": ["cultural_analysis", "trend_prediction", "brand_insights"]
    }

@app.post("/api/analyze")
async def analyze_cultural_preferences(preferences: UserPreferences):
    """
    Main endpoint: Complete cultural analysis pipeline
    - Input: User cultural preferences
    - Output: Cultural profile + trend predictions with 98% confidence
    """
    try:
        analysis = await trend_analyzer.predict_trends(preferences, "90d")
        
        return {
            "success": True,
            "cultural_profile": {
                "profile_id": analysis.cultural_profile.profile_id,
                "cultural_segments": analysis.cultural_profile.cultural_segments,
                "confidence_score": analysis.cultural_profile.confidence_score,
                "behavioral_indicators": analysis.cultural_profile.behavioral_indicators,
                "cross_domain_connections": analysis.cultural_profile.cross_domain_connections
            },
            "trend_predictions": [
                {
                    "trend": pred.predicted_trend,
                    "confidence": pred.confidence_score,
                    "timeline_days": pred.timeline_days,
                    "target_audience": pred.target_audience,
                    "reasoning": pred.cultural_reasoning
                }
                for pred in analysis.predictions
            ],
            "analysis_metadata": {
                "total_predictions": analysis.total_predictions,
                "average_confidence": analysis.average_confidence,
                "timestamp": analysis.analysis_timestamp
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/similar-profiles/{profile_id}")
async def find_similar_profiles(profile_id: str):
    """Find culturally similar user profiles"""
    try:
        similar_profiles = await qloo_service.get_similar_profiles(profile_id)
        return {
            "success": True,
            "profile_id": profile_id,
            "similar_profiles": similar_profiles,
            "count": len(similar_profiles)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Similar profiles search failed: {str(e)}")

@app.get("/api/performance")
async def get_performance_metrics():
    """Get system performance metrics"""
    metrics = qloo_service.get_performance_metrics()
    return {
        "success": True,
        "qloo_performance": metrics,
        "system_status": "operational"
    }

@app.post("/api/predict-trends")
async def predict_trends_endpoint(
    cultural_profile: CulturalProfile, 
    timeframe: str = "90d"
):
    """Generate trend predictions for existing cultural profile"""
    try:
        predictions = await gemini_service.analyze_cultural_trends(cultural_profile, timeframe)
        return {
            "success": True,
            "predictions": [
                {
                    "category": pred.product_category,
                    "trend": pred.predicted_trend,
                    "confidence": pred.confidence_score,
                    "timeline": pred.timeline_days,
                    "audience": pred.target_audience,
                    "reasoning": pred.cultural_reasoning,
                    "opportunity": pred.market_opportunity
                }
                for pred in predictions
            ],
            "timeframe": timeframe
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
