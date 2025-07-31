from typing import List, Dict, Optional
import asyncio
import json
import re
from datetime import datetime

# Import your models
from models.trend_models import (
    UserPreferences, 
    CulturalProfile, 
    TrendPrediction, 
    BrandIdentityKit
)

# Import your services
from services.qloo_service import QlooService
from services.gemini_service import GeminiService

class TrendAnalysis:
    """Container for trend analysis results"""
    
    def __init__(self, predictions: List[TrendPrediction], cultural_profile: CulturalProfile, 
                 analysis_date: datetime, timeframe: str, total_predictions: int, average_confidence: float):
        self.predictions = predictions
        self.cultural_profile = cultural_profile
        self.analysis_date = analysis_date
        self.timeframe = timeframe
        self.total_predictions = total_predictions
        self.average_confidence = average_confidence

class TrendAnalyzer:
    """Main trend analysis engine combining Qloo + Gemini insights"""
    
    def __init__(self):
        try:
            self.qloo_service = QlooService()
            self.gemini_service = GeminiService()
            print("✅ TrendAnalyzer initialized successfully")
        except Exception as e:
            print(f"⚠️ TrendAnalyzer initialization error: {e}")
            self.qloo_service = None
            self.gemini_service = None
    
    async def predict_trends(self, user_preferences: UserPreferences, timeframe: str = "90d") -> TrendAnalysis:
        """Complete trend prediction pipeline"""
        try:
            print("🔍 Creating cultural profile...")
            
            if self.qloo_service:
                # Use the working Qloo service
                cultural_profile = await self.qloo_service.get_enhanced_cultural_insights(user_preferences)
            else:
                cultural_profile = self._create_fallback_cultural_profile(user_preferences)
            
            if not cultural_profile:
                print("❌ Failed to create cultural profile")
                return self._create_empty_analysis(timeframe)
            
            print(f"✅ Cultural profile created (confidence: {cultural_profile.confidence_score}%)")
            
            # Generate predictions (with Gemini fallback due to quota)
            predictions = []
            if self.gemini_service:
                try:
                    print("🤖 Attempting Gemini predictions...")
                    predictions = await self.gemini_service.analyze_cultural_trends(cultural_profile, timeframe)
                except Exception as e:
                    print(f"⚠️ Gemini quota exceeded, using enhanced fallback: {e}")
                    predictions = self._create_enhanced_predictions(cultural_profile, timeframe)
            else:
                predictions = self._create_enhanced_predictions(cultural_profile, timeframe)
            
            final_predictions = self._score_and_rank_predictions(predictions)
            
            print(f"✅ Generated {len(final_predictions)} trend predictions")
            
            return TrendAnalysis(
                predictions=final_predictions,
                cultural_profile=cultural_profile,
                analysis_date=datetime.now(),
                timeframe=timeframe,
                total_predictions=len(final_predictions),
                average_confidence=sum(p.confidence_score for p in final_predictions) / len(final_predictions) if final_predictions else 0
            )
            
        except Exception as e:
            print(f"❌ Error in trend analysis: {e}")
            return self._create_empty_analysis(timeframe)

    async def generate_brand_identity(self, cultural_profile: CulturalProfile) -> BrandIdentityKit:
        """Generate brand identity kit from cultural profile"""
        try:
            print("🎨 Generating brand identity...")
            
            if self.gemini_service:
                try:
                    prompt = self._create_brand_identity_prompt(cultural_profile)
                    response_text = await self.gemini_service.analyze_cultural_trends_with_custom_prompt(
                        cultural_profile, prompt
                    )
                    
                    if response_text:
                        brand_kit = self._parse_brand_identity_response(response_text)
                        print(f"✅ Brand identity created: {brand_kit.brand_name}")
                        return brand_kit
                except Exception as e:
                    print(f"⚠️ Gemini quota exceeded for brand generation: {e}")
            
            # Fallback brand identity (enhanced based on cultural profile)
            print("🎨 Using enhanced fallback brand identity")
            return self._create_enhanced_brand_kit(cultural_profile)
            
        except Exception as e:
            print(f"❌ Error generating brand identity: {e}")
            return self._create_enhanced_brand_kit(cultural_profile)

    def _create_brand_identity_prompt(self, cultural_profile: CulturalProfile) -> str:
        """Create enhanced prompt for brand identity generation"""
        segments = getattr(cultural_profile, 'cultural_segments', [])
        connections = getattr(cultural_profile, 'cross_domain_connections', {})
        
        cultural_context = f"""
**CULTURAL IDENTITY ANALYSIS:**
- Primary Segments: {', '.join(segments[:3]) if segments else 'Creative Individual'}
- Brand Affinities: {', '.join(connections.get('brands', [])[:3])}
- Music Preferences: {', '.join(connections.get('music', []))}
- Lifestyle Elements: {', '.join(connections.get('lifestyle', []))}
"""

        return f"""
Create a personal brand identity based on this cultural analysis:
{cultural_context}

Generate ONLY valid JSON:
{{
    "brand_name": "Unique 2-3 word name",
    "tagline": "Compelling 4-8 word slogan",
    "mission_statement": "2-3 sentence purpose statement",
    "core_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "color_palette": {{
        "primary": "#HEXCODE",
        "secondary": "#HEXCODE",
        "accent": "#HEXCODE",
        "neutral": "#HEXCODE"
    }},
    "social_media_bio": "Engaging 120-character bio"
}}
"""

    def _parse_brand_identity_response(self, response: str) -> BrandIdentityKit:
        """Parse brand identity from response"""
        try:
            # Extract JSON using regex
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                return BrandIdentityKit(**data)
        except Exception as e:
            print(f"⚠️ JSON parsing error: {e}")
        
        return self._create_enhanced_brand_kit(None)

    def _create_enhanced_brand_kit(self, cultural_profile: Optional[CulturalProfile]) -> BrandIdentityKit:
        """Create enhanced brand kit based on cultural profile"""
        if cultural_profile:
            segments = getattr(cultural_profile, 'cultural_segments', [])
            connections = getattr(cultural_profile, 'cross_domain_connections', {})
            music_prefs = connections.get('music', [])
            
            # Customize based on jazz preference (from your logs)
            if any('jazz' in str(item).lower() for item in music_prefs + segments):
                return BrandIdentityKit(
                    brand_name="Jazz Collective",
                    tagline="Authentic Rhythm, Modern Soul",
                    mission_statement="Bridging timeless jazz heritage with contemporary cultural expression through authentic storytelling and community connection.",
                    core_keywords=["authentic", "jazz", "cultural", "storytelling", "community"],
                    color_palette={
                        "primary": "#2C3E50",
                        "secondary": "#E67E22",
                        "accent": "#F39C12",
                        "neutral": "#95A5A6"
                    },
                    social_media_bio="Jazz culture curator & authentic storyteller | Where tradition meets innovation 🎷"
                )
        
        # Default fallback
        return BrandIdentityKit(
            brand_name="Cultural Navigator",
            tagline="Exploring What's Next",
            mission_statement="Bridging cultures and communities through curiosity-driven exploration and authentic storytelling.",
            core_keywords=["explorer", "cultural", "authentic", "storytelling", "community"],
            color_palette={
                "primary": "#9B59B6",
                "secondary": "#8E44AD", 
                "accent": "#E74C3C",
                "neutral": "#34495E"
            },
            social_media_bio="Cultural explorer & trend navigator | Finding meaning in the spaces between 🗺️"
        )

    def _create_enhanced_predictions(self, cultural_profile: CulturalProfile, timeframe: str) -> List[TrendPrediction]:
        """Create enhanced predictions based on cultural profile"""
        timeline_days = {"30d": 30, "90d": 90, "180d": 180}[timeframe]
        
        # Extract user preferences
        connections = getattr(cultural_profile, 'cross_domain_connections', {})
        music_prefs = connections.get('music', [])
        segments = getattr(cultural_profile, 'cultural_segments', [])
        
        predictions = []
        
        # Jazz-specific prediction (based on your logs showing jazz preference)
        if any('jazz' in str(item).lower() for item in music_prefs + segments):
            predictions.append(TrendPrediction(
                product_category="Music & Culture",
                predicted_trend="Neo-jazz fusion experiences with AI-curated playlists",
                confidence_score=88.0,
                timeline_days=timeline_days - 15,
                target_audience=["jazz enthusiasts", "cultural explorers"],
                cultural_reasoning="Your jazz preference indicates appreciation for sophisticated, authentic cultural experiences that blend tradition with innovation.",
                market_opportunity="Growing market for personalized jazz experiences leveraging AI curation."
            ))
        
        # Add universal predictions
        predictions.extend([
            TrendPrediction(
                product_category="Cultural Experiences",
                predicted_trend="Hyperlocal cultural discovery platforms",
                confidence_score=82.0,
                timeline_days=timeline_days - 20,
                target_audience=["cultural enthusiasts", "experience seekers"],
                cultural_reasoning="Based on your cultural segments, you value authentic, community-driven experiences.",
                market_opportunity="Emerging market for AI-powered local cultural recommendations."
            ),
            TrendPrediction(
                product_category="Lifestyle",
                predicted_trend="Sustainable artisan marketplace with cultural storytelling",
                confidence_score=79.0,
                timeline_days=timeline_days,
                target_audience=["conscious consumers", "culture advocates"],
                cultural_reasoning="Your profile suggests appreciation for authentic, meaningful products with cultural narratives.",
                market_opportunity="Growing demand for sustainable products with authentic cultural connections."
            )
        ])
        
        return predictions

    def _score_and_rank_predictions(self, predictions: List[TrendPrediction]) -> List[TrendPrediction]:
        """Apply final scoring and ranking"""
        for prediction in predictions:
            # Score based on timeline, market opportunity, and audience
            timeline_score = max(0.5, (180 - prediction.timeline_days) / 180)
            market_score = len(prediction.market_opportunity.split()) / 20  # Rough relevance score
            audience_score = min(1.0, len(prediction.target_audience) / 3)
            
            final_score = (
                prediction.confidence_score * 0.6 +
                timeline_score * 15 +
                market_score * 15 +
                audience_score * 10
            )
            prediction.confidence_score = min(95, final_score)
        
        return sorted(predictions, key=lambda p: p.confidence_score, reverse=True)

    def _create_fallback_cultural_profile(self, user_preferences: UserPreferences) -> CulturalProfile:
        """Create fallback cultural profile"""
        segments = ["cultural explorers"]
        
        # Add segments based on preferences
        if user_preferences.music_genres:
            if 'jazz' in user_preferences.music_genres:
                segments.append("jazz enthusiasts")
        
        return CulturalProfile(
            profile_id=f"fallback_{datetime.now().isoformat()}",
            cultural_segments=segments,
            cross_domain_connections={
                'music': user_preferences.music_genres,
                'lifestyle': user_preferences.lifestyle_choices,
                'entertainment': user_preferences.entertainment_types
            },
            behavioral_indicators={
                "early_adopter": 0.75,
                "cultural_openness": 0.85
            },
            confidence_score=75.0
        )

    def _create_empty_analysis(self, timeframe: str) -> TrendAnalysis:
        """Create empty analysis when everything fails"""
        return TrendAnalysis(
            predictions=[],
            cultural_profile=None,
            analysis_date=datetime.now(),
            timeframe=timeframe,
            total_predictions=0,
            average_confidence=0
        )
