from typing import List, Dict, Optional
from models.trend_models import UserPreferences, CulturalProfile, TrendPrediction, TrendAnalysis
from services.qloo_service import QlooService
from services.gemini_service import GeminiService
from datetime import datetime
import asyncio

class TrendAnalyzer:
     """Main trend analysis engine combining Qloo + Gemini insights"""
    
     def __init__(self):
        self.qloo_service = QlooService()
        self.gemini_service = GeminiService()
     
     async def predict_trends(self, user_preferences: UserPreferences, timeframe: str = "90d") -> TrendAnalysis:
        """
        Complete trend prediction pipeline
        
        Args:
            user_preferences: User's cultural preferences
            timeframe: Prediction timeframe (30d, 90d, 180d)
            
        Returns:
            Complete trend analysis with predictions
        """
        

        print("🔍 Creating cultural profile...")
        cultural_profile = await self.qloo_service.create_cultural_profile(user_preferences)
        
        if not cultural_profile:
            print("❌ Failed to create cultural profile")
            return self._create_empty_analysis(timeframe)
        
        print(f"✅ Cultural profile created (confidence: {cultural_profile.confidence_score}%)")
        

        print("🔍 Analyzing cultural communities...")
        similar_profiles = await self.qloo_service.get_similar_profiles(cultural_profile.profile_id)
        

        print("🤖 Generating trend predictions with Gemini...")
        predictions = await self.gemini_service.analyze_cultural_trends(cultural_profile, timeframe)
        

        enhanced_predictions = self._enhance_with_community_data(predictions, similar_profiles)
        
        final_predictions = self._score_and_rank_predictions(enhanced_predictions)
        
        print(f"✅ Generated {len(final_predictions)} trend predictions")
        
        return TrendAnalysis(
            predictions=final_predictions,
            analysis_date=datetime.now(),
            timeframe=timeframe,
            total_predictions=len(final_predictions),
            average_confidence=sum(p.confidence_score for p in final_predictions) / len(final_predictions) if final_predictions else 0
        )

     def _enhance_with_community_data(self,predictions: List[TrendPrediction], community_data: List[Dict]) -> List[TrendPrediction]:
             """Enhance predictions with insights from similar cultural profiles"""
             if not community_data:
               return predictions
             community_interests = []
             for profile in community_data:
                 community_interests.extend(profile.get("emerging_interest",[]))
             for prediction in predictions:
                 community_alignment = self._calculate_community_alignment(prediction,community_interests)
                 if community_alignment > 0.5:
                     prediction.confidence_score = min(95,prediction.confidence_score * 1.1)
                     prediction.cultural_reasoning += f"This Trend  aligns with emerging interests in similar cultural communities (alignment:{community_alignment:.0%}.)"

             return predictions
     def _calculate_commiunity_alignment(self,prediction: TrendPrediction, community_interests: List[str]) -> float:
         prediction_words = prediction.predicted_trend.lower.split()
         match=0
         for interest in community_interests:
             interest_words = interest.lower().split()
             if any(word in prediction_words for word in interest_words):
                matches += 1
         return matches / len(community_interests) if community_interests else 0
      
