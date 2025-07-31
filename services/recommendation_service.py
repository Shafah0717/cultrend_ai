# services/recommendation_service.py
from content.products_data import PRODUCT_RECOMMENDATIONS, EXPERIENCE_RECOMMENDATIONS
import random

class RecommendationService:
    def __init__(self):
        try:
            self.products = PRODUCT_RECOMMENDATIONS
            self.experiences = EXPERIENCE_RECOMMENDATIONS
            print(f"✅ DEBUG - Loaded {len(self.products)} product categories")
            print(f"✅ DEBUG - Available categories: {list(self.products.keys())}")
            
            # Debug: Show products per category
            for category, products in self.products.items():
                print(f"   - {category}: {len(products)} products")
                if products:
                    print(f"     Example: {products[0].get('name', 'Unknown')}")
        except ImportError as e:
            print(f"❌ Failed to import product data: {e}")
            self.products = {}
            self.experiences = {}

    def get_personalized_recommendations(self, cultural_profile, brand_kit, recommendation_type="products", max_recommendations=6):
        """Get personalized recommendations based on cultural profile and brand kit"""
        print("🔍 DEBUG - get_personalized_recommendations called")
        print(f"🔍 DEBUG - Cultural profile exists: {cultural_profile is not None}")
        print(f"🔍 DEBUG - Brand kit exists: {brand_kit is not None}")
        print(f"🔍 DEBUG - Recommendation type: {recommendation_type}")
        print(f"🔍 DEBUG - Max recommendations: {max_recommendations}")
        
        try:
            recommendations = []
            
            # Extract user preferences from cultural profile
            preferences = self._extract_preferences_from_profile(cultural_profile)
            print(f"🔍 DEBUG - Extracted preferences: {preferences}")
            
            # Get products based on preferences
            if recommendation_type == "products":
                recommendations = self._get_matching_products(preferences, max_recommendations)
            elif recommendation_type == "experiences":
                recommendations = self._get_matching_experiences(preferences, max_recommendations)
            
            print(f"🔍 DEBUG - Found {len(recommendations)} recommendations")
            
            # CRITICAL FIX: Force fallback if no recommendations found
            if not recommendations or len(recommendations) == 0:
                print("⚠️ DEBUG - No recommendations found, using enhanced fallback")
                recommendations = self._get_enhanced_fallback_recommendations(max_recommendations)
            
            # Final validation
            print(f"🔍 DEBUG - Final recommendations count: {len(recommendations)}")
            if recommendations:
                for i, rec in enumerate(recommendations[:3]):
                    print(f"   {i+1}. {rec.get('name', 'Unknown')} - {rec.get('price', 'No price')}")
            
            return recommendations
            
        except Exception as e:
            print(f"❌ ERROR in get_personalized_recommendations: {e}")
            import traceback
            traceback.print_exc()
            return self._get_enhanced_fallback_recommendations(max_recommendations)

    def _extract_preferences_from_profile(self, cultural_profile):
        """Extract relevant keywords from cultural profile"""
        preferences = set()
        
        print("🔍 DEBUG - Extracting preferences from cultural profile...")
        print(f"🔍 DEBUG - Cultural profile type: {type(cultural_profile)}")
        
        # Extract from cultural segments
        if hasattr(cultural_profile, 'cultural_segments') and cultural_profile.cultural_segments:
            segments = cultural_profile.cultural_segments
            print(f"🔍 DEBUG - Cultural segments: {segments}")
            
            for segment in segments:
                segment_lower = str(segment).lower()
                print(f"   Checking segment: '{segment_lower}'")
                
                if 'jazz' in segment_lower or 'music' in segment_lower:
                    preferences.add('jazz')
                    print("     -> Added 'jazz'")
                if 'sustain' in segment_lower or 'eco' in segment_lower:
                    preferences.add('sustainability')
                    print("     -> Added 'sustainability'")
                if 'creative' in segment_lower or 'art' in segment_lower:
                    preferences.add('creative')
                    print("     -> Added 'creative'")
                if 'luxury' in segment_lower or 'premium' in segment_lower:
                    preferences.add('luxury')
                    print("     -> Added 'luxury'")
                if 'local' in segment_lower or 'community' in segment_lower:
                    preferences.add('local')
                    print("     -> Added 'local'")
                if 'indie' in segment_lower or 'independent' in segment_lower:
                    preferences.add('creative')
                    print("     -> Added 'creative' (indie)")
        
        # Extract from cross-domain connections
        if hasattr(cultural_profile, 'cross_domain_connections') and cultural_profile.cross_domain_connections:
            connections = cultural_profile.cross_domain_connections
            print(f"🔍 DEBUG - Cross-domain connections: {connections}")
            
            # Check music preferences
            music_prefs = connections.get('music', [])
            print(f"   Music preferences: {music_prefs}")
            for music in music_prefs:
                music_str = str(music).lower()
                if 'jazz' in music_str:
                    preferences.add('jazz')
                    print("     -> Added 'jazz' from music")
                if 'soul' in music_str:
                    preferences.add('soul')
                    print("     -> Added 'soul' from music")
                if 'indie' in music_str or 'rock' in music_str:
                    preferences.add('creative')
                    print("     -> Added 'creative' from music")
            
            # Check lifestyle preferences
            lifestyle_prefs = connections.get('lifestyle', [])
            print(f"   Lifestyle preferences: {lifestyle_prefs}")
            for lifestyle in lifestyle_prefs:
                lifestyle_str = str(lifestyle).lower()
                if 'sustain' in lifestyle_str:
                    preferences.add('sustainability')
                    print("     -> Added 'sustainability' from lifestyle")
                if 'creative' in lifestyle_str:
                    preferences.add('creative')
                    print("     -> Added 'creative' from lifestyle")
                if 'local' in lifestyle_str:
                    preferences.add('local')
                    print("     -> Added 'local' from lifestyle")
        
        # CRITICAL FIX: Always ensure we have preferences
        if not preferences:
            preferences = {'jazz', 'sustainability', 'creative'}
            print("🔍 DEBUG - No preferences found, adding defaults: jazz, sustainability, creative")
        
        print(f"🔍 DEBUG - Final extracted preferences: {list(preferences)}")
        return list(preferences)

    def _get_matching_products(self, preferences, max_recommendations):
        """Get products matching user preferences"""
        matching_products = []
        
        print(f"🔍 DEBUG - Looking for products matching preferences: {preferences}")
        print(f"🔍 DEBUG - Available product categories: {list(self.products.keys())}")
        
        # Get products for each preference
        for pref in preferences:
            if pref in self.products:
                products = self.products[pref]
                matching_products.extend(products)
                print(f"✅ DEBUG - Added {len(products)} products for preference '{pref}'")
                # Show first product as example
                if products:
                    print(f"   Example: {products[0].get('name', 'Unknown')}")
            else:
                print(f"⚠️ DEBUG - No products found for preference '{pref}'")
        
        # CRITICAL FIX: Always ensure we have products
        if not matching_products:
            print("🔍 DEBUG - No matching products found, adding ALL fallback products")
            # Add ALL available products as fallback
            for category, products in self.products.items():
                matching_products.extend(products)
                print(f"✅ DEBUG - Added {len(products)} products from category '{category}'")
        
        print(f"🔍 DEBUG - Total matching products before dedup: {len(matching_products)}")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_products = []
        for product in matching_products:
            product_name = product.get('name', '')
            if product_name and product_name not in seen:
                seen.add(product_name)
                unique_products.append(product)
        
        print(f"🔍 DEBUG - Unique products after dedup: {len(unique_products)}")
        
        # Shuffle and limit results
        random.shuffle(unique_products)
        final_products = unique_products[:max_recommendations]
        
        print(f"🔍 DEBUG - Final products to return: {len(final_products)}")
        for i, product in enumerate(final_products):
            print(f"   {i+1}. {product.get('name', 'Unknown')} - {product.get('price', 'No price')}")
        
        return final_products

    def _get_matching_experiences(self, preferences, max_recommendations):
        """Get experiences matching user preferences"""
        matching_experiences = []
        
        print(f"🔍 DEBUG - Looking for experiences matching: {preferences}")
        
        for pref in preferences:
            if pref in self.experiences:
                experiences = self.experiences[pref]
                matching_experiences.extend(experiences)
                print(f"✅ DEBUG - Added {len(experiences)} experiences for '{pref}'")
            else:
                print(f"⚠️ DEBUG - No experiences found for preference '{pref}'")
        
        # Fallback for experiences
        if not matching_experiences:
            for category, experiences in self.experiences.items():
                matching_experiences.extend(experiences)
        
        random.shuffle(matching_experiences)
        return matching_experiences[:max_recommendations]

    def _get_fallback_recommendations(self, max_recommendations):
        """Original fallback recommendations"""
        fallback = []
        
        # Add some products from each category
        for category, products in self.products.items():
            if products:
                fallback.append(products[0])  # Take first product from each category
                if len(fallback) >= max_recommendations:
                    break
        
        print(f"🔍 DEBUG - Fallback recommendations: {len(fallback)}")
        return fallback[:max_recommendations]

    def _get_enhanced_fallback_recommendations(self, max_recommendations):
        """Enhanced fallback with guaranteed products"""
        print("🔍 DEBUG - Getting enhanced fallback recommendations")
        
        fallback = []
        
        # Priority order: jazz, sustainability, creative, luxury, local, soul
        priority_categories = ['jazz', 'sustainability', 'creative', 'luxury', 'local', 'soul']
        
        for category in priority_categories:
            if category in self.products and self.products[category]:
                products = self.products[category]
                # Add up to 2 products from each priority category
                for product in products[:2]:
                    if len(fallback) < max_recommendations:
                        fallback.append(product)
                        print(f"✅ DEBUG - Added fallback product: {product.get('name', 'Unknown')} from {category}")
        
        # If still not enough, add from remaining categories
        if len(fallback) < max_recommendations:
            for category, products in self.products.items():
                if category not in priority_categories and products:
                    for product in products:
                        if len(fallback) < max_recommendations:
                            fallback.append(product)
                            print(f"✅ DEBUG - Added remaining product: {product.get('name', 'Unknown')} from {category}")
        
        print(f"🔍 DEBUG - Enhanced fallback total: {len(fallback)} products")
        return fallback[:max_recommendations]

    def get_recommendation_summary(self, recommendations):
        """Generate a summary for the recommendations"""
        if not recommendations:
            return "Here are some curated recommendations for you:"
        
        categories = set(rec.get('category', 'General') for rec in recommendations)
        category_text = ', '.join(categories)
        
        summary = f"Based on your cultural DNA, here are {len(recommendations)} personalized recommendations spanning {category_text}:"
        print(f"🔍 DEBUG - Generated summary: {summary}")
        return summary
