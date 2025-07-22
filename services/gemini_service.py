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
        self.model = genai.GenerativeModel('gemini-1.5-pro')
     async def analyze_cultural_trends(self,cultural_profile:CulturalProfile,timeframe: str = "90d") -> List[TrendPrediction]:
        """
        Analyze cultural profile and predict trends using Gemini
        
        Args:
            cultural_profile: Cultural analysis from Qloo
            timeframe: Prediction timeframe (30d, 90d, 180d)
            
        Returns:
            List of trend predictions
        """

        # Create Gemini prompt
        prompt = self._create_gemini_prompt(cultural_profile, timeframe)

        try:
            # Generate content with Gemini
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2000,
                )
            )
            # Parse Gemini response into trend predictions
            predictions = self._parse_gemini_response(response.text, timeframe)
            return predictions
            
        except Exception as e:
            print(f"Error with Gemini analysis: {e}")
            # Return sample predictions for development
            return self._create_sample_predictions(timeframe)
        
     def _create_gemini_prompt(self, profile: CulturalProfile, timeframe: str) -> str:
         """Create comprehensive prompt for Gemini"""
        
         timeline_days = {"30d": 30, "90d": 90, "180d": 180}[timeframe]
                
         prompt = f"""
            You are an expert cultural intelligence analyst specializing in trend prediction. Your task is to analyze cultural preference patterns and predict emerging trends with high accuracy.

        ## Your Expertise:
        - Understanding cross-domain cultural connections (music ↔ fashion ↔ dining ↔ lifestyle)
        - Identifying early adopter communities and their influence patterns
        - Predicting product trends 3-6 months before mainstream adoption
        - Explaining cultural reasoning behind trend predictions

        ## Cultural Profile Analysis:

        **Cultural Segments:** {', '.join(profile.cultural_segments)}

        **Cross-Domain Connections:**
        {json.dumps(profile.cross_domain_connections, indent=2)}

        **Behavioral Indicators:**
        {json.dumps(profile.behavioral_indicators, indent=2)}

        **Profile Confidence:** {profile.confidence_score}%

        ## Analysis Requirements:

        Predict 5-7 emerging trends for the next {timeline_days} days based on this cultural profile. Focus on products or categories that don't exist yet but should, given these cultural patterns.

        ## Output Format:

        Provide your analysis in this exact JSON structure:

        {{
            "predictions": [
                {{
                    "product_category": "Fashion",
                    "predicted_trend": "Sustainable vintage-inspired tech accessories",
                    "confidence_score": 85,
                    "timeline_days": 75,
                    "target_audience": ["eco-conscious millennials", "indie music fans"],
                    "cultural_reasoning": "The intersection of vintage aesthetic preferences and sustainability values, amplified by indie music culture's influence on fashion choices, creates demand for tech accessories that blend nostalgic design with environmental consciousness.",
                    "market_opportunity": "Growing market for sustainable accessories among culturally-aware consumers who value both aesthetics and environmental impact"
                }}
            ]
        }}

        ## Key Guidelines:
        - Base predictions on cultural pattern intersections, not current trends
        - Explain WHY trends will emerge, not just WHAT will trend
        - Focus on 3-6 month lead time predictions
        - Assign realistic confidence scores (60-95%)
        - Target specific cultural communities, not broad demographics
        - Emphasize emerging opportunities, not established markets

        Analyze the cultural data and provide your trend predictions now:
        """
         return prompt
    
    


