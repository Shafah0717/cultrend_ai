# services/explanation_service.py

class ExplanationService:
    def get_recommendation_explanation(self, recommendation, cultural_profile, brand_kit):
        """Generate explanation for why this product was recommended"""
        try:
            # Extract product name and keywords
            product_name = recommendation.get('name', 'this product')
            keywords = recommendation.get('keywords', [])
            
            # Generate explanations based on keywords and profile
            explanations = {
                "main": f"{product_name} aligns with your cultural preferences",
                "cultural": "Matches your cultural segments and lifestyle choices",
                "brand": f"Fits perfectly with your {getattr(brand_kit, 'brand_name', 'Cultural Navigator')} brand identity"
            }
            
            # Customize based on keywords
            if 'jazz' in keywords:
                explanations["main"] = f"Perfect for your jazz music appreciation and cultural exploration"
            elif 'sustainability' in keywords:
                explanations["main"] = f"Aligns with your sustainable and eco-conscious values"
            elif 'creative' in keywords:
                explanations["main"] = f"Supports your creative expression and artistic interests"
            elif 'luxury' in keywords:
                explanations["main"] = f"Matches your appreciation for premium, high-quality items"
            
            return explanations
            
        except Exception as e:
            print(f"ERROR in get_recommendation_explanation: {e}")
            return {"main": "Recommended based on your preferences"}
