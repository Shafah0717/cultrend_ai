# services/recommendation_service.py

from typing import List, Dict, Any
from models.trend_models import CulturalProfile, BrandIdentityKit
from content.products_data import PRODUCT_RECOMMENDATIONS, EXPERIENCE_RECOMMENDATIONS
import random

class RecommendationService:
    """Service for generating personalized product and experience recommendations"""
    
    def __init__(self):
        self.products = PRODUCT_RECOMMENDATIONS
        self.experiences = EXPERIENCE_RECOMMENDATIONS
    
    def get_personalized_recommendations(self, cultural_profile: CulturalProfile, 
                                       brand_kit: BrandIdentityKit, 
                                       recommendation_type: str = "products",
                                       max_recommendations: int = 6) -> List[Dict[str, Any]]:
        try:
            print(f"🛍️ Generating {recommendation_type} recommendations...")
            user_keywords = self._extract_user_keywords(cultural_profile, brand_kit)
            
            if recommendation_type == "products":
                recommendations = self._get_product_recommendations(user_keywords)
            elif recommendation_type == "experiences":
                recommendations = self._get_experience_recommendations(user_keywords)
            else:
                products = self._get_product_recommendations(user_keywords)
                experiences = self._get_experience_recommendations(user_keywords)
                recommendations = products + experiences
            
            scored_recommendations = self._score_recommendations(recommendations, user_keywords)
            top_recommendations = scored_recommendations[:max_recommendations]
            
            print(f"✅ Generated {len(top_recommendations)} personalized recommendations")
            return top_recommendations
            
        except Exception as e:
            print(f"❌ Error generating recommendations: {e}")
            return []

    def _extract_user_keywords(self, cultural_profile: CulturalProfile, brand_kit: BrandIdentityKit) -> List[str]:
        keywords = []
        if hasattr(cultural_profile, 'cultural_segments'):
            for segment in cultural_profile.cultural_segments:
                keywords.extend(segment.lower().replace('_', ' ').replace('-', ' ').split())
        
        if hasattr(cultural_profile, 'cross_domain_connections'):
            connections = cultural_profile.cross_domain_connections
            for pref_type in ["music", "fashion", "lifestyle", "dining"]:
                if pref_type in connections:
                    keywords.extend([item.lower() for item in connections[pref_type]])

        if hasattr(brand_kit, 'core_keywords'):
            keywords.extend([kw.lower() for kw in brand_kit.core_keywords])
        
        return list(set(kw for kw in keywords if len(kw) > 2))

    def _get_product_recommendations(self, user_keywords: List[str]) -> List[Dict[str, Any]]:
        recommendations = []
        for products in self.products.values():
            for product in products:
                if any(kw in user_keywords for kw in product.get('keywords', [])):
                    if product not in recommendations:
                        recommendations.append(product)
        return recommendations

    def _get_experience_recommendations(self, user_keywords: List[str]) -> List[Dict[str, Any]]:
        recommendations = []
        for experiences in self.experiences.values():
            for experience in experiences:
                if any(kw in user_keywords for kw in experience.get('keywords', [])):
                    if experience not in recommendations:
                        recommendations.append(experience)
        return recommendations

    def _score_recommendations(self, recommendations: List[Dict[str, Any]], user_keywords: List[str]) -> List[Dict[str, Any]]:
        for item in recommendations:
            score = sum(1 for kw in user_keywords if kw in item.get('keywords', []))
            item['relevance_score'] = score + random.uniform(0, 0.5)
        return sorted(recommendations, key=lambda x: x['relevance_score'], reverse=True)

    def get_recommendation_summary(self, recommendations: List[Dict[str, Any]]) -> str:
        if not recommendations:
            return "No recommendations found for your profile."
        categories = set(item.get('category', 'General') for item in recommendations)
        return f"Found {len(recommendations)} personalized recommendations across {', '.join(categories)}."

