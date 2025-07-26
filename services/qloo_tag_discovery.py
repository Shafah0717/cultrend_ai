# services/qloo_tag_discovery.py
import aiohttp
import asyncio
import json
from typing import Dict, List, Set
from config import settings

class QlooTagDiscovery:
    """Systematic discovery of available Qloo tag URNs"""
    
    def __init__(self):
        self.base_url = "https://hackathon.api.qloo.com"
        self.headers = {
            "X-Api-Key": settings.qloo_api_key,
            "Content-Type": "application/json"
        }
        self.discovered_tags = {}
    
    async def discover_tag_categories(self) -> Dict[str, List[str]]:
        """Systematically discover available tag categories"""
        
        # Test different tag namespace patterns
        tag_patterns = [
            "urn:tag:keyword:lifestyle",
            "urn:tag:keyword:fashion", 
            "urn:tag:keyword:food",
            "urn:tag:keyword:media",
            "urn:tag:genre:music",
            "urn:tag:genre:restaurant",
            "urn:tag:attribute:style",
            "urn:tag:interest:culture"
        ]
        
        discovered_tags = {}
        
        for pattern in tag_patterns:
            print(f"🔍 Testing tag pattern: {pattern}")
            tags = await self._test_tag_pattern(pattern)
            if tags:
                discovered_tags[pattern] = tags
                print(f"✅ Found {len(tags)} tags for {pattern}")
            else:
                print(f"❌ No tags found for {pattern}")
        
        return discovered_tags
    
    async def _test_tag_pattern(self, tag_pattern: str) -> List[str]:
        """Test if a tag pattern returns valid results"""
        
        try:
            # Method 1: Try using filter.tag.types (from your documentation)
            params = {
                "filter.type": "urn:tag",
                "filter.tag.types": tag_pattern,
                "take": 20
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/v2/insights",
                    params=params,
                    headers=self.headers,
                    timeout=10
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return self._extract_tag_urns(data)
                    else:
                        print(f"   Status {response.status} for pattern {tag_pattern}")
                        return []
                        
        except Exception as e:
            print(f"   Error testing {tag_pattern}: {e}")
            return []
    
    def _extract_tag_urns(self, response_data: Dict) -> List[str]:
        """Extract tag URNs from API response"""
        
        tag_urns = []
        
        # Try different response structures
        if "results" in response_data:
            results = response_data["results"]
            
            # Check for direct tag entities
            if isinstance(results, dict) and "entities" in results:
                for entity in results["entities"]:
                    if entity.get("type") == "urn:entity:tag":
                        tag_urns.append(entity.get("id", ""))
            
            # Check for tag arrays
            elif isinstance(results, list):
                for item in results:
                    if isinstance(item, dict) and "id" in item:
                        tag_urns.append(item["id"])
        
        return [tag for tag in tag_urns if tag.startswith("urn:tag:")]

    async def test_preference_to_tag_mapping(self) -> Dict[str, List[str]]:
        """Test mapping user preferences to actual tag URNs"""
        
        preference_tests = {
            "sustainable": ["urn:tag:keyword:lifestyle:sustainable", "urn:tag:keyword:fashion:sustainable"],
            "wellness": ["urn:tag:keyword:lifestyle:wellness", "urn:tag:keyword:lifestyle:health"],
            "indie": ["urn:tag:genre:music:indie", "urn:tag:keyword:culture:indie"],
            "artisanal": ["urn:tag:keyword:food:artisanal", "urn:tag:keyword:craft:artisanal"],
            "minimalist": ["urn:tag:keyword:lifestyle:minimalist", "urn:tag:attribute:style:minimal"]
        }
        
        valid_mappings = {}
        
        for preference, test_urns in preference_tests.items():
            print(f"\n🧪 Testing preference: {preference}")
            valid_tags = []
            
            for tag_urn in test_urns:
                if await self._validate_tag_urn(tag_urn):
                    valid_tags.append(tag_urn)
                    print(f"   ✅ Valid: {tag_urn}")
                else:
                    print(f"   ❌ Invalid: {tag_urn}")
            
            if valid_tags:
                valid_mappings[preference] = valid_tags
        
        return valid_mappings
    
    async def _validate_tag_urn(self, tag_urn: str) -> bool:
        """Validate if a specific tag URN exists and returns data"""
        
        try:
            params = {
                "filter.type": "urn:entity:brand",
                "signal.interests.tags": tag_urn,
                "take": 1
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/v2/insights",
                    params=params,
                    headers=self.headers,
                    timeout=8
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        entities = data.get("results", {}).get("entities", [])
                        return len(entities) > 0
                    else:
                        return False
                        
        except Exception:
            return False
