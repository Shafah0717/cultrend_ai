import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


class Settings:

    def __init__(self):
        try:
            self.qloo_api_key = st.secrets["qloo"]["api_key"]
            self.gemini_api_key = st.secrets["gemini"]["api_key"]
        except (KeyError, FileNotFoundError, AttributeError):
            # Fall back to environment variables (for local development)
            self.qloo_api_key = os.getenv("QLOO_API_KEY")
            self.gemini_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        # Graceful error handling for missing keys

        
        self.qloo_base_url="https://hackathon.api.qloo.com"
        
        if not self.qloo_api_key:
            print("Warning: Qloo API key not found")
            # Don't raise error immediately - let the app handle it
        
        if not self.gemini_api_key:
            print("Warning: Gemini API key not found")

        #api endpoint


        # if not self.qloo_api_key:
        #     raise ValueError("Qloo env required")
        # if not self.google_api_key:
        #     raise ValueError("gemini env required")
        
    def get_qloo_headers(self):
         """Get headers for Qloo API requests"""
         return {
             "X-Api-Key": self.qloo_api_key,
             "Content-Type":"application/json"
             
         }
settings = Settings()