# services/recommendation_service.py
from content.products_data import PRODUCT_RECOMMENDATIONS, EXPERIENCE_RECOMMENDATIONS
import random

class RecommendationService:
    def __init__(self):
        self.products = PRODUCT_RECOMMENDATIONS
        self.experiences = EXPERIENCE_RECOMMENDATIONS

    def get_personalized_recommendations(self, cultural_profile, brand_kit, recommendation_type="products", max_recommendations=6):
        """Get personalized recommendations based on cultural profile and brand kit"""
        try:
            recommendations = []
            
            # Extract user preferences from cultural profile
            preferences = self._extract_preferences_from_profile(cultural_profile)
            
            print(f"DEBUG - Extracted preferences: {preferences}")
            
            # Get products based on preferences
            if recommendation_type == "products":
                recommendations = self._get_matching_products(preferences, max_recommendations)
            elif recommendation_type == "experiences":
                recommendations = self._get_matching_experiences(preferences, max_recommendations)
            
            print(f"DEBUG - Found {len(recommendations)} recommendations")
            return recommendations
            
        except Exception as e:
            print(f"ERROR in get_personalized_recommendations: {e}")
            return self._get_fallback_recommendations(max_recommendations)

    def _extract_preferences_from_profile(self, cultural_profile):
        """Extract relevant keywords from cultural profile"""
        preferences = set()
        
        # Extract from cultural segments
        if hasattr(cultural_profile, 'cultural_segments'):
            for segment in cultural_profile.cultural_segments:
                segment_lower = segment.lower()
                if 'jazz' in segment_lower:
                    preferences.add('jazz')
                if 'sustain' in segment_lower:
                    preferences.add('sustainability')
                if 'creative' in segment_lower:
                    preferences.add('creative')
                if 'luxury' in segment_lower:
                    preferences.add('luxury')
                if 'local' in segment_lower:
                    preferences.add('local')
        
        # Extract from cross-domain connections
        if hasattr(cultural_profile, 'cross_domain_connections'):
            connections = cultural_profile.cross_domain_connections
            
            # Check music preferences
            music_prefs = connections.get('music', [])
            for music in music_prefs:
                if 'jazz' in music.lower():
                    preferences.add('jazz')
                if 'soul' in music.lower():
                    preferences.add('soul')
            
            # Check lifestyle preferences
            lifestyle_prefs = connections.get('lifestyle', [])
            for lifestyle in lifestyle_prefs:
                if 'sustain' in lifestyle.lower():
                    preferences.add('sustainability')
                if 'creative' in lifestyle.lower():
                    preferences.add('creative')
                if 'local' in lifestyle.lower():
                    preferences.add('local')
        
        # Add fallback preferences if none found
        if not preferences:
            preferences = {'jazz', 'sustainability'}  # Default to jazz (from your logs)
            
        return list(preferences)

    def _get_matching_products(self, preferences, max_recommendations):
        """Get products matching user preferences"""
        matching_products = []
        
        # Get products for each preference
        for pref in preferences:
            if pref in self.products:
                matching_products.extend(self.products[pref])
        
        # If no matches, add some default recommendations
        if not matching_products:
            # Add jazz products as fallback (since user showed jazz preference)
            if 'jazz' in self.products:
                matching_products.extend(self.products['jazz'])
            if 'sustainability' in self.products:
                matching_products.extend(self.products['sustainability'][:2])
        
        # Shuffle and limit results
        random.shuffle(matching_products)
        return matching_products[:max_recommendations]

    def _get_matching_experiences(self, preferences, max_recommendations):
        """Get experiences matching user preferences"""
        matching_experiences = []
        
        for pref in preferences:
            if pref in self.experiences:
                matching_experiences.extend(self.experiences[pref])
        
        random.shuffle(matching_experiences)
        return matching_experiences[:max_recommendations]

    def _get_fallback_recommendations(self, max_recommendations):
        """Fallback recommendations when everything else fails"""
        fallback = []
        
        # Add some products from each category
        for category, products in self.products.items():
            if products:
                fallback.append(products[0])  # Take first product from each category
                if len(fallback) >= max_recommendations:
                    break
        
        return fallback[:max_recommendations]

    def get_recommendation_summary(self, recommendations):
        """Generate a summary for the recommendations"""
        if not recommendations:
            return "Here are some curated recommendations for you:"
        
        categories = set(rec.get('category', 'General') for rec in recommendations)
        category_text = ', '.join(categories)
        
        return f"Based on your cultural DNA, here are {len(recommendations)} personalized recommendations spanning {category_text}:"
