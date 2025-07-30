import os
import streamlit as st

class Settings:
    def __init__(self):
        self.qloo_base_url = "https://hackathon.api.qloo.com"
        
        # Only get keys, don't validate by calling APIs
        self.qloo_api_key = (
            st.secrets.get("qloo", {}).get("api_key") or 
            os.getenv("QLOO_API_KEY")
        )
        self.gemini_api_key = (
            st.secrets.get("gemini", {}).get("api_key") or 
            os.getenv("GOOGLE_API_KEY") or 
            os.getenv("GEMINI_API_KEY")
        )
        
        # Simple validation without API calls
        if not self.qloo_api_key or not self.gemini_api_key:
            st.error("🔑 API keys required")
            st.stop()

# Cache the settings instance
@st.cache_resource
def get_settings():
    return Settings()

settings = get_settings()
