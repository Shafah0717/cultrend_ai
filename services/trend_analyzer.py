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
                 community_alignment = self._calculate_commiunity_alignment(prediction,community_interests)
                 if community_alignment > 0.5:
                     prediction.confidence_score = min(95,prediction.confidence_score * 1.1)
                     prediction.cultural_reasoning += f"This Trend  aligns with emerging interests in similar cultural communities (alignment:{community_alignment:.0%}.)"

             return predictions
     def _calculate_commiunity_alignment(self,prediction: TrendPrediction, community_interests: List[str]) -> float:
         prediction_words = prediction.predicted_trend.lower().split()
         match=0
         for interest in community_interests:
             interest_words = interest.lower().split()
             if any(word in prediction_words for word in interest_words):
                matches += 1
         return matches / len(community_interests) if community_interests else 0
     def _score_and_rank_predictions(self,predictions: List[TrendPrediction]) -> List[TrendPrediction]:
         """Apply final scoring and ranking to predictions""" 
         for prediction in predictions:
             timeline_score = max(0.5,(180 - prediction.timeline_days)/180)
             market_keywords = ["growing","emerging","untapped","opportunity"]
             market_score = sum(1 for keyword in market_keywords if keyword in prediction.market_opportunity.lower()) / len(market_keywords)
             
             audience_score =  min(1.0, len(prediction.target_audience)/3)
             final_score = (
                     prediction.confidence_score * 0.5 +
                     timeline_score * 20 +
                     market_score * 15 +
                     audience_score * 15
             )
             prediction.confidence_score = min(95, final_score)

             return sorted(predictions, key=lambda p: p.confidence_score, reverse=True)
     def _create_empty_analysis(self, timeframe: str) -> TrendAnalysis:
            """Create empty analysis when cultural profile creation fails"""
            return TrendAnalysis(
               predictions=[],
               analysis_date=datetime.now(),
               timeframe=timeframe,
               total_predictions=0,
               average_confidence=0
            )
async def test_complete_pipeline():
         """Test the complete trend analysis pipeline"""
         test_preferences = UserPreferences(
            music_genres=["indie rock", "electronic", "folk"],
            dining_preferences=["artisanal coffee", "plant-based", "local sourcing"],
            fashion_styles=["minimalist", "sustainable", "vintage-inspired"],
            entertainment_types=["independent films", "live music", "podcasts"],
            lifestyle_choices=["sustainable living", "wellness", "remote work"]
         )
         analyzer = TrendAnalyzer()
         analysis = await analyzer.predict_trends(test_preferences, "90d")

         print("\n🎯 TREND ANALYSIS RESULTS")
         print("=" * 50)
         print(f"Timeframe: {analysis.timeframe}")
         print(f"Total Predictions: {analysis.total_predictions}")
         print(f"Average Confidence: {analysis.average_confidence:.1f}%")

         print("\n📈 TOP PREDICTIONS:")
         for i, prediction in enumerate(analysis.predictions[:3], 1):
                 print(f"\n{i}. {prediction.predicted_trend}")
                 print(f"   Category: {prediction.product_category}")
                 print(f"   Confidence: {prediction.confidence_score:.0f}%")
                 print(f"   Timeline: {prediction.timeline_days} days")
                 print(f"   Target: {', '.join(prediction.target_audience)}")
                 print(f"   Reasoning: {prediction.cultural_reasoning[:100]}...")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_complete_pipeline()) 


