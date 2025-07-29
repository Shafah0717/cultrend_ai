# services/explanation_service.py

from models.trend_models import CulturalProfile, BrandIdentityKit

class ExplanationService:
    """
    Service to generate clear, user-friendly explanations for why
    a product or experience was recommended.
    """
    def get_recommendation_explanation(self, product: dict, profile: CulturalProfile, brand_kit: BrandIdentityKit) -> dict:
        """
        Generates a dictionary of reasons for a recommendation.
        """
        explanations = {}

        # 1. Match based on cultural segments
        if profile.cultural_segments:
            # Match the product's keywords to the user's cultural segments
            product_keywords = product.get("keywords", [])
            for segment in profile.cultural_segments:
                segment_keyword = segment.split()[0].lower() # e.g., 'wellness' from 'wellness advocates'
                if segment_keyword in product_keywords:
                    explanations['cultural_match'] = f"Matches your '{segment}' lifestyle."
                    break # Stop after finding the first match

        # 2. Match based on brand identity
        if brand_kit and brand_kit.core_keywords:
            product_keywords = product.get("keywords", [])
            for keyword in brand_kit.core_keywords:
                if keyword.lower() in product_keywords:
                    explanations['brand_alignment'] = f"Aligns with your brand's core value of '{keyword.title()}'."
                    break

        # 3. Match based on specific user preferences
        if profile.cross_domain_connections:
            connections = profile.cross_domain_connections
            product_keywords = product.get("keywords", [])
            
            # Check music, fashion, etc.
            for preference_type in ["music", "fashion", "lifestyle", "dining"]:
                if preference_type in connections:
                    for user_preference in connections[preference_type]:
                        if user_preference.lower() in product_keywords:
                            explanations['preference_match'] = f"Connects with your interest in {user_preference.title()}."
                            # Use break to only show the first, most direct match
                            break
                if 'preference_match' in explanations:
                    break

        # If no specific matches, provide a general reason
        if not explanations:
            explanations['general_match'] = "This is a popular choice among people with similar cultural tastes."

        return explanations

