import aiohttp
import asyncio
import json
from typing import Dict, List, Optional
from config import settings
from models.trend_models import UserPreferences, CulturalProfile

class QlooService:
    #interact with taste api of qloo
    def __init__(self):
        self.base_url=settings.qloo_base_url
        self.headers=settings.get_qloo_header()

    async def