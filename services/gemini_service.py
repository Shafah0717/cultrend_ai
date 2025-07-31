# services/gemini_service.py
import google.generativeai as genai
import streamlit as st
import os
from typing import Dict, List, Optional
from config import settings
from models.trend_models import CulturalProfile, TrendPrediction
import json
from datetime import datetime, timedelta

class GeminiService:
    """Service to interact with Google Gemini for trend analysis with safety handling"""
    
    def __init__(self):
        try:
            # Initialize finish reasons mapping
            self.finish_reasons = {
                0: "FINISH_REASON_UNSPECIFIED",
                1: "STOP",  # Natural completion - success
                2: "SAFETY",  # Blocked by safety filters
                3: "RECITATION",  # Blocked for copyright
                4: "OTHER"  # Other reason
            }
            
            api_key = self._get_api_key()
            if not api_key:
                print("❌ No API key found")
                self.model = None
                return
            
            # Configure and test the API key
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
        # Try Streamlit secrets first
        try:
            key = st.secrets["gemini"]["api_key"]
            if key and len(key) > 20:  # Basic validation
                print(f"✅ Found API key in Streamlit secrets (length: {len(key)})")
                return key
            else:
                print("⚠️ API key in secrets appears invalid")
        except Exception as e:
            print(f"⚠️ Could not access Streamlit secrets: {e}")
        
        # Try environment variables as fallback
        for env_var in ["GOOGLE_API_KEY", "GEMINI_API_KEY"]:
            key = os.getenv(env_var)
            if key:
                print(f"✅ Found API key in {env_var}")
                return key
        
        print("❌ No API key found in any location")
        return None
    
    async def analyze_cultural_trends(self, cultural_profile: CulturalProfile, timeframe: str = "90d") -> List[TrendPrediction]:
        """Analyze cultural profile and predict trends using Gemini with safety handling"""
        
        # Check if model is available
        if not self.model:
            print("🛡️ No valid Gemini model - using enhanced fallback")
            return self._create_enhanced_sample_predictions(cultural_profile, timeframe)
        
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

    async def analyze_cultural_trends_with_custom_prompt(self, cultural_profile: CulturalProfile, custom_prompt: str) -> str:
        """Generate response using custom prompt for brand identity generation"""
        
        # Check if model is available
        if not self.model:
            print("🛡️ No valid Gemini model - cannot generate custom response")
            return ""
        
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
            return ""
    
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
    
    # Add all your other existing methods here...
    def _create_safe_prompt(self, profile: CulturalProfile, timeframe: str) -> str:
        # Your existing implementation
        pass
    
    def _parse_real_gemini_response(self, response_text: str, timeframe: str) -> List[TrendPrediction]:
        # Your existing implementation
        pass
    
    def create_brand_identity_prompt(self, cultural_profile: CulturalProfile) -> str:
        # Your existing implementation
        pass
    
    def _get_default_value(self, field: str):
        # Your existing implementation
        pass
    
    def _create_enhanced_sample_predictions(self, cultural_profile: CulturalProfile, timeframe: str) -> List[TrendPrediction]:
        # Your existing implementation
        pass
    
    def _create_default_sample_predictions(self, timeframe: str) -> List[TrendPrediction]:
        # Your existing implementation
        pass
    
    def test_gemini_connection(self) -> bool:
        # Your existing implementation
        pass
