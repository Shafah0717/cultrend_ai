from pydantic import BaseModel,Field
from typing import List, Dict, Optional
from datetime import datetime

class UserPreferences(BaseModel):
    #users cultural preference input

    music_genres:List[str]=[]
    dining_preferences:List[str]=[]
    fashion_styles:List[str]=[]
    entertainment_types:List[str]=[]
    lifestyle_choices:List[str]=[]

class CulturalProfile(BaseModel):
    #qloo cultural analysis of user preference

    profile_id:str
    cultural_segments:List[str]
    cross_domain_connections:Dict[str,List[str]]
    behavioral_indicators:Dict[str,float]
    confidence_score:float
    
class TrendPrediction(BaseModel):
    #single trend prediction
    product_category:str
    predicted_trend:str
    confidence_score:float
    timeline_days:float
    target_audience:List[str]
    cultural_reasoning:str
    market_opportunity:str
    created_at:datetime=datetime.now()

class TrendAnalysis(BaseModel):
    predictions: List[TrendPrediction]
    cultural_profile: Optional[CulturalProfile] = None  
    analysis_date: datetime
    timeframe: str
    total_predictions: int
    average_confidence: float

class BrandIdentityKit(BaseModel):
    brand_name: str = Field(..., description="A catchy, memorable name for the personal brand.")
    tagline: str = Field(..., description="A short, impactful slogan that captures the brand's essence.")
    mission_statement: str = Field(..., description="A brief paragraph explaining the brand's purpose and values.")
    core_keywords: List[str] = Field(..., description="5-7 keywords that define the brand's identity.")
    color_palette: Dict[str, str] = Field(..., description="A dictionary of 4-5 brand colors with hex codes and names (e.g., {'primary': '#3A5FCD', 'accent': '#FDB813'}).")
    social_media_bio: str = Field(..., description="A concise, engaging bio suitable for platforms like Instagram or X.")

