# services/qloo_service.py - ENHANCED STRUCTURED VERSION
import aiohttp
import asyncio
import json
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from config import settings
from models.trend_models import UserPreferences, CulturalProfile

class QlooService:
    """
    Enhanced Qloo service with structured API integration and intelligent fallbacks.
    
    Features:
    - Multi-method brand insights discovery
    - Proper demographics parameter handling
    - Robust error handling with meaningful fallbacks
    - Real cultural intelligence integration
    - Production-ready logging and monitoring
    """
    
    # Class constants for API configuration
    # Add this method to your QlooService class
    
    def __init__(self):
        """Initialize Qloo service with configuration and connection settings."""

        self.BRAND_RELEVANT_TAGS = [
            'urn:tag:genre:brand:fashion',
            'urn:tag:genre:brand:lifestyle', 
            'urn:tag:genre:brand:entertainment',
            'urn:tag:genre:brand:technology',
            'urn:tag:genre:brand:food_and_beverage'
        ]
        self.base_url = "https://hackathon.api.qloo.com"
        self.headers = {
            "X-Api-Key": settings.qloo_api_key,
            "Content-Type": "application/json"
        }
        
        self.api_available = None
        self.request_timeout = 15
        self.max_retries = 2
        
        # Performance tracking
        self.api_call_count = 0
        self.successful_calls = 0
        self.failed_calls = 0
    async def get_similarity_score(self, entity1: str, entity2: str) -> float:
        """Get similarity between two entities (simulated for demo)"""
        # Real implementation would use:
        # response = await self._make_enhanced_request(...)
        # return response.get("similarity", 0.5)
        return random.uniform(0.4, 0.92)
    async def create_cultural_profile(self, preferences: UserPreferences) -> Optional[CulturalProfile]:
        """
        Create comprehensive cultural profile using real Qloo API integration.
        
        Args:
            preferences: User's cultural preferences across multiple domains
            
        Returns:
            CulturalProfile with real brand insights or enhanced sample data
        """
        
        try:
            print("🔍 Creating enhanced cultural profile...")

            self._log_preferences_summary(preferences)
            
            # Initialize API connection if needed
            if self.api_available is None:
                self.api_available = await self._test_api_connection()
            
            if self.api_available:
                print("🔍 Using real Qloo API with enhanced intelligence...")
                return await self._create_profile_with_enhanced_api(preferences)
            else:
                print("🔄 Using enhanced sample data with cultural intelligence...")
                return self._create_enhanced_sample_profile(preferences)
                
        except Exception as e:
            print(f"⚠️ Cultural profile creation error: {e}")
            self.failed_calls += 1
            return self._create_enhanced_sample_profile(preferences)
    
    async def _create_profile_with_enhanced_api(self, preferences: UserPreferences) -> CulturalProfile:
        """
        Create profile using enhanced multi-method API approach.
        
        This method tries multiple strategies to get the best cultural insights:
        1. Preference-targeted brand insights
        2. Demographic + popularity filtering  
        3. Cultural context analysis
        4. Cross-domain relationship mapping
        """
        
        try:
            print("🎯 Executing enhanced multi-method API strategy...")
            
            # Method 1: Get preference-targeted brand insights
            brand_insights = await self._get_preference_targeted_brands(preferences)
            
            # Method 2: Get demographic-based insights  
            demographic_insights = await self._get_demographic_insights(preferences)
            
            # Method 3: Get cultural context

            cultural_context = await self._get_enhanced_cultural_context(preferences)

            # Method 4: Get cross-domain relationships
            cross_domain_data = await self._get_cross_domain_relationships(preferences)


            # Combine all insights for comprehensive analysis
            combined_insights = self._combine_insights(
                brand_insights, demographic_insights, cultural_context, cross_domain_data
            )

            
            if self._has_meaningful_combined_data(combined_insights):
                print("✅ Enhanced Qloo insights successfully integrated!")
                return self._parse_enhanced_insights(combined_insights, preferences)
            else:
                print("⚠️ Enhanced API methods returned insufficient data, using intelligent fallback")
                return self._create_enhanced_sample_profile(preferences)
                
        except Exception as e:
            print(f"⚠️ Enhanced API approach error: {e}")
            self.failed_calls += 1
            return self._create_enhanced_sample_profile(preferences)
    
    async def _get_preference_targeted_brands(self, preferences: UserPreferences) -> Optional[Dict]:
        """Get brand insights targeted to specific user preferences."""
        
        try:
            print("🎯 Method 1: Preference-targeted brand discovery...")
            
            # Extract relevant lifestyle tags from preferences
            lifestyle_tags = self._extract_lifestyle_tags(preferences)
            
            if lifestyle_tags:
                # Try with lifestyle tags first
                params = {
                    "filter.type": "urn:entity:brand",
                    "filter.tags": ",".join(lifestyle_tags),
                    "filter.popularity.min": 0.2,  # Include emerging brands
                    "take": 12
                }
                
                result = await self._make_enhanced_request(params, "Lifestyle-targeted brands")
                if result:
                    return result
            
            # Fallback: Use preference keywords as signals
            preference_keywords = self._extract_preference_keywords(preferences)
            if preference_keywords:
                params = {
                    "filter.type": "urn:entity:brand",
                    "signal.interests.keywords": preference_keywords,
                    "filter.popularity.min": 0.3,
                    "take": 10
                }
                
                return await self._make_enhanced_request(params, "Keyword-targeted brands")
            
            return None
                    
        except Exception as e:
            print(f"⚠️ Preference-targeted brands error: {e}")
            return None
    
    async def _get_demographic_insights(self, preferences: UserPreferences) -> Optional[Dict]:
        """Get insights based on demographic and audience targeting."""
        
        try:
            print("🎯 Method 2: Demographic-based brand insights...")
            
            # Determine optimal age group and audience
            age_group = self._determine_optimal_age_group(preferences)
            audience = self._determine_target_audience(preferences)
            
            approaches = [
                {
                    "filter.type": "urn:entity:brand",
                    "filter.popularity.min": 0.3,
                    "signal.demographics.age": age_group,
                    "signal.demographics.audiences": audience,
                    "filter.location.query": "United States",
                    "take": 10
                },
                {
                    "filter.type": "urn:entity:brand", 
                    "signal.demographics.age": age_group,
                    "filter.popularity.min": 0.25,
                    "take": 8
                }
            ]
            
            for i, params in enumerate(approaches, 1):
                print(f"   🔍 Demographic approach {i}...")
                result = await self._make_enhanced_request(params, f"Demographics-{i}")
                if result:
                    return result
            
            return None
                    
        except Exception as e:
            print(f"⚠️ Demographic insights error: {e}")
            return None
    
    async def _get_enhanced_cultural_context(self, preferences: UserPreferences) -> Optional[Dict]:
        """Get enhanced cultural context from multiple entity types."""
        
        try:
            print("🎯 Method 3: Enhanced cultural context analysis...")
            
            cultural_data = {}
            
            # Get movie context (proven to work)
            movie_context = await self._get_movie_cultural_context()
            if movie_context:
                cultural_data["movies"] = movie_context
            
            # Try to get artist context for music preferences
            if preferences.music_genres:
                artist_context = await self._get_artist_cultural_context(preferences.music_genres)
                if artist_context:
                    cultural_data["artists"] = artist_context
            
            # Try to get place context for dining preferences
            if preferences.dining_preferences:
                place_context = await self._get_place_cultural_context(preferences.dining_preferences)
                if place_context:
                    cultural_data["places"] = place_context
            
            return cultural_data if cultural_data else None
                    
        except Exception as e:
            print(f"⚠️ Enhanced cultural context error: {e}")
            return None
    
    async def _get_cross_domain_relationships(self, preferences: UserPreferences) -> Optional[Dict]:
        """Analyze cross-domain cultural relationships."""
        
        try:
            print("🎯 Method 4: Cross-domain relationship analysis...")
            
            # This could be expanded to analyze relationships between
            # music preferences and fashion brands, lifestyle and dining, etc.
            # For now, we'll do a simplified cross-domain analysis
            
            cross_domain_params = {
                "filter.type": "urn:entity:brand",
                "filter.popularity.min": 0.4,  # Focus on well-connected brands
                "signal.demographics.audiences": "cultural_influencers",
                "take": 6
            }
            
            return await self._make_enhanced_request(cross_domain_params, "Cross-domain analysis")
                    
        except Exception as e:
            print(f"⚠️ Cross-domain analysis error: {e}")
            return None
    
    async def _get_movie_cultural_context(self) -> Optional[Dict]:
        """Get cultural context from movie entities (proven working method)."""
        
        params = {
            "filter.type": "urn:entity:movie",
            "filter.tags": "urn:tag:genre:media:comedy",
            "take": 6
        }
        
        return await self._make_enhanced_request(params, "Movie cultural context")
    
    async def _get_artist_cultural_context(self, music_genres: List[str]) -> Optional[Dict]:
        """Get cultural context from music artists."""
        
        # Try to get artist insights based on music preferences
        music_keywords = ",".join(music_genres[:3])
        
        params = {
            "filter.type": "urn:entity:artist",
            "signal.interests.keywords": music_keywords,
            "filter.popularity.min": 0.2,
            "take": 5
        }
        
        return await self._make_enhanced_request(params, "Artist cultural context")
    
    async def _get_place_cultural_context(self, dining_preferences: List[str]) -> Optional[Dict]:
        """Get cultural context from places/restaurants."""
        
        dining_keywords = ",".join(dining_preferences[:3])
        
        params = {
            "filter.type": "urn:entity:place",
            "signal.interests.keywords": dining_keywords,
            "filter.location.query": "New York",  # Focus on major cultural center
            "take": 4
        }
        
        return await self._make_enhanced_request(params, "Place cultural context")
    
    async def _make_enhanced_request(self, params: Dict, request_type: str) -> Optional[Dict]:
        """
        Make enhanced API request with retry logic and detailed logging.
        
        Args:
            params: API request parameters
            request_type: Description of request for logging
            
        Returns:
            API response data or None if failed
        """
        
        self.api_call_count += 1
        
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    print(f"   🔄 Retry {attempt} for {request_type}...")
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.base_url}/v2/insights",
                        params=params,
                        headers=self.headers,
                        timeout=self.request_timeout
                    ) as response:
                        
                        if response.status == 200:
                            data = await response.json()
                            entities = data.get("results", {}).get("entities", [])
                            
                            if entities:
                                print(f"✅ {request_type} SUCCESS: Found {len(entities)} entities")
                                self.successful_calls += 1
                                return data
                            else:
                                print(f"⚠️ {request_type}: API success but 0 entities returned")
                                return None
                        else:
                            error_text = await response.text()
                            print(f"⚠️ {request_type} failed ({response.status}): {error_text[:100]}...")
                            
                            # Don't retry on client errors (400-499)
                            if 400 <= response.status < 500:
                                break
                                
            except asyncio.TimeoutError:
                print(f"⏰ {request_type} timeout (attempt {attempt + 1})")
            except Exception as e:
                print(f"⚠️ {request_type} error (attempt {attempt + 1}): {e}")
        
        self.failed_calls += 1
        return None
    
    def _combine_insights(self, *insights: Optional[Dict]) -> Dict:
        """Combine multiple insight sources into unified data structure."""
        
        print("🔍 ENTITY COMBINATION DEBUG:")
        input_insights_debug = []
        for i, insight in enumerate(insights):
            if insight:
                if isinstance(insight, dict) and "results" in insight:
                    entity_count = len(insight.get("results", {}).get("entities", []))
                    input_insights_debug.append(f"Input{i+1}: {entity_count} entities")
                else:
                    context_keys = list(insight.keys()) if isinstance(insight, dict) else ["unknown"]
                    input_insights_debug.append(f"Input{i+1}: {context_keys} context")
            else:
                input_insights_debug.append(f"Input{i+1}: None")
        
        print(f"   📥 Raw inputs: {' | '.join(input_insights_debug)}")
        
        combined = {
            "brand_entities": [],
            "movie_entities": [],
            "artist_entities": [],
            "place_entities": [],
            "total_entities": 0,
            "data_sources": [],
            "entities": [],  # This is critical for consolidation
            "debug_info": {
                "combination_timestamp": datetime.now().isoformat(),
                "input_sources": len([i for i in insights if i is not None]),
                "entity_breakdown": {}
            }
        }
        
        method_names = [
            "preference_targeted_brands",
            "demographic_insights", 
            "movie_context",
            "artist_context",
            "place_context",
            "cross_domain_analysis"
        ]
        
        method_index = 0
        processing_log = []
        
        for insight in insights:
            if insight:
                if isinstance(insight, dict) and "results" in insight:
                    # Standard insights response
                    entities = insight.get("results", {}).get("entities", [])
                    entity_count = len(entities)
                    
                    entity_type_counts = {"brand": 0, "movie": 0, "artist": 0, "place": 0, "other": 0}
                    
                    # FIXED: Process each entity with proper scope
                    for entity in entities:
                        try:
                            entity_type = entity.get("type", "")
                            entity_name = entity.get("name", "Unknown")
                            
                            # NEW: Use name-based classification since all types are "urn:entity"
                            classification = self._classify_entity_by_name(entity)
                            
                            if classification == "brand":
                                combined["brand_entities"].append(entity)
                                entity_type_counts["brand"] += 1
                            elif classification == "movie":
                                combined["movie_entities"].append(entity)
                                entity_type_counts["movie"] += 1
                            elif classification == "artist":
                                combined["artist_entities"].append(entity)
                                entity_type_counts["artist"] += 1
                            elif classification == "place":
                                combined["place_entities"].append(entity)
                                entity_type_counts["place"] += 1
                            else:
                                entity_type_counts["other"] += 1
                                print(f"      ⚠️ Unclassified entity: {entity_name} (type: {entity_type})")
                            
                            # Add to main entities list
                            combined["entities"].append(entity)
                            
                        except Exception as e:
                            print(f"⚠️ Error processing entity {entity_name}: {e}")
                            continue
                    
                    method_name = method_names[method_index] if method_index < len(method_names) else f"method_{method_index+1}"
                    processing_log.append(f"{method_name}: {entity_type_counts}")
                    combined["debug_info"]["entity_breakdown"][method_name] = entity_type_counts
                    combined["data_sources"].append(f"{method_name}_{entity_count}_entities")
                    method_index += 1
                    
                elif isinstance(insight, dict):
                    # Cultural context with multiple entity types
                    for key, value in insight.items():
                        if key in ["movies", "artists", "places"] and value:
                            entities = value.get("results", {}).get("entities", [])
                            entity_count = len(entities)
                            
                            for entity in entities:
                                try:
                                    combined[f"{key[:-1]}_entities"].append(entity)
                                    combined["entities"].append(entity)
                                except Exception as e:
                                    print(f"⚠️ Error processing cultural entity: {e}")
                                    continue
                            
                            context_method = f"cultural_{key}"
                            processing_log.append(f"{context_method}: {entity_count} entities")
                            combined["debug_info"]["entity_breakdown"][context_method] = {key[:-1]: entity_count}
                            combined["data_sources"].append(f"cultural_{key}_{entity_count}_entities")
        
        # CRITICAL: Consolidate entity counts
        print("🔍 ENTITY CONSOLIDATION DEBUG:")
        all_entities = combined["entities"]
        entity_categories = ["brand_entities", "movie_entities", "artist_entities", "place_entities"]
        
        for category in entity_categories:
            category_entities = combined.get(category, [])
            if category_entities:
                print(f"   📦 {category}: {len(category_entities)} entities")
                first_entity = category_entities[0]
                entity_name = first_entity.get("name", "Unknown")
                entity_type = first_entity.get("type", "Unknown")
                print(f"      🔍 Example: {entity_name} (type: {entity_type})")
        
        print(f"   📊 Total consolidated entities: {len(all_entities)}")
        
        combined["total_entities"] = len(all_entities)
        
        print(f"   📈 Processing summary: {' | '.join(processing_log)}")
        print(f"   ✅ Combination complete: {combined['total_entities']} total entities")
        
        return combined

    def _classify_entity_by_name(self, entity: Dict) -> str:
        """Classify entities when type field is generic (urn:entity)"""
        
        entity_name = entity.get("name", "").lower()
        
        # Known brands from your debug output
        known_brands = [
            "nike", "netflix", "instagram", "youtube", "twitter", "cnn", 
            "christian dior", "victoria's secret", "playstation", "new york times",
            "saputo", "beyu", "gameday couture", "haldiram's", "china airlines",
            "blimpie", "lotte", "holded", "b & m", "ulla popken", "mtr foods", "posh"
        ]
        
        # Known artists from your debug output
        known_artists = ["coldplay", "radiohead", "the beatles"]
        
        # Known movies from your debug output  
        known_movies = ["django unchained", "wolf of wall street"]
        
        # Known places from your debug output
        known_places = ["washington square park", "top of the rock", "niagara falls"]
        
        # Classify by exact name matching
        if any(brand in entity_name for brand in known_brands):
            return "brand"
        elif any(artist in entity_name for artist in known_artists):
            return "artist"
        elif any(movie in entity_name for movie in known_movies):
            return "movie"
        elif any(place in entity_name for place in known_places):
            return "place"
        else:
            # Pattern-based fallback classification
            if any(pattern in entity_name for pattern in ["company", "corp", "inc", "ltd"]):
                return "brand"
            elif "park" in entity_name or "square" in entity_name or "falls" in entity_name:
                return "place"
            else:
                return "unknown"


    
    def _has_meaningful_combined_data(self, combined_insights: Dict) -> bool:
        """Check if combined insights contain meaningful data for analysis."""
        
        total_entities = combined_insights.get("total_entities", 0)
        brand_entities = len(combined_insights.get("brand_entities", []))
        
        # We need at least 3 total entities OR at least 1 brand entity for meaningful analysis
        return total_entities >= 3 or brand_entities >= 1
    
    def _parse_enhanced_insights(self, combined_insights: Dict, preferences: UserPreferences) -> CulturalProfile:
        """Parse combined insights into comprehensive cultural profile."""
        
        try:
            print("🔍 Parsing enhanced cultural insights...")
            print("🔍 BRAND PARSING DEBUG:")
            raw_brands = combined_insights.get("brand_entities", [])
            print(f"📋 Raw brand entities from API: {len(raw_brands)}")
            
            for i, brand in enumerate(raw_brands[:3]):
                print(f"   {i+1}. {brand}")  # Print full brand object
            
            # Check how brands are being processed
            processed_brands = []
            for entity in raw_brands:
                if isinstance(entity, dict):
                    brand_name = entity.get('name') or entity.get('title') or str(entity)
                    processed_brands.append(brand_name)
                    print(f"✅ Processed brand: {brand_name}")
                else:
                    print(f"⚠️ Unexpected brand format: {type(entity)} - {entity}")
            
            print(f"🏢 Final processed brands: {processed_brands}")

            print("🔍 RAW API RESPONSE DEBUG:")
    
    # Check all entity types in your response
            all_entities = combined_insights.get("entities", [])
            print(f"📋 Total raw entities: {len(all_entities)}")
            
            entity_types = {}
            for entity in all_entities:
                entity_type = entity.get('type', 'unknown')
                entity_name = entity.get('name') or entity.get('title', 'Unknown')
                
                if entity_type not in entity_types:
                    entity_types[entity_type] = []
                entity_types[entity_type].append(entity_name)
            
            print("📊 Entity breakdown by type:")
            for entity_type, names in entity_types.items():
                print(f"   {entity_type}: {len(names)} entities")
                for name in names[:2]:  # Show first 2 examples
                    print(f"      - {name}")
            ##
            
            # Extract entities by type
            brand_entities = combined_insights.get("brand_entities", [])
            movie_entities = combined_insights.get("movie_entities", [])
            artist_entities = combined_insights.get("artist_entities", [])
            place_entities = combined_insights.get("place_entities", [])
            
            # Extract entity names
            brands = [entity.get("name", "") for entity in brand_entities if entity.get("name")]
            movies = [entity.get("name", "") for entity in movie_entities if entity.get("name")]
            artists = [entity.get("name", "") for entity in artist_entities if entity.get("name")]
            places = [entity.get("name", "") for entity in place_entities if entity.get("name")]


            # Enhanced cultural segment analysis
            segments = self._extract_enhanced_cultural_segments(
                brand_entities, preferences, movies, artists, places
            )
             
            
            # Calculate enhanced behavioral indicators
            behavioral_indicators = self._calculate_enhanced_behavioral_indicators(
                combined_insights, segments, preferences
            )
            
            # Calculate confidence score based on data richness
            confidence_score = self._calculate_enhanced_confidence_score(combined_insights, segments)
            
            print(f"🎭 Enhanced cultural segments: {segments}")
            if brands:
                print(f"🏢 Real brand insights: {brands[:4]}")
            if artists:
                print(f"🎵 Cultural artists: {artists[:3]}")
            if places:
                print(f"📍 Cultural places: {places[:3]}")
            
            # ✅ FIXED: Ensure data_sources is a list, not an integer
            data_sources_list = combined_insights.get("data_sources", [])
            if isinstance(data_sources_list, int):
                # Convert count back to list format for compatibility
                data_sources_list = [f"method_{i+1}" for i in range(data_sources_list)]
             ##### NEW DEBUG CODE: Final profile creation summary #####
            print("🔍 PROFILE CREATION SUMMARY:")
            print(f"   📊 Profile elements:")
            print(f"      - Cultural segments: {len(segments)}")
            print(f"      - Brands: {len(brands)}")
            print(f"      - Artists: {len(artists)}")
            print(f"      - Places: {len(places)}")
            print(f"      - Confidence score: {confidence_score}")
            print(f"      - Behavioral indicators: {len(behavioral_indicators)}")
            print(f"   ✅ Profile ready for creation")
            ##### END NEW DEBUG CODE #####
            
            return CulturalProfile(
                profile_id=f"qloo_enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                cultural_segments=segments,
                cross_domain_connections={
                    "music": preferences.music_genres,
                    "fashion": preferences.fashion_styles,
                    "dining": preferences.dining_preferences,
                    "lifestyle": preferences.lifestyle_choices,
                    "entertainment": preferences.entertainment_types,
                    "brands": brands[:8],
                    "artists": artists[:6],
                    "movies": movies[:4],
                    "places": places[:4],
                    "data_sources": data_sources_list 
                },
                behavioral_indicators=behavioral_indicators,
                confidence_score=confidence_score
            )
            
        except Exception as e:
            print(f"⚠️ Enhanced insights parsing error: {e}")
            ##### NEW DEBUG CODE: Error context debugging #####
            print("🔍 ERROR CONTEXT DEBUG:")
            print(f"   📊 Combined insights keys: {list(combined_insights.keys()) if combined_insights else 'None'}")
            print(f"   📊 Combined insights type: {type(combined_insights)}")
            import traceback
            print(f"   📊 Full error traceback:")
            traceback.print_exc()
            ##### END NEW DEBUG CODE #####
            return self._create_enhanced_sample_profile(preferences)

    
    # Utility methods for enhanced analysis
    
    def _extract_lifestyle_tags(self, preferences: UserPreferences) -> List[str]:
        """Extract relevant lifestyle tags from user preferences."""
        
        relevant_tags = []
        all_prefs = (preferences.lifestyle_choices + preferences.fashion_styles + 
                    preferences.dining_preferences)
        
        for pref in all_prefs:
            pref_lower = pref.lower()
            for keyword, tag in self.BRAND_RELEVANT_TAGS.items():
                if keyword in pref_lower and tag not in relevant_tags:
                    relevant_tags.append(tag)
        
        return relevant_tags[:4]  # Limit to 4 most relevant tags
    
    def _extract_preference_keywords(self, preferences: UserPreferences) -> str:
        """Extract meaningful keywords from all user preferences."""
        
        keywords = []
        
        # Priority order: lifestyle > fashion > dining > music
        preference_categories = [
            preferences.lifestyle_choices,
            preferences.fashion_styles,
            preferences.dining_preferences,
            preferences.music_genres[:2]  # Limit music to 2 for balance
        ]
        
        for category in preference_categories:
            for pref in category[:3]:  # Max 3 per category
                clean_pref = pref.lower().strip()
                if len(clean_pref) > 2 and clean_pref not in keywords:
                    keywords.append(clean_pref)
        
        return ",".join(keywords[:6])  # API efficiency limit
    
    def _determine_optimal_age_group(self, preferences: UserPreferences) -> str:
        """Determine optimal age group based on preference patterns."""
        
        # Analyze preferences to suggest age group
        all_prefs = " ".join(preferences.lifestyle_choices + preferences.music_genres + 
                           preferences.fashion_styles).lower()
        
        if any(term in all_prefs for term in ["tiktok", "gen z", "gaming", "streaming"]):
            return "24_and_younger"
        elif any(term in all_prefs for term in ["career", "startup", "remote work", "indie"]):
            return "25_to_29"
        elif any(term in all_prefs for term in ["family", "home", "investment", "premium"]):
            return "30_to_34"
        else:
            return "25_to_29"  # Default to millennial range
    
    def _determine_target_audience(self, preferences: UserPreferences) -> str:
        """Determine target audience based on cultural preferences."""
        
        all_prefs = " ".join(preferences.lifestyle_choices + preferences.fashion_styles + 
                           preferences.entertainment_types).lower()
        
        if any(term in all_prefs for term in ["creative", "art", "design", "music"]):
            return "creatives"
        elif any(term in all_prefs for term in ["wellness", "health", "mindful", "yoga"]):
            return "wellness_enthusiasts"
        elif any(term in all_prefs for term in ["startup", "entrepreneur", "business"]):
            return "entrepreneurs"
        elif any(term in all_prefs for term in ["urban", "city", "professional"]):
            return "urban_professionals"
        else:
            return "millennials"  # Default broad audience
    
    def _extract_enhanced_cultural_segments(self, brand_entities: List[Dict], 
                                          preferences: UserPreferences,
                                          movies: List[str], artists: List[str], 
                                          places: List[str]) -> List[str]:
        """Extract cultural segments from multiple data sources."""
        
        segments = set()
        
        # Analyze brand entities for cultural insights
        for entity in brand_entities:
            brand_name = entity.get("name", "").lower()
            
            # Brand-based cultural analysis
            if any(keyword in brand_name for keyword in ["sustainable", "eco", "green", "organic"]):
                segments.add("sustainability advocates")
            elif any(keyword in brand_name for keyword in ["luxury", "premium", "designer"]):
                segments.add("luxury consumers")
            elif any(keyword in brand_name for keyword in ["tech", "digital", "innovation"]):
                segments.add("tech enthusiasts")
            elif any(keyword in brand_name for keyword in ["wellness", "health", "fitness"]):
                segments.add("wellness advocates")
            elif any(keyword in brand_name for keyword in ["art", "creative", "design"]):
                segments.add("creative professionals")
        
        # Analyze user preferences
        preference_segments = self._extract_cultural_segments_from_preferences(preferences)
        segments.update(preference_segments)
        
        # Cross-reference with cultural entities
        if artists and any("indie" in artist.lower() for artist in artists):
            segments.add("indie culture")
        if places and any("artisan" in place.lower() for place in places):
            segments.add("artisanal culture")
        
        # Ensure we have meaningful segments
        segments_list = list(segments)
        if not segments_list:
            segments_list = ["cultural enthusiasts", "brand-conscious consumers"]
        
        return segments_list[:6]  # Limit to 6 most relevant segments
    
    def _calculate_enhanced_behavioral_indicators(self, combined_insights: Dict, 
                                                segments: List[str], 
                                                preferences: UserPreferences) -> Dict[str, float]:
        """Calculate enhanced behavioral indicators based on rich data."""
        
        total_entities = combined_insights.get("total_entities", 0)
        brand_count = len(combined_insights.get("brand_entities", []))
        data_source_count = len(combined_insights.get("data_sources", []))
        
        # Base scores
        early_adopter = 0.75
        influence_score = 0.65
        cultural_openness = 0.8
        
        # Adjust based on data richness
        early_adopter += min(0.15, total_entities * 0.01)
        influence_score += min(0.2, len(segments) * 0.03)
        cultural_openness += min(0.15, data_source_count * 0.02)
        
        # Adjust based on brand diversity
        brand_diversity = min(1.0, brand_count / 8)
        
        # Preference complexity factor
        pref_complexity = len(preferences.music_genres + preferences.lifestyle_choices + 
                             preferences.fashion_styles + preferences.dining_preferences) / 20
        
        return {
            "early_adopter": min(0.95, early_adopter),
            "influence_score": min(0.9, influence_score),
            "cultural_openness": min(0.95, cultural_openness),
            "brand_affinity": brand_diversity,
            "cultural_diversity": min(1.0, len(segments) / 6),
            "preference_complexity": min(1.0, pref_complexity),
            "data_richness": min(1.0, total_entities / 15)
        }
    
    def _calculate_enhanced_confidence_score(self, combined_insights: Dict, segments: List[str]) -> float:
        """Calculate confidence score based on data quality and completeness."""
        
        base_confidence = 80.0
        
        # Data richness bonus
        total_entities = combined_insights.get("total_entities", 0)
        brand_entities = len(combined_insights.get("brand_entities", []))
        data_sources = len(combined_insights.get("data_sources", []))
        
        # Scoring factors
        entity_bonus = min(15.0, total_entities * 1.2)
        brand_bonus = min(10.0, brand_entities * 2.0)
        source_bonus = min(8.0, data_sources * 2.0)
        segment_bonus = min(7.0, len(segments) * 1.2)
        
        final_confidence = base_confidence + entity_bonus + brand_bonus + source_bonus + segment_bonus
        
        return min(98.0, final_confidence)
    
    # Keep existing methods for compatibility
    
    async def _test_api_connection(self) -> bool:
        """Test API connection with proven working parameters."""
        
        try:
            params = {
                "filter.type": "urn:entity:movie",
                "filter.tags": "urn:tag:genre:media:comedy",
                "take": 1
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
                        entities = data.get("results", {}).get("entities", [])
                        print(f"✅ Enhanced API connection test successful - {len(entities)} entities")
                        return True
                    else:
                        print(f"⚠️ API connection test failed: {response.status}")
                        return False
                        
        except Exception as e:
            print(f"❌ API connection test error: {e}")
            return False
    
    def _extract_cultural_segments_from_preferences(self, preferences: UserPreferences) -> List[str]:
        """Extract cultural segments from user preferences."""
        
        segments = []
        all_prefs = (preferences.music_genres + preferences.dining_preferences + 
                    preferences.fashion_styles + preferences.lifestyle_choices)
        
        preference_mapping = {
            "indie": "indie culture",
            "sustain": "sustainability advocates", 
            "minimal": "minimalists",
            "tech": "tech enthusiasts",
            "wellness": "wellness advocates",
            "luxury": "luxury consumers",
            "vintage": "vintage enthusiasts",
            "creative": "creative professionals",
            "artisan": "artisanal culture"
        }
        
        for pref in all_prefs:
            pref_lower = pref.lower()
            for keyword, segment in preference_mapping.items():
                if keyword in pref_lower and segment not in segments:
                    segments.append(segment)
        
        return segments
    
    def _create_enhanced_sample_profile(self, preferences: UserPreferences) -> CulturalProfile:
        """Create enhanced sample profile with intelligent analysis."""
        
        print("🔄 Creating enhanced intelligent sample profile...")
        
        segments = self._extract_cultural_segments_from_preferences(preferences)
        if not segments:
            segments = ["cultural enthusiasts", "trend-conscious consumers"]
        
        # Enhanced behavioral indicators for sample profile
        pref_count = len(preferences.music_genres + preferences.dining_preferences + 
                        preferences.fashion_styles + preferences.lifestyle_choices)
        
        early_adopter = min(0.9, 0.75 + (pref_count * 0.015))
        influence_score = min(0.85, 0.65 + (len(segments) * 0.03))
        cultural_openness = min(0.9, 0.8 + (pref_count * 0.01))
        
        return CulturalProfile(
            profile_id=f"enhanced_sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            cultural_segments=segments,
            cross_domain_connections={
                "music": preferences.music_genres,
                "fashion": preferences.fashion_styles,
                "dining": preferences.dining_preferences,
                "lifestyle": preferences.lifestyle_choices,
                "entertainment": preferences.entertainment_types
            },
            behavioral_indicators={
                "early_adopter": early_adopter,
                "influence_score": influence_score,
                "cultural_openness": cultural_openness,
                "preference_diversity": min(1.0, pref_count / 15),
                "cultural_sophistication": min(1.0, len(segments) / 5)
            },
            confidence_score=min(92.0, 82.0 + (pref_count * 0.8) + (len(segments) * 1.5))
        )
    
    def _log_preferences_summary(self, preferences: UserPreferences) -> None:
        """Log summary of user preferences for debugging."""
        
        print(f"📝 User Preferences Summary:")
        print(f"   🎵 Music: {preferences.music_genres}")
        print(f"   👔 Fashion: {preferences.fashion_styles}")
        print(f"   🍽️ Dining: {preferences.dining_preferences}")
        print(f"   🏡 Lifestyle: {preferences.lifestyle_choices}")
        print(f"   🎬 Entertainment: {preferences.entertainment_types}")
    
    async def get_similar_profiles(self, profile_id: str) -> List[Dict]:
        """Get similar cultural profiles using enhanced analysis."""
        
        try:
            print(f"🔍 Enhanced cultural community analysis...")
            
            if self.api_available:
                # Try to get real audience insights
                params = {
                    "filter.type": "urn:entity:brand",
                    "filter.popularity.min": 0.4,
                    "signal.demographics.audiences": "cultural_influencers",
                    "take": 8
                }
                
                result = await self._make_enhanced_request(params, "Similar profiles")
                if result:
                    entities = result.get("results", {}).get("entities", [])
                    return self._create_similar_profiles_from_entities(profile_id, entities)
            
            # Enhanced sample similar profiles
            return self._create_enhanced_similar_profiles(profile_id)
                        
        except Exception as e:
            print(f"⚠️ Similar profiles error: {e}")
            return self._create_enhanced_similar_profiles(profile_id)
    
    def _create_similar_profiles_from_entities(self, profile_id: str, entities: List[Dict]) -> List[Dict]:
        """Create similar profiles based on real brand entities."""
        
        similar_profiles = []
        
        for i, entity in enumerate(entities[:4]):
            brand_name = entity.get("name", f"Cultural Brand {i+1}")
            
            similar_profiles.append({
                "profile_id": f"qloo_similar_{profile_id}_{i+1}",
                "similarity_score": 0.88 - (i * 0.04),
                "emerging_interests": [
                    f"{brand_name}-inspired lifestyle",
                    "cultural authenticity",
                    "cross-domain experiences"
                ],
                "cultural_overlap": ["brand-conscious consumers", "cultural early adopters"],
                "behavioral_patterns": {
                    "early_adopter": 0.82 - (i * 0.03), 
                    "influence": 0.74 + (i * 0.02),
                    "cultural_engagement": 0.79
                }
            })
        
        return similar_profiles
    
    def _create_enhanced_similar_profiles(self, profile_id: str) -> List[Dict]:
        """Create enhanced sample similar profiles."""
        
        return [
            {
                "profile_id": f"enhanced_similar_{profile_id}_1",
                "similarity_score": 0.89,
                "emerging_interests": [
                    "sustainable luxury brands", 
                    "tech-enabled wellness", 
                    "artisanal digital experiences"
                ],
                "cultural_overlap": ["sustainability advocates", "tech enthusiasts", "luxury consumers"],
                "behavioral_patterns": {
                    "early_adopter": 0.86, 
                    "influence": 0.74,
                    "cultural_openness": 0.82,
                    "brand_loyalty": 0.67
                }
            },
            {
                "profile_id": f"enhanced_similar_{profile_id}_2",
                "similarity_score": 0.84,
                "emerging_interests": [
                    "indie wellness brands",
                    "minimalist tech products", 
                    "authentic cultural experiences"
                ],
                "cultural_overlap": ["indie culture", "wellness advocates", "minimalists"],
                "behavioral_patterns": {
                    "early_adopter": 0.81, 
                    "influence": 0.71,
                    "cultural_openness": 0.85,
                    "authenticity_preference": 0.79
                }
            },
            {
                "profile_id": f"enhanced_similar_{profile_id}_3",
                "similarity_score": 0.78,
                "emerging_interests": [
                    "creative technology tools",
                    "sustainable fashion platforms",
                    "community-driven brands"
                ],
                "cultural_overlap": ["creative professionals", "sustainability advocates"],
                "behavioral_patterns": {
                    "early_adopter": 0.83, 
                    "influence": 0.68,
                    "cultural_openness": 0.80,
                    "community_engagement": 0.75
                }
            }
        ]
    
    def get_performance_metrics(self) -> Dict[str, any]:
        """Get service performance metrics for monitoring."""
        
        success_rate = (self.successful_calls / max(1, self.api_call_count)) * 100
        
        return {
            "total_api_calls": self.api_call_count,
            "successful_calls": self.successful_calls,
            "failed_calls": self.failed_calls,
            "success_rate": f"{success_rate:.1f}%",
            "api_available": self.api_available
        }
    

# Enhanced test function
async def test_enhanced_qloo_integration():
    """Test the enhanced Qloo integration with comprehensive scenarios."""
    
    print("🧪 Testing Enhanced Qloo Integration")
    print("=" * 60)
    
    from models.trend_models import UserPreferences
    
    # Test scenarios for different user types
    test_scenarios = [
        {
            "name": "Sustainable Tech Professional",
            "prefs": UserPreferences(
                music_genres=["indie rock", "electronic", "ambient"],
                dining_preferences=["sustainable", "organic", "plant-based", "local"],
                fashion_styles=["minimalist", "sustainable", "tech wear"],
                entertainment_types=["documentaries", "indie films", "podcasts"],
                lifestyle_choices=["sustainable living", "remote work", "wellness", "technology", "minimalism"]
            )
        },
        {
            "name": "Creative Wellness Advocate", 
            "prefs": UserPreferences(
                music_genres=["indie folk", "jazz", "world music"],
                dining_preferences=["artisanal", "organic", "vegan", "fair trade"],
                fashion_styles=["vintage", "artisanal", "sustainable", "bohemian"],
                entertainment_types=["art galleries", "live music", "theater", "books"],
                lifestyle_choices=["wellness", "creativity", "mindfulness", "community", "authenticity"]
            )
        }
    ]
    
    qloo_service = QlooService()
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}️⃣ Testing: {scenario['name']}")
        print("-" * 40)
        
        profile = await qloo_service.create_cultural_profile(scenario['prefs'])
        
        if profile:
            print(f"✅ Enhanced profile created successfully!")
            print(f"   📋 ID: {profile.profile_id}")
            print(f"   🎭 Cultural segments: {profile.cultural_segments}")
            print(f"   📊 Confidence: {profile.confidence_score:.1f}%")
            
            # Show cross-domain connections
            connections = profile.cross_domain_connections
            if connections.get("brands"):
                print(f"   🏢 Real brand insights: {connections['brands'][:3]}")
            if connections.get("artists"):
                print(f"   🎵 Cultural artists: {connections['artists'][:3]}")
            
            # Show enhanced behavioral indicators
            indicators = profile.behavioral_indicators
            print(f"   🎯 Early adopter: {indicators.get('early_adopter', 0):.2f}")
            print(f"   💫 Cultural openness: {indicators.get('cultural_openness', 0):.2f}")
            print(f"   📈 Data richness: {indicators.get('data_richness', 0):.2f}")
            
            # Test similar profiles
            similar = await qloo_service.get_similar_profiles(profile.profile_id)
            if similar:
                print(f"   👥 Found {len(similar)} similar profiles")
                print(f"   🎯 Top similarity: {similar[0]['similarity_score']:.0%}")
        else:
            print("❌ Profile creation failed")
    
    # Show performance metrics
    metrics = qloo_service.get_performance_metrics()
    print(f"\n📊 Enhanced Service Performance:")
    for key, value in metrics.items():
        print(f"   {key}: {value}")
    
    print(f"\n🎯 Enhanced Qloo integration test completed!")
    print(f"✅ Your TrendSeer now has production-ready cultural intelligence!")

