import aiohttp
import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime
from config import settings
from models.trend_models import UserPreferences, CulturalProfile
# services/qloo_parameter_testing.py
class QlooParameterTesting:
    """Test different parameter combinations for optimal results"""
    
    async def test_parameter_combinations(self) -> Dict[str, any]:
        """Test various parameter combinations to find optimal approaches"""
        
        # Define test combinations based on the documentation
        test_combinations = [
            {
                "name": "Tags + Demographics",
                "params": {
                    "filter.type": "urn:entity:brand",
                    "signal.interests.tags": "urn:tag:keyword:lifestyle:sustainable",
                    "signal.demographics.age": "25-35",
                    "take": 10
                }
            },
            {
                "name": "Entities + Tags",
                "params": {
                    "filter.type": "urn:entity:brand",
                    "signal.interests.entities": "discovered_entity_ids",  # Will be replaced
                    "filter.tags": "urn:tag:genre:music:indie",
                    "take": 10
                }
            },
            {
                "name": "Multiple Signals",
                "params": {
                    "filter.type": "urn:entity:brand",
                    "signal.interests.tags": "urn:tag:keyword:lifestyle:wellness",
                    "signal.demographics.audiences": "millennials",
                    "filter.popularity.min": 0.3,
                    "take": 10
                }
            },
            {
                "name": "Location + Interests",
                "params": {
                    "filter.type": "urn:entity:place",
                    "signal.interests.tags": "urn:tag:keyword:food:artisanal",
                    "filter.location.query": "New York",
                    "take": 8
                }
            }
        ]
        
        results = {}
        
        for combination in test_combinations:
            print(f"\n🧪 Testing combination: {combination['name']}")
            
            # For entity-based tests, discover real entity IDs first
            if "discovered_entity_ids" in str(combination["params"]):
                entities = await self._get_sample_entities()
                if entities:
                    entity_ids = [e["id"] for e in entities[:3]]
                    combination["params"]["signal.interests.entities"] = ",".join(entity_ids)
                else:
                    print(f"   ⚠️ Skipping {combination['name']} - no entities found")
                    continue
            
            # Test the combination
            response_data = await self._test_combination(combination["params"])
            
            results[combination["name"]] = {
                "parameters": combination["params"],
                "entities_returned": len(response_data.get("results", {}).get("entities", [])),
                "success": response_data.get("results", {}).get("entities", []) != [],
                "sample_entity": response_data.get("results", {}).get("entities", [{}])[0].get("name", "None") if response_data.get("results", {}).get("entities") else "None"
            }
            
            print(f"   📊 Results: {results[combination['name']]['entities_returned']} entities")
            print(f"   ✅ Success: {results[combination['name']]['success']}")
        
        return results
    
    async def _test_combination(self, params: Dict) -> Dict:
        """Test a specific parameter combination"""
        
        try:
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
                        print(f"   ❌ API error: {response.status}")
                        return {}
                        
        except Exception as e:
            print(f"   ❌ Request error: {e}")
            return {}
