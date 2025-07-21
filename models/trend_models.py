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