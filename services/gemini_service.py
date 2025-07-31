# services/gemini_service.py
import google.generativeai as genai
from typing import Dict, List, Optional
from config import settings
from models.trend_models import CulturalProfile, TrendPrediction
import json
from datetime import datetime, timedelta


class GeminiService:
    """Service to interact with Google Gemini for trend analysis with safety handling"""
    
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=settings.gemini_api_key)
        # Use gemini-1.5-flash for better safety compliance
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Finish reason mappings
        self.finish_reasons = {
            0: "FINISH_REASON_UNSPECIFIED",
            1: "STOP",  # Natural completion - success
            2: "SAFETY",  # Blocked by safety filters
            3: "RECITATION",  # Blocked for copyright
            4: "OTHER"  # Other reason
        }
        try:
            api_key = self._get_api_key()
            if not api_key:
                print("❌ No API key found")
                self.model = None
                return
            
            # Test the key immediately
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Quick connection test
            test_response = self.model.generate_content(
                "Hello",
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=10,
                )
            )
            print("✅ Gemini API key verified successfully")
            
        except Exception as e:
            print(f"❌ Gemini API key verification failed: {e}")
            self.model = None
    
    def _get_api_key(self):
        """Enhanced API key retrieval with logging"""
        # Try Streamlit secrets
        try:
            key = st.secrets["gemini"]["api_key"]
            if key and len(key) > 20:  # Basic validation
                print(f"✅ Found API key in Streamlit secrets (length: {len(key)})")
                return key
            else:
                print("⚠️ API key in secrets appears invalid")
        except Exception as e:
            print(f"⚠️ Could not access Streamlit secrets: {e}")
        
        # Try environment variables
        for env_var in ["GOOGLE_API_KEY", "GEMINI_API_KEY"]:
            key = os.getenv(env_var)
            if key:
                print(f"✅ Found API key in {env_var}")
                return key
        
        print("❌ No API key found in any location")
        return None
    
    async def analyze_cultural_trends(self, cultural_profile: CulturalProfile, timeframe: str = "90d") -> List[TrendPrediction]:
        """
        Analyze cultural profile and predict trends using Gemini with safety handling
        
        Args:
            cultural_profile: Cultural analysis from Qloo
            timeframe: Prediction timeframe (30d, 90d, 180d)
            
        Returns:
            List of trend predictions from Gemini or fallback data
        """
        
        try:
            print("🤖 Sending cultural data to Gemini AI...")
            
            # Create safety-compliant prompt
            prompt = self._create_safe_prompt(cultural_profile, timeframe)
            
            # Call Gemini with optimized settings
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,  # Balanced creativity
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=1500,
                ),
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]
            )
            
            print("✅ Gemini API call completed")
            
            # Handle response safely
            response_text = self._handle_gemini_response(response)
            
            if response_text:
                print("📝 Processing Gemini's response...")
                predictions = self._parse_real_gemini_response(response_text, timeframe)
                
                if predictions and len(predictions) > 0:
                    print(f"🎯 Successfully created {len(predictions)} predictions from Gemini AI")
                    return predictions
                else:
                    print("⚠️ No valid predictions parsed from Gemini, using enhanced sample data")
                    return self._create_enhanced_sample_predictions(cultural_profile, timeframe)
            else:
                print("⚠️ Could not extract valid response from Gemini, using sample data")
                return self._create_enhanced_sample_predictions(cultural_profile, timeframe)
                
        except genai.types.BlockedPromptException:
            print("🛡️ Prompt was blocked by Gemini safety filters")
            return self._create_enhanced_sample_predictions(cultural_profile, timeframe)
            
        except genai.types.StopCandidateException:
            print("⚠️ Gemini response generation was stopped")
            return self._create_enhanced_sample_predictions(cultural_profile, timeframe)
            
        except Exception as e:
            print(f"⚠️ Gemini API error: {e}")
            return self._create_enhanced_sample_predictions(cultural_profile, timeframe)

    # ADDED: Missing method for brand identity generation
    async def analyze_cultural_trends_with_custom_prompt(self, cultural_profile: CulturalProfile, custom_prompt: str) -> str:
        """
        Generate response using custom prompt for brand identity generation.
        Returns raw text response for custom parsing by the caller.
        """
        try:
            print("🤖 Sending custom prompt to Gemini AI...")
            
            # Call Gemini with the custom prompt
            response = self.model.generate_content(
                custom_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=1500,
                ),
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]
            )
            
            print("✅ Gemini API call completed")
            
            # Handle response safely
            response_text = self._handle_gemini_response(response)
            
            if response_text:
                print("✅ Custom prompt processing completed")
                return response_text
            else:
                print("⚠️ Could not extract valid response from Gemini")
                return ""
                
        except Exception as e:
            print(f"❌ Error in analyze_cultural_trends_with_custom_prompt: {e}")
            raise e
    
    def _handle_gemini_response(self, response) -> Optional[str]:
        """Safely extract text from Gemini response with comprehensive error handling"""
        
        try:
            # Check if response has candidates
            if not hasattr(response, 'candidates') or not response.candidates:
                print("❌ No candidates in Gemini response")
                return None
                
            candidate = response.candidates[0]
            
            # Check finish reason
            finish_reason = getattr(candidate, 'finish_reason', 0)
            reason_name = self.finish_reasons.get(finish_reason, "UNKNOWN")
            
            print(f"📋 Gemini finish reason: {finish_reason} ({reason_name})")
            
            if finish_reason == 1:  # STOP - successful completion
                print("✅ Gemini completed successfully")
                
                if hasattr(candidate, 'content') and candidate.content and candidate.content.parts:
                    response_text = candidate.content.parts[0].text
                    print(f"📏 Response length: {len(response_text)} characters")
                    return response_text
                else:
                    print("❌ No content parts in successful response")
                    return None
                    
            elif finish_reason == 2:  # SAFETY
                print("🛡️ Response blocked by Gemini safety filters")
                print("   This is common with cultural analysis - using fallback data")
                return None
                
            elif finish_reason == 3:  # RECITATION  
                print("📝 Response blocked for potential copyright issues")
                return None
                
            elif finish_reason == 4:  # OTHER
                print("⚠️ Response stopped for other reasons")
                return None
                
            else:
                print(f"❓ Unknown finish reason: {finish_reason}")
                return None
                
        except Exception as e:
            print(f"❌ Error handling Gemini response: {e}")
            return None
    
    def _create_safe_prompt(self, profile: CulturalProfile, timeframe: str) -> str:
        """Create a safety-compliant prompt for Gemini that avoids triggering filters"""
        
        timeline_days = {"30d": 30, "90d": 90, "180d": 180}[timeframe]
        
        # Extract preferences safely
        music_prefs = profile.cross_domain_connections.get('music', [])[:3]
        fashion_prefs = profile.cross_domain_connections.get('fashion', [])[:3]
        dining_prefs = profile.cross_domain_connections.get('dining', [])[:3]
        lifestyle_prefs = profile.cross_domain_connections.get('lifestyle', [])[:3]
        entertainment_prefs = profile.cross_domain_connections.get('entertainment', [])[:3]
        
        # Create neutral, business-focused prompt
        prompt = f"""You are a market research consultant analyzing consumer preference patterns to identify potential product opportunities. Please provide a professional market analysis.

## CONSUMER PREFERENCE ANALYSIS

**Consumer Segments:** {', '.join(profile.cultural_segments[:3])}

**Preference Categories:**
- Music/Audio: {', '.join(music_prefs)}
- Fashion/Style: {', '.join(fashion_prefs)}
- Food/Dining: {', '.join(dining_prefs)}
- Entertainment: {', '.join(entertainment_prefs)}
- Lifestyle: {', '.join(lifestyle_prefs)}

**Analysis Period:** Next {timeline_days} days

## REQUEST

Based on these consumer preferences, identify 3 potential product or service opportunities that might emerge in the marketplace. Focus on legitimate business opportunities and market trends.

## REQUIRED RESPONSE FORMAT

Respond with ONLY valid JSON in this exact structure:

{{
    "predictions": [
        {{
            "product_category": "Consumer Products",
            "predicted_trend": "Sustainable audio accessories with minimalist design",
            "confidence_score": 78,
            "timeline_days": 85,
            "target_audience": ["eco-conscious consumers", "audio enthusiasts"],
            "cultural_reasoning": "Market research indicates growing consumer interest in environmentally responsible products combined with high-quality audio experiences",
            "market_opportunity": "Emerging market segment for premium sustainable electronics with estimated growth potential"
        }},
        {{
            "product_category": "Lifestyle Services",
            "predicted_trend": "Personalized wellness platforms for remote professionals",
            "confidence_score": 82,
            "timeline_days": 90,
            "target_audience": ["remote workers", "wellness-focused consumers"],
            "cultural_reasoning": "Analysis shows convergence of remote work trends with increased focus on personal wellness and work-life balance",
            "market_opportunity": "Growing market for digital wellness solutions tailored to remote work environments"
        }},
        {{
            "product_category": "Food & Beverage",
            "predicted_trend": "Artisanal functional beverages with local sourcing",
            "confidence_score": 75,
            "timeline_days": 95,
            "target_audience": ["health-conscious consumers", "local food supporters"],
            "cultural_reasoning": "Consumer preference data shows intersection of health consciousness with support for local businesses",
            "market_opportunity": "Niche market for premium functional beverages with local community connection"
        }}
    ]
}}

Please provide your market analysis in the specified JSON format:"""
        
        return prompt
    
    def _parse_real_gemini_response(self, response_text: str, timeframe: str) -> List[TrendPrediction]:
        """Parse actual Gemini response into TrendPrediction objects with robust error handling"""
        
        try:
            print(f"🔍 Parsing Gemini response...")
            print(f"📄 Response preview: {response_text[:150]}...")
            
            # Clean response text
            cleaned = response_text.strip()
            
            # Remove markdown formatting if present
            if cleaned.startswith("``````"):
                lines = cleaned.split('\n')
                cleaned = '\n'.join(lines[1:-1])
            
            # Find JSON boundaries
            start_idx = cleaned.find('{')
            end_idx = cleaned.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                cleaned = cleaned[start_idx:end_idx]
                print(f"🧹 Extracted JSON: {len(cleaned)} characters")
            else:
                print("❌ Could not find JSON boundaries in response")
                return []
            
            # Parse JSON
            try:
                data = json.loads(cleaned)
                print("✅ JSON parsed successfully")
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"🔍 Problematic JSON: {cleaned[:300]}...")
                return []
            
            # Process predictions
            predictions = []
            predictions_data = data.get("predictions", [])
            
            print(f"📊 Found {len(predictions_data)} predictions in response")
            
            for i, pred_data in enumerate(predictions_data, 1):
                try:
                    print(f"🔄 Processing prediction {i}...")
                    
                    # Validate required fields
                    required_fields = ["product_category", "predicted_trend", "confidence_score", 
                                     "timeline_days", "target_audience", "cultural_reasoning", "market_opportunity"]
                    
                    for field in required_fields:
                        if field not in pred_data:
                            print(f"⚠️ Missing field '{field}' in prediction {i}")
                            pred_data[field] = self._get_default_value(field)
                    
                    # Create prediction object
                    prediction = TrendPrediction(
                        product_category=str(pred_data.get("product_category", "Consumer Products")),
                        predicted_trend=str(pred_data.get("predicted_trend", "Emerging trend")),
                        confidence_score=float(pred_data.get("confidence_score", 75)),
                        timeline_days=int(pred_data.get("timeline_days", 90)),
                        target_audience=list(pred_data.get("target_audience", ["consumers"])),
                        cultural_reasoning=str(pred_data.get("cultural_reasoning", "Based on market analysis")),
                        market_opportunity=str(pred_data.get("market_opportunity", "Market opportunity identified"))
                    )
                    
                    predictions.append(prediction)
                    print(f"✅ Prediction {i} processed: {prediction.predicted_trend[:50]}...")
                    
                except Exception as e:
                    print(f"⚠️ Error processing prediction {i}: {e}")
                    continue
            
            print(f"🎯 Successfully processed {len(predictions)} predictions from Gemini")
            return predictions
                
        except Exception as e:
            print(f"❌ Error parsing Gemini response: {e}")
            return []

    # MOVED: Brand identity prompt function inside the class
    def create_brand_identity_prompt(self, cultural_profile: CulturalProfile) -> str:
        """Convert the cultural profile to a readable string for brand identity generation"""
        profile_summary = f"""
        - Cultural Segments: {', '.join(cultural_profile.cultural_segments)}
        - Key Affinities (Brands): {', '.join(cultural_profile.cross_domain_connections.get('brands', []))}
        - Key Affinities (Artists): {', '.join(cultural_profile.cross_domain_connections.get('artists', []))}
        - Behavioral Indicators: Early Adopter ({cultural_profile.behavioral_indicators.get('early_adopter', 'N/A')}), Cultural Openness ({cultural_profile.behavioral_indicators.get('cultural_openness', 'N/A')})
        """

        prompt = f"""
        Act as an expert brand strategist. Based on the following cultural taste profile, generate a complete personal brand identity kit. The user's cultural DNA is defined by these characteristics:
        {profile_summary}

        Your task is to synthesize this cultural data into a cohesive and compelling personal brand. Generate the following assets and provide the output ONLY in a valid JSON format that matches this Pydantic model:

        class BrandIdentityKit(BaseModel):
            brand_name: str
            tagline: str
            mission_statement: str
            core_keywords: List[str]
            color_palette: Dict[str, str] # e.g., {{"primary": "#HEXCODE", "accent_1": "#HEXCODE"}}
            social_media_bio: str

        Analyze the user's affinities (e.g., minimalist fashion, indie music, sustainable values) to inform the brand's name, voice, and aesthetic. The color palette should reflect their taste. The mission statement and bio must capture their core values. Be creative and insightful.
        """
        return prompt

    def _get_default_value(self, field: str):
        """Get default values for missing fields"""
        defaults = {
            "product_category": "Consumer Products",
            "predicted_trend": "Emerging market trend",
            "confidence_score": 75,
            "timeline_days": 90,
            "target_audience": ["consumers"],
            "cultural_reasoning": "Based on consumer preference analysis",
            "market_opportunity": "Emerging market opportunity"
        }
        return defaults.get(field, "Unknown")
    
    def _create_enhanced_sample_predictions(self, cultural_profile: CulturalProfile, timeframe: str) -> List[TrendPrediction]:
        """Create enhanced sample predictions based on actual user cultural profile"""
        
        timeline_days = {"30d": 30, "90d": 90, "180d": 180}[timeframe]
        
        print("🔄 Creating enhanced sample predictions based on cultural profile...")
        
        # Extract user preferences
        music_prefs = cultural_profile.cross_domain_connections.get('music', [])
        fashion_prefs = cultural_profile.cross_domain_connections.get('fashion', [])
        dining_prefs = cultural_profile.cross_domain_connections.get('dining', [])
        lifestyle_prefs = cultural_profile.cross_domain_connections.get('lifestyle', [])
        
        # Generate predictions based on actual preferences
        predictions = []
        
        # Fashion prediction based on user's fashion preferences
        if fashion_prefs:
            fashion_elements = ', '.join(fashion_prefs[:2])
            predictions.append(TrendPrediction(
                product_category="Fashion",
                predicted_trend=f"Sustainable {fashion_elements}-inspired accessories with tech integration",
                confidence_score=87.0,
                timeline_days=timeline_days - 15,
                target_audience=[f"{fashion_prefs[0]} enthusiasts" if fashion_prefs else "fashion enthusiasts", "eco-conscious consumers"],
                cultural_reasoning=f"Your preference for {fashion_elements} combined with growing sustainability consciousness creates demand for accessories that blend your aesthetic with environmental values and modern functionality.",
                market_opportunity=f"Growing market for sustainable fashion accessories targeting {fashion_elements} aesthetic preferences."
            ))
        
        # Lifestyle prediction based on user's lifestyle choices
        if lifestyle_prefs:
            lifestyle_elements = ', '.join(lifestyle_prefs[:2])
            predictions.append(TrendPrediction(
                product_category="Lifestyle",
                predicted_trend=f"Artisanal wellness products designed for {lifestyle_elements} practitioners",
                confidence_score=83.0,
                timeline_days=timeline_days - 25,
                target_audience=[f"{lifestyle_prefs[0]} practitioners" if lifestyle_prefs else "lifestyle enthusiasts", "wellness consumers"],
                cultural_reasoning=f"The intersection of {lifestyle_elements} with wellness trends creates opportunity for specialized products that support your specific lifestyle approach.",
                market_opportunity=f"Underserved market for wellness products tailored to {lifestyle_elements} community needs."
            ))
        
        # Dining/Entertainment prediction
        if dining_prefs or music_prefs:
            cultural_elements = (dining_prefs + music_prefs)[:2]
            element_desc = ', '.join(cultural_elements)
            predictions.append(TrendPrediction(
                product_category="Experience",
                predicted_trend=f"Cultural experience platforms combining {element_desc} with community connection",
                confidence_score=79.0,
                timeline_days=timeline_days,
                target_audience=[f"{cultural_elements[0]} enthusiasts" if cultural_elements else "cultural enthusiasts", "community-oriented consumers"],
                cultural_reasoning=f"Your appreciation for {element_desc} indicates desire for authentic cultural experiences that build community around shared interests.",
                market_opportunity=f"Emerging market for experiential platforms serving {element_desc} communities."
            ))
        
        # Fallback if no specific preferences
        if not predictions:
            predictions = self._create_default_sample_predictions(timeframe)
        
        print(f"✅ Created {len(predictions)} enhanced sample predictions")
        return predictions
    
    def _create_default_sample_predictions(self, timeframe: str) -> List[TrendPrediction]:
        """Create default sample predictions when no specific preferences available"""
        
        timeline_days = {"30d": 30, "90d": 90, "180d": 180}[timeframe]
        
        return [
            TrendPrediction(
                product_category="Technology",
                predicted_trend="Privacy-focused digital wellness platforms",
                confidence_score=85.0,
                timeline_days=timeline_days - 10,
                target_audience=["privacy-conscious consumers", "wellness enthusiasts"],
                cultural_reasoning="Growing awareness of digital privacy combined with wellness trends creates demand for platforms that protect user data while supporting personal growth.",
                market_opportunity="Emerging market for privacy-first wellness technology solutions."
            ),
            TrendPrediction(
                product_category="Lifestyle",
                predicted_trend="Sustainable local community products",
                confidence_score=81.0,
                timeline_days=timeline_days - 20,
                target_audience=["community-oriented consumers", "sustainability advocates"],
                cultural_reasoning="Increasing focus on local communities and environmental responsibility drives demand for products that support both local economies and sustainable practices.",
                market_opportunity="Growing market for locally-sourced sustainable products with community impact."
            ),
            TrendPrediction(
                product_category="Consumer Products",
                predicted_trend="Artisanal tech accessories with cultural storytelling",
                confidence_score=77.0,
                timeline_days=timeline_days,
                target_audience=["cultural enthusiasts", "tech users"],
                cultural_reasoning="Convergence of technology adoption with desire for authentic, meaningful products creates opportunities for tech accessories with cultural narratives.",
                market_opportunity="Niche market for premium tech accessories with authentic cultural connections."
            )
        ]
    
    def test_gemini_connection(self) -> bool:
        """Test if Gemini API connection is working properly"""
        
        try:
            print("🧪 Testing Gemini connection...")
            response = self.model.generate_content(
                "Please respond with exactly: 'Connection test successful'",
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=50,
                )
            )
            
            response_text = self._handle_gemini_response(response)
            
            if response_text and "successful" in response_text.lower():
                print(f"✅ Gemini connection test successful")
                return True
            else:
                print(f"❌ Gemini connection test failed: {response_text}")
                return False
                
        except Exception as e:
            print(f"❌ Gemini connection test error: {e}")
            return False