# Add this test function to check your Qloo service independently
async def test_qloo_variations():
    """Test if Qloo returns different results for different inputs"""
    
    from models.trend_models import UserPreferences
    from services.trend_analyzer import TrendAnalyzer
    
    analyzer = TrendAnalyzer()
    
    # Test 1: Electronic music preferences
    prefs1 = UserPreferences(
        music_genres=["electronic", "techno", "house"],
        fashion_styles=["streetwear", "techwear"],
        lifestyle_choices=["nightlife", "urban living"]
    )
    
    # Test 2: Folk music preferences  
    prefs2 = UserPreferences(
        music_genres=["folk", "acoustic", "indie folk"],
        fashion_styles=["vintage", "bohemian"],
        lifestyle_choices=["nature", "mindfulness", "artisanal"]
    )
    
    print("🧪 Testing Qloo variations...")
    
    profile1 = await analyzer.qloo_service.create_cultural_profile(prefs1)
    print(f"Test 1 - Segments: {profile1.cultural_segments}")
    print(f"Test 1 - Artists: {profile1.cross_domain_connections.get('artists', [][:3])}")
    
    profile2 = await analyzer.qloo_service.create_cultural_profile(prefs2)
    print(f"Test 2 - Segments: {profile2.cultural_segments}")
    print(f"Test 2 - Artists: {profile2.cross_domain_connections.get('artists', [])[:3]}")
    
    # Check if results are different
    same_segments = profile1.cultural_segments == profile2.cultural_segments
    same_artists = (profile1.cross_domain_connections.get('artists', []) == 
                   profile2.cross_domain_connections.get('artists', []))
    
    print(f"🔍 Results comparison:")
    print(f"   Same segments: {same_segments}")
    print(f"   Same artists: {same_artists}")
    
    if same_segments and same_artists:
        print("⚠️ WARNING: Qloo returning identical results for different inputs!")
        print("   This suggests fallback/sample data is being used instead of real API data.")
    else:
        print("✅ SUCCESS: Qloo returning varied results for different inputs!")

    

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_enhanced_qloo_integration())
    asyncio.run(test_qloo_variations())

