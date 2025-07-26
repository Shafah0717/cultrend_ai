import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    def __init__(self):
        self.qloo_api_key=os.getenv("QLOO_API_KEY")
        self.google_api_key=os.getenv("GOOGLE_API_KEY")
        self.debug=os.getenv("DEBUG","FALSE").lower()=="true"

        #api endpoint

        self.qloo_base_url="https://hackathon.api.qloo.com"

        if not self.qloo_api_key:
            raise ValueError("Qloo env required")
        if not self.google_api_key:
            raise ValueError("gemini env required")
        
    def get_qloo_headers(self):
         """Get headers for Qloo API requests"""
         return {
             "X-Api-Key": self.qloo_api_key,
             "Content-Type":"application/json"
             
         }
settings = Settings()