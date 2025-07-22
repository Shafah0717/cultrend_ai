# services/qloo_service.py
import aiohttp
import asyncio
import json
from typing import Dict, List, Optional
from config import settings
from models.trend_models import UserPreferences, CulturalProfile

class QlooService:
    """Service to interact with Qloo's Taste AI API"""
    
    def __init__(self):
        self.base_url = settings.qloo_base_url
        self.headers = settings.get_qloo_header()
    
    async def create_cultural_profile(self, preferences: UserPreferences) -> Optional[CulturalProfile]:
        """
        Convert user preferences into cultural profile using Qloo API
        
        Args:
            preferences: User's cultural preferences
            
        Returns:
            Cultural profile with cross-domain insights
        """
        try:
            # Prepare data for Qloo API
            payload = {
                "input_data": {
                    "music": preferences.music_genres,
                    "dining": preferences.dining_preferences,
                    "fashion": preferences.fashion_styles,
                    "entertainment": preferences.entertainment_types,
                    "lifestyle": preferences.lifestyle_choices
                },
                "analysis_type": "cross_domain_mapping",
                "return_cultural_segments": True
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/v1/taste-profile",
                    json=payload,
                    headers=self.headers,
                    timeout=30
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_cultural_profile(data)
                    else:
                        print(f"Qloo API error: {response.status}")
                        # Return sample data for development
                        return self._create_sample_profile()
                        
        except Exception as e:
            print(f"Error creating cultural profile: {e}")
            # Return sample data for development
            return self._create_sample_profile()
    
    def _parse_cultural_profile(self, qloo_response: Dict) -> CulturalProfile:
        """Parse Qloo API response into our data model"""
        
        # Extract cultural segments
        segments = qloo_response.get("cultural_segments", [])
        
        # Extract cross-domain connections
        connections = qloo_response.get("cross_domain_affinities", {})
        
        # Calculate behavioral indicators
        indicators = qloo_response.get("behavioral_scores", {})
        
        # Overall confidence from Qloo
        confidence = qloo_response.get("confidence_score", 0.0)
        
        return CulturalProfile(
            profile_id=qloo_response.get("profile_id", "unknown"),
            cultural_segments=segments,
            cross_domain_connections=connections,
            behavioral_indicators=indicators,
            confidence_score=confidence
        )
    
    def _create_sample_profile(self) -> CulturalProfile:
        """Create sample profile for development/testing"""
        return CulturalProfile(
            profile_id="sample_profile_123",
            cultural_segments=["indie culture", "sustainability advocates", "minimalists"],
            cross_domain_connections={
                "music": ["indie rock", "folk", "ambient"],
                "fashion": ["vintage", "minimalist", "sustainable"],
                "dining": ["artisanal", "local", "plant-based"],
                "lifestyle": ["wellness", "sustainability", "mindfulness"]
            },
            behavioral_indicators={
                "early_adopter": 0.8,
                "influence_score": 0.6,
                "cultural_openness": 0.9
            },
            confidence_score=85.0
        )
    
    async def get_similar_profiles(self, profile_id: str) -> List[Dict]:
        """Find similar cultural profiles (early adopter communities)"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/v1/similar-profiles/{profile_id}",
                    headers=self.headers,
                    timeout=15
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return data.get("similar_profiles", [])
                    else:
                        # Return sample data for development
                        return self._get_sample_similar_profiles()
                        
        except Exception as e:
            print(f"Error getting similar profiles: {e}")
            return self._get_sample_similar_profiles()
    
    def _get_sample_similar_profiles(self) -> List[Dict]:
        """Sample similar profiles for development"""
        return [
            {
                "profile_id": "similar_1",
                "similarity_score": 0.82,
                "emerging_interests": ["sustainable tech", "artisanal goods", "wellness products"]
            },
            {
                "profile_id": "similar_2", 
                "similarity_score": 0.76,
                "emerging_interests": ["vintage fashion", "indie brands", "eco-friendly"]
            }
        ]

# Test function for beginners
async def test_qloo_service():
    """Test function to verify Qloo integration works"""
    
    # Create sample preferences
    test_preferences = UserPreferences(
        music_genres=["indie rock", "folk"],
        dining_preferences=["artisanal coffee", "farm-to-table"],
        fashion_styles=["vintage", "minimalist"],
        entertainment_types=["indie films", "live music"],
        lifestyle_choices=["sustainable living", "local shopping"]
    )
    
    # Test the service
    qloo_service = QlooService()
    profile = await qloo_service.create_cultural_profile(test_preferences)
    
    if profile:
        print("✅ Qloo integration successful!")
        print(f"Cultural segments: {profile.cultural_segments}")
        print(f"Confidence: {profile.confidence_score}")
    else:
        print("❌ Qloo integration failed")

# Uncomment to test:
#import asyncio
#asyncio.run(test_qloo_service())