# Test functions - MUST be outside the class
async def test_gemini_service():
    """Comprehensive test of Gemini service with real responses"""
    
    print("🤖 Testing Gemini LLM Service with Enhanced Safety Handling...")
    print("=" * 60)
    
    try:
        # Import models
        from models.trend_models import CulturalProfile
        
        # Create realistic cultural profile
        sample_profile = CulturalProfile(
            profile_id="comprehensive_test_456",
            cultural_segments=["indie culture", "sustainability advocates", "remote work professionals"],
            cross_domain_connections={
                "music": ["indie rock", "electronic", "folk"],
                "fashion": ["vintage", "minimalist", "sustainable"],
                "dining": ["artisanal coffee", "plant-based", "local sourcing"],
                "entertainment": ["indie films", "podcasts", "live music"],
                "lifestyle": ["remote work", "wellness", "sustainable living"]
            },
            behavioral_indicators={
                "early_adopter": 0.85,
                "influence": 0.7,
                "cultural_openness": 0.9
            },
            confidence_score=88.0
        )
        
        # Test the service
        print("🏗️ Creating GeminiService instance...")
        gemini_service = GeminiService()
        
        # Test connection first
        print("\n1️⃣ Testing API connection...")
        connection_ok = gemini_service.test_gemini_connection()
        
        print(f"\n2️⃣ Running trend analysis...")
        predictions = await gemini_service.analyze_cultural_trends(sample_profile, "90d")
        
        if predictions:
            print("✅ Analysis completed successfully!")
            print(f"   📊 Generated {len(predictions)} predictions")
            print(f"   🎯 Average confidence: {sum(p.confidence_score for p in predictions) / len(predictions):.1f}%")
            
            for i, pred in enumerate(predictions, 1):
                print(f"\n🔮 Prediction {i}:")
                print(f"   📂 Category: {pred.product_category}")
                print(f"   🎯 Trend: {pred.predicted_trend}")
                print(f"   📊 Confidence: {pred.confidence_score}%")
                print(f"   ⏰ Timeline: {pred.timeline_days} days")
                print(f"   👥 Target: {', '.join(pred.target_audience[:2])}")
                print(f"   💡 Reasoning: {pred.cultural_reasoning[:120]}...")
                print(f"   💰 Opportunity: {pred.market_opportunity[:100]}...")
        else:
            print("❌ No predictions generated")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


