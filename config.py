import os
import streamlit as st

class Settings:
    def __init__(self):
        self.qloo_api_key = None
        self.gemini_api_key = None
        self.qloo_base_url = "https://hackathon.api.qloo.com"
        
        # Debug: Check what's available
        self._debug_secrets()
        
        # Try multiple methods to get API keys
        self._load_api_keys()
        
        # Validate keys
        self._validate_keys()
    
    def _debug_secrets(self):
        """Debug function to see what secrets are available"""
        try:
            st.write("🔍 **Debug Info:**")
            st.write("Available secrets:", list(st.secrets.keys()) if hasattr(st, 'secrets') else "No secrets")
            if hasattr(st, 'secrets') and 'qloo' in st.secrets:
                st.write("Qloo section:", list(st.secrets['qloo'].keys()))
            if hasattr(st, 'secrets') and 'gemini' in st.secrets:
                st.write("Gemini section:", list(st.secrets['gemini'].keys()))
        except Exception as e:
            st.write(f"Debug error: {e}")
    
    def _load_api_keys(self):
        """Try multiple methods to load API keys"""
        # Method 1: Streamlit secrets (primary for deployment)
        try:
            if hasattr(st, 'secrets') and st.secrets:
                self.qloo_api_key = st.secrets.get("qloo", {}).get("api_key")
                self.gemini_api_key = st.secrets.get("gemini", {}).get("api_key")
                if self.qloo_api_key:
                    st.success("✅ Qloo API key loaded from Streamlit secrets")
                if self.gemini_api_key:
                    st.success("✅ Gemini API key loaded from Streamlit secrets")
        except Exception as e:
            st.warning(f"Secrets loading error: {e}")
        
        # Method 2: Environment variables (fallback)
        if not self.qloo_api_key:
            self.qloo_api_key = os.getenv("QLOO_API_KEY")
            if self.qloo_api_key:
                st.info("ℹ️ Qloo API key loaded from environment")
        
        if not self.gemini_api_key:
            self.gemini_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            if self.gemini_api_key:
                st.info("ℹ️ Gemini API key loaded from environment")
    
    def _validate_keys(self):
        """Validate that required keys are present"""
        missing_keys = []
        
        if not self.qloo_api_key:
            missing_keys.append("QLOO_API_KEY")
        
        if not self.gemini_api_key:
            missing_keys.append("GOOGLE_API_KEY/GEMINI_API_KEY")
        
        if missing_keys:
            st.error(f"🔑 Missing API keys: {', '.join(missing_keys)}")
            st.info("**To fix this:**")
            st.info("1. Go to your Streamlit app settings")
            st.info("2. Click 'Secrets' tab")
            st.info("3. Add your API keys in this format:")
            st.code("""
[qloo]
api_key = your_actual_qloo_key

[gemini]
api_key = your_actual_gemini_key
            """)
            st.stop()

# Create settings instance
settings = Settings()
