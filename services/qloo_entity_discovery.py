import aiohttp
import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime
from config import settings
from models.trend_models import UserPreferences, CulturalProfile
# services/qloo_entity_discovery.py
class QlooEntityDiscovery:
    """Test entity ID discovery workflow"""
    
    async def test_entity_discovery_workflow(self) -> Dict[str, any]:
        """Test the complete entity discovery workflow"""
        
        test_preferences = [
            "sustainable fashion",
            "indie music",
            "artisanal coffee",
            "wellness products",
            "minimalist design"
        ]
        
        results = {}
        
        for preference in test_preferences:
            print(f"\n🔍 Testing preference: '{preference}'")
            
            # Step 1: Search for entities
            entities = await self._search_entities(preference)
            print(f"   Found {len(entities)} entities via search")
            
            # Step 2: Use entity IDs in insights
            if entities:
                insights = await self._test_entity_insights(entities[:3])
                results[preference] = {
                    "entities_found": len(entities),
                    "sample_entities": entities[:3],
                    "insights_returned": len(insights.get("results", {}).get("entities", [])),
                    "workflow_success": len(insights.get("results", {}).get("entities", [])) > 0
                }
                print(f"   ✅ Workflow success: {results[preference]['workflow_success']}")
            else:
                results[preference] = {
                    "entities_found": 0,
                    "workflow_success": False
                }
                print(f"   ❌ No entities found for '{preference}'")
        
        return results
    
    async def _search_entities(self, query: str) -> List[Dict]:
        """Search for entities using the /search endpoint"""
        
        try:
            params = {
                "query": query,
                "types": "brand,artist,place",  # Test multiple types
                "limit": 5
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/search",
                    params=params,
                    headers=self.headers,
                    timeout=10
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        entities = []
                        
                        # Extract entity information
                        for result in data.get("results", []):
                            entities.append({
                                "id": result.get("id", ""),
                                "name": result.get("name", ""),
                                "type": result.get("type", "")
                            })
                        
                        return entities
                    else:
                        print(f"   Search failed with status {response.status}")
                        return []
                        
        except Exception as e:
            print(f"   Search error: {e}")
            return []
    
    async def _test_entity_insights(self, entities: List[Dict]) -> Dict:
        """Test using discovered entity IDs in insights API"""
        
        try:
            entity_ids = [entity["id"] for entity in entities if entity["id"]]
            
            params = {
                "filter.type": "urn:entity:brand",
                "signal.interests.entities": ",".join(entity_ids),
                "take": 8
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/v2/insights",
                    params=params,
                    headers=self.headers,
                    timeout=15
                ) as response:
                    
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {}
                        
        except Exception as e:
            print(f"   Insights error: {e}")
            return {}