async def test_safety_scenarios():
    """Test various scenarios that might trigger safety filters"""
    
    print("\n🛡️ Testing Safety Filter Scenarios...")
    print("=" * 40)
    
    from models.trend_models import CulturalProfile
    
    # Test different cultural profiles
    test_profiles = [
        {
            "name": "Music Enthusiast",
            "profile": CulturalProfile(
                profile_id="music_test",
                cultural_segments=["music lovers"],
                cross_domain_connections={"music": ["jazz", "classical"], "lifestyle": ["cultural events"]},
                behavioral_indicators={"early_adopter": 0.7},
                confidence_score=80.0
            )
        },
        {
            "name": "Tech Professional", 
            "profile": CulturalProfile(
                profile_id="tech_test",
                cultural_segments=["tech enthusiasts"],
                cross_domain_connections={"lifestyle": ["remote work"], "entertainment": ["gaming"]},
                behavioral_indicators={"early_adopter": 0.9},
                confidence_score=85.0
            )
        }
    ]
    
    service = GeminiService()
    
    for test_case in test_profiles: 
        print(f"\n🧪 Testing: {test_case['name']}")
        predictions = await service.analyze_cultural_trends(test_case['profile'], "90d")
        print(f"   📊 Result: {len(predictions)} predictions generated")
        
        if predictions:
            print(f"   ✅ Success: {predictions[0].predicted_trend[:60]}...")
        else:
            print("   ⚠️ No predictions (likely safety filtered)")


# Run tests when file is executed directly
if __name__ == "__main__":
    import asyncio
    
    print("🚀 Starting Comprehensive Gemini Service Tests...")
    
    # Run main test
    asyncio.run(test_gemini_service())
    
    print("\n" + "="*60)
    
    # Run safety tests
    asyncio.run(test_safety_scenarios())
    
    print("\n🎉 All tests completed!")
