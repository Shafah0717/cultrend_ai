from pydantic import BaseModel
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
    behavioral_indicator:Dict[str,float]
    confidence_score:float
    
class TrendPrediction(BaseModel):
    #single trend prediction
    product_category:str
    predicted_trend:str
    confidence_score:float
    timeline_days:float
    target_audience:List[str]
    cultural_reasoning:str
    market_oppurtunity:str
    created_at:datetime=datetime.now()

class TrendAnalysis(BaseModel):
   predictions:List[TrendPrediction]
   analysis_date:datetime
   timeframe:str
   total_predictions:int
   average_confidence:float
   

