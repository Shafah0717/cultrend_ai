from typing import List, Dict, Optional
from models.trend_models import UserPreferences, CulturalProfile, TrendPrediction, TrendAnalysis, BrandIdentityKit
from services.qloo_service import QlooService
from services.gemini_service import GeminiService
from datetime import datetime
import asyncio
import json
import re

def create_brand_identity_prompt(cultural_profile: CulturalProfile) -> str:
    """Enhanced prompt that leverages rich Qloo cultural data for authentic brand generation"""
    # Extract comprehensive cultural data
    segments = getattr(cultural_profile, 'cultural_segments', [])
    enhanced_segments = getattr(cultural_profile, 'enhanced_cultural_segments', [])
    all_segments = segments + enhanced_segments
    
    connections = getattr(cultural_profile, 'cross_domain_connections', {})
    brands = connections.get('brands', [])[:5]
    artists = connections.get('artists', [])[:5]
    places = connections.get('places', [])[:3]
    
    behavioral = getattr(cultural_profile, 'behavioral_indicators', {})
    early_adopter = behavioral.get('early_adopter', 0)
    cultural_openness = behavioral.get('cultural_openness', 0)
    
    # Build rich cultural context (FIXED: Unicode bullets replaced with dashes)
    cultural_context = f"""
**CULTURAL IDENTITY ANALYSIS:**
- Primary Segments: {', '.join(all_segments[:3]) if all_segments else 'Creative Individual'}
- Brand Affinities: {', '.join(brands) if brands else 'Emerging brands, authentic experiences'}
- Artist/Creator Influences: {', '.join(artists) if artists else 'Independent creators, authentic voices'}
- Place Connections: {', '.join(places) if places else 'Local communities, creative spaces'}
- Innovation Level: {'High' if early_adopter > 0.7 else 'Moderate' if early_adopter > 0.4 else 'Selective'} early adopter
- Cultural Openness: {'Very High' if cultural_openness > 0.8 else 'High' if cultural_openness > 0.6 else 'Moderate'}
"""

    prompt = f"""
You are an expert brand strategist working with a client who has undergone deep cultural analysis. Create a personal brand identity that authentically reflects their unique cultural DNA.

{cultural_context}

**TASK:** Generate a complete brand identity kit that captures this person's authentic cultural essence. The brand should feel genuine, aspirational, and commercially viable.

**OUTPUT FORMAT:** Provide ONLY valid JSON matching this exact structure:

{{
    "brand_name": "A distinctive, memorable name (2-3 words max) that reflects their cultural identity",
    "tagline": "A powerful 4-8 word slogan that captures their essence and values",
    "mission_statement": "A compelling 2-3 sentence statement of purpose that connects their cultural values to their brand promise",
    "core_keywords": ["5-7 keywords that define their brand personality and market position"],
    "color_palette": {{
        "primary": "#HEXCODE",
        "secondary": "#HEXCODE", 
        "accent": "#HEXCODE",
        "neutral": "#HEXCODE"
    }},
    "social_media_bio": "An engaging 120-character bio perfect for Instagram/LinkedIn that showcases their unique value"
}}

**BRAND GUIDELINES:**
- Reflect their cultural segments in the naming and tone
- Color palette should mirror their aesthetic preferences and lifestyle
- Mission should connect personal values to professional/creative purpose  
- Keywords should be searchable and relevant to their industries/interests
- Bio should be compelling enough to attract their target community

Focus on authenticity over generic appeal. This brand should feel unmistakably THEIRS.
"""
    return prompt

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
            
            # FIXED: Use the correct method name that matches your dashboard
            if self.qloo_service:
                cultural_profile = await self.qloo_service.get_enhanced_cultural_insights(user_preferences)
            else:
                cultural_profile = None
            
            if not cultural_profile:
                print("❌ Failed to create cultural profile")
                return self._create_empty_analysis(timeframe)
            
            print(f"✅ Cultural profile created (confidence: {cultural_profile.confidence_score}%)")
            
            # Handle Gemini quota gracefully
            predictions = []
            if self.gemini_service:
                try:
                    print("🤖 Generating trend predictions with Gemini...")
                    predictions = await self.gemini_service.analyze_cultural_trends(cultural_profile, timeframe)
                except Exception as e:
                    print(f"⚠️ Gemini quota exceeded, using enhanced fallback: {e}")
                    predictions = self._create_enhanced_predictions(cultural_profile, timeframe)
            else:
                predictions = self._create_enhanced_predictions(cultural_profile, timeframe)
            
            # Enhance and rank predictions
            enhanced_predictions = self._enhance_with_community_data(predictions, [])
            final_predictions = self._score_and_rank_predictions(enhanced_predictions)
            
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
        """Generate brand identity kit from cultural profile using Gemini"""
        try:
            prompt = create_brand_identity_prompt(cultural_profile)
            print("🎨 Generating brand identity with enhanced cultural context...")

            if self.gemini_service:
                try:
                    response_text = await self.gemini_service.analyze_cultural_trends_with_custom_prompt(cultural_profile, prompt)
                    clean_text = response_text.strip()

                    # Extract JSON using regex
                    json_match = re.search(r"\{.*\}", clean_text, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(0)
                        json_data = json.loads(json_str)
                        brand_kit = BrandIdentityKit(**json_data)
                        print(f"✅ Brand identity created: {brand_kit.brand_name}")
                        return brand_kit
                except Exception as e:
                    print(f"⚠️ Gemini quota exceeded for brand generation: {e}")

            # Enhanced fallback based on cultural profile
            print("🎨 Using enhanced fallback brand identity")
            return self._create_fallback_brand_kit(cultural_profile)

        except Exception as e:
            print(f"❌ Brand generation error: {e}")
            return self._create_fallback_brand_kit(cultural_profile)

    def _create_enhanced_predictions(self, cultural_profile: CulturalProfile, timeframe: str) -> List[TrendPrediction]:
        """Create enhanced predictions based on cultural profile"""
        timeline_days = {"30d": 30, "90d": 90, "180d": 180}[timeframe]
        
        # Extract user preferences from cultural profile
        connections = getattr(cultural_profile, 'cross_domain_connections', {})
        segments = getattr(cultural_profile, 'cultural_segments', [])
        
        predictions = []
        
        # Jazz-specific prediction (based on your logs showing jazz preference)
        if any('jazz' in str(item).lower() for item in connections.get('music', []) + segments):
            predictions.append(TrendPrediction(
                product_category="Music & Culture",
                predicted_trend="AI-curated jazz fusion experiences",
                confidence_score=88.0,
                timeline_days=timeline_days - 15,
                target_audience=["jazz enthusiasts", "cultural explorers"],
                cultural_reasoning="Your jazz preference indicates appreciation for sophisticated, authentic cultural experiences.",
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
                cultural_reasoning="Your profile suggests appreciation for authentic, meaningful products.",
                market_opportunity="Growing demand for sustainable products with authentic cultural connections."
            )
        ])
        
        return predictions

    def _create_fallback_brand_kit(self, cultural_profile: CulturalProfile) -> BrandIdentityKit:
        """Create a fallback brand kit based on cultural segments"""
        segments = getattr(cultural_profile, 'cultural_segments', ['Creative Individual'])
        connections = getattr(cultural_profile, 'cross_domain_connections', {})
        
        # Customize based on jazz preference (from your logs)
        if any('jazz' in str(item).lower() for item in connections.get('music', []) + segments):
            return BrandIdentityKit(
                brand_name="Jazz Collective",
                tagline="Authentic Rhythm, Modern Soul",
                mission_statement="Bridging timeless jazz heritage with contemporary cultural expression through authentic storytelling and community connection.",
                core_keywords=["authentic", "jazz", "cultural", "storytelling", "community"],
                color_palette={"primary": "#2C3E50", "secondary": "#E67E22", "accent": "#F39C12", "neutral": "#95A5A6"},
                social_media_bio="Jazz culture curator & authentic storyteller | Where tradition meets innovation 🎷"
            )
        
        # Other segment-based fallbacks
        primary_segment = segments[0] if segments else 'Creative Individual'
        
        if 'indie' in primary_segment.lower():
            return BrandIdentityKit(
                brand_name="Indie Collective",
                tagline="Authentically Different",
                mission_statement="Curating unique experiences that celebrate independent creativity and authentic self-expression in a world of mass production.",
                core_keywords=["authentic", "independent", "creative", "unique", "community"],
                color_palette={"primary": "#2C3E50", "secondary": "#E67E22", "accent": "#F39C12", "neutral": "#BDC3C7"},
                social_media_bio="Independent creator & cultural curator | Authentic experiences over mainstream trends ✨"
            )
        elif 'sustain' in primary_segment.lower():
            return BrandIdentityKit(
                brand_name="Conscious Collective",
                tagline="Purpose Driven Living",
                mission_statement="Inspiring sustainable choices through mindful consumption and community-driven initiatives that create positive impact.",
                core_keywords=["sustainable", "mindful", "purpose-driven", "community", "impact"],
                color_palette={"primary": "#27AE60", "secondary": "#2ECC71", "accent": "#F1C40F", "neutral": "#95A5A6"},
                social_media_bio="Sustainable living advocate | Conscious choices for a better tomorrow 🌱"
            )
        else:
            return BrandIdentityKit(
                brand_name="Cultural Navigator",
                tagline="Exploring What's Next",
                mission_statement="Bridging cultures and communities through curiosity-driven exploration and authentic storytelling.",
                core_keywords=["explorer", "cultural", "authentic", "storytelling", "community"],
                color_palette={"primary": "#9B59B6", "secondary": "#8E44AD", "accent": "#E74C3C", "neutral": "#34495E"},
                social_media_bio="Cultural explorer & trend navigator | Finding meaning in the spaces between 🗺️"
            )

    def _enhance_with_community_data(self, predictions: List[TrendPrediction], community_data: List[Dict]) -> List[TrendPrediction]:
        """Enhance predictions with insights from similar cultural profiles"""
        if not community_data:
            return predictions
        
        community_interests = []
        for profile in community_data:
            community_interests.extend(profile.get("emerging_interests", []))
        
        for prediction in predictions:
            community_alignment = self._calculate_community_alignment(prediction, community_interests)
            if community_alignment > 0.5:
                prediction.confidence_score = min(95, prediction.confidence_score * 1.1)
                prediction.cultural_reasoning += f" This trend aligns with emerging interests in similar cultural communities (alignment: {community_alignment:.0%})."
        
        return predictions

    def _calculate_community_alignment(self, prediction: TrendPrediction, community_interests: List[str]) -> float:
        """Calculate alignment between prediction and community interests"""
        prediction_words = prediction.predicted_trend.lower().split()
        matches = 0
        for interest in community_interests:
            interest_words = interest.lower().split()
            if any(word in prediction_words for word in interest_words):
                matches += 1
        return matches / len(community_interests) if community_interests else 0

    def _score_and_rank_predictions(self, predictions: List[TrendPrediction]) -> List[TrendPrediction]:
        """Apply final scoring and ranking to predictions"""
        for prediction in predictions:
            timeline_score = max(0.5, (180 - prediction.timeline_days) / 180)
            market_keywords = ["growing", "emerging", "untapped", "opportunity"]
            market_score = sum(1 for keyword in market_keywords if keyword in prediction.market_opportunity.lower()) / len(market_keywords)
            audience_score = min(1.0, len(prediction.target_audience) / 3)
            
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
        # FIXED: Added missing cultural_profile parameter
        return TrendAnalysis(
            predictions=[],
            cultural_profile=None,  # ← This was missing
            analysis_date=datetime.now(),
            timeframe=timeframe,
            total_predictions=0,
            average_confidence=0
        )
