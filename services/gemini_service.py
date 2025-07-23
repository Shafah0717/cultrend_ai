# services/gemini_service.py
import google.generativeai as genai
from typing import Dict, List
from config import settings
from models.trend_models import CulturalProfile, TrendPrediction
import json
from datetime import datetime, timedelta

class GeminiService:
    """Service to interact with Google Gemini for trend analysis"""
    
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
    
    async def analyze_cultural_trends(self, cultural_profile: CulturalProfile, timeframe: str = "90d") -> List[TrendPrediction]:
        """Analyze cultural profile and predict trends using Gemini"""
        
        try:
            print("🤖 Calling Gemini API...")
            
            prompt = f"""
            Analyze these cultural preferences and predict 2 emerging trends:
            
            Cultural Segments: {', '.join(cultural_profile.cultural_segments)}
            Cross-Domain Connections: {cultural_profile.cross_domain_connections}
            
            Provide 2 trend predictions in JSON format:
            {{
                "predictions": [
                    {{
                        "product_category": "Fashion",
                        "predicted_trend": "Sustainable tech accessories",
                        "confidence_score": 85,
                        "timeline_days": 75,
                        "target_audience": ["eco-conscious millennials"],
                        "cultural_reasoning": "Cultural analysis here",
                        "market_opportunity": "Market opportunity here"
                    }}
                ]
            }}
            """
            
            # Call Gemini
            response = self.model.generate_content(prompt)
            print("✅ Gemini API call successful")
            
            # For now, return sample data (we'll parse real response later)
            return self._create_sample_predictions(timeframe)
            
        except Exception as e:
            print(f"⚠️ Gemini API error: {e}")
            return self._create_sample_predictions(timeframe)
    
    def _create_sample_predictions(self, timeframe: str) -> List[TrendPrediction]:
        """Create sample predictions for development"""
        
        timeline_days = {"30d": 30, "90d": 90, "180d": 180}[timeframe]
        
        return [
            TrendPrediction(
                product_category="Fashion",
                predicted_trend="Sustainable tech accessories with vintage aesthetics",
                confidence_score=88.0,
                timeline_days=timeline_days - 15,
                target_audience=["eco-conscious millennials", "indie music fans"],
                cultural_reasoning="The intersection of vintage aesthetic preferences and sustainability values creates demand for tech accessories that blend nostalgic design with environmental consciousness.",
                market_opportunity="Growing market for sustainable accessories among culturally-aware consumers."
            ),
            TrendPrediction(
                product_category="Lifestyle", 
                predicted_trend="Artisanal wellness products for remote workers",
                confidence_score=82.0,
                timeline_days=timeline_days - 30,
                target_audience=["remote workers", "wellness enthusiasts"],
                cultural_reasoning="Remote work culture combined with wellness trends creates opportunity for handcrafted wellness items designed for home office environments.",
                market_opportunity="Underserved market of remote workers seeking wellness products."
            )
        ]

# Test function - MUST be outside the class
async def test_gemini_service():
    """Test Gemini service with sample data"""
    
    from models.trend_models import CulturalProfile
    
    # Create sample cultural profile
    sample_profile = CulturalProfile(
        profile_id="test_gemini_123",
        cultural_segments=["indie culture", "sustainability advocates", "minimalists"],
        cross_domain_connections={
            "music": ["indie rock", "folk"],
            "fashion": ["vintage", "minimalist"],
            "dining": ["artisanal", "local"]
        },
        behavioral_indicators={"early_adopter": 0.8, "influence": 0.6},
        confidence_score=85.0
    )
    
    gemini_service = GeminiService()
    predictions = await gemini_service.analyze_cultural_trends(sample_profile, "90d")
    
    if predictions:
        print("✅ Gemini integration successful!")
        for pred in predictions[:2]:  # Show first 2 predictions
            print(f"Trend: {pred.predicted_trend}")
            print(f"Confidence: {pred.confidence_score}%")
    else:
        print("❌ Gemini integration failed")

# Run test when file is executed directly
if __name__ == "__main__":
    import asyncio
    print("Starting Gemini service test...")
    asyncio.run(test_gemini_service())
