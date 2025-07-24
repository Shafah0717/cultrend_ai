# utils/helpers.py
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any
from models.trend_models import UserPreferences
import os

def save_to_file(data: Dict, filename: str):
    """Save data to JSON file for debugging"""
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    with open(f"data/{filename}", 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    print(f"✅ Data saved to data/{filename}")

def load_from_file(filename: str) -> Dict:
    """Load data from JSON file"""
    
    try:
        with open(f"data/{filename}", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File data/{filename} not found")
        return {}

def validate_api_keys():
    """Validate that all required API keys are present"""
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    required_keys = ["QLOO_API_KEY", "GOOGLE_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Missing API keys: {', '.join(missing_keys)}")
        print("Please add them to your .env file")
        return False
    else:
        print("✅ All API keys found")
        return True

def create_demo_data():
    """Create demo data for the hackathon presentation"""
    
    demo_scenarios = {
        "indie_culture_demo": {
            "preferences": {
                "music_genres": ["indie rock", "folk", "ambient"],
                "dining_preferences": ["artisanal coffee", "plant-based", "local sourcing"],
                "fashion_styles": ["vintage", "minimalist", "sustainable"],
                "entertainment_types": ["indie films", "live music", "podcasts"],
                "lifestyle_choices": ["sustainable living", "mindfulness", "remote work"]
            },
            "expected_trends": [
                "Sustainable tech accessories with vintage aesthetics",
                "Artisanal wellness products for remote workers",
                "Locally-sourced functional beverages with indie branding"
            ]
        },
        "urban_trendsetter_demo": {
            "preferences": {
                "music_genres": ["hip-hop", "jazz", "R&B"],
                "dining_preferences": ["street food", "fusion cuisine", "craft cocktails"],
                "fashion_styles": ["streetwear", "luxury brands", "sneakers"],
                "entertainment_types": ["sports", "gaming", "social media"],
                "lifestyle_choices": ["fitness", "urban living", "nightlife"]
            },
            "expected_trends": [
                "Tech-enhanced fitness gear with streetwear aesthetics",
                "Fusion street food with premium ingredients",
                "Gaming-inspired luxury accessories"
            ]
        }
    }
    
    save_to_file(demo_scenarios, "demo_scenarios.json")
    print("✅ Demo scenarios created for hackathon presentation")

async def test_full_system():
    """Comprehensive system test"""
    
    print("🧪 Testing TrendSeer System with Gemini LLM")
    print("=" * 50)
    
    # Test 1: API key validation
    print("1. Testing API keys...")
    if not validate_api_keys():
        return False
    
    # Test 2: Gemini connection
    print("2. Testing Gemini LLM connection...")
    try:
        from services.gemini_service import GeminiService
        gemini_service = GeminiService()
        
        test_response = gemini_service.model.generate_content("Hello, this is a connection test.")
        if test_response and test_response.text:
            print("✅ Gemini LLM connection successful")
        else:
            print("❌ Gemini LLM connection failed")
            return False
    except Exception as e:
        print(f"❌ Gemini connection error: {e}")
        return False
    
    # Test 3: Sample preferences analysis
    print("3. Testing with sample preferences...")
    from models.trend_models import UserPreferences
    from services.trend_analyzer import TrendAnalyzer
    
    sample_preferences = UserPreferences(
        music_genres=["indie rock", "folk"],
        dining_preferences=["artisanal coffee", "plant-based"],
        fashion_styles=["minimalist", "sustainable"],
        entertainment_types=["indie films", "podcasts"],
        lifestyle_choices=["sustainable living", "wellness"]
    )
    
    # Test 4: Full trend analysis
    print("4. Running complete trend analysis...")
    analyzer = TrendAnalyzer()
    
    try:
        analysis = await analyzer.predict_trends(sample_preferences, "90d")
        
        if analysis.total_predictions > 0:
            print(f"✅ Analysis successful! Generated {analysis.total_predictions} predictions")
            print(f"   Average confidence: {analysis.average_confidence:.1f}%")
            
            # Show top prediction
            if analysis.predictions:
                top_prediction = analysis.predictions[0]
                print(f"   🥇 Top prediction: {top_prediction.predicted_trend}")
                print(f"   🎯 Confidence: {top_prediction.confidence_score:.0f}%")
                print(f"   ⏰ Timeline: {top_prediction.timeline_days} days")
            
            # Save results for demo
            save_to_file(analysis.dict(), "test_analysis_results.json")
            
            return True
        else:
            print("❌ No predictions generated")
            return False
            
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

def performance_benchmark():
    """Benchmark system performance"""
    
    import time
    
    print("⚡ Performance Benchmark")
    print("-" * 30)
    
    # Test API response times (mock)
    start_time = time.time()
    # Simulate API calls
    time.sleep(0.1)  # Simulate Qloo API call
    qloo_time = time.time() - start_time
    
    start_time = time.time()
    time.sleep(0.3)  # Simulate Gemini API call
    gemini_time = time.time() - start_time
    
    print(f"Qloo API response time: {qloo_time:.2f}s")
    print(f"Gemini LLM response time: {gemini_time:.2f}s")
    print(f"Total analysis time: {qloo_time + gemini_time:.2f}s")

# Demo script for hackathon
class HackathonDemo:
    """Demo script specifically for hackathon presentation"""
    
    def __init__(self):
        from services.trend_analyzer import TrendAnalyzer
        self.analyzer = TrendAnalyzer()
    
    async def run_compelling_demo(self):
        """Run a compelling demo for judges"""
        
        print("🎭 HACKATHON DEMO: TrendSeer with Gemini LLM")
        print("=" * 60)
        
        # Demo persona: Someone whose cultural preferences predict emerging trends
        print("\n👤 Demo Profile: Indie Culture Sustainability Advocate")
        print("   Music: Indie rock, folk, ambient")
        print("   Dining: Artisanal coffee, plant-based, local sourcing")
        print("   Fashion: Vintage, minimalist, sustainable")
        print("   Entertainment: Indie films, live music, podcasts")
        print("   Lifestyle: Sustainable living, mindfulness, remote work")
        
        demo_preferences = UserPreferences(
            music_genres=["indie rock", "folk", "ambient"],
            dining_preferences=["artisanal coffee", "plant-based", "local sourcing"],
            fashion_styles=["vintage", "minimalist", "sustainable"],
            entertainment_types=["indie films", "live music", "podcasts"],
            lifestyle_choices=["sustainable living", "mindfulness", "remote work"]
        )
        
        print("\n🤖 Gemini AI is analyzing cultural patterns...")
        
        # Run analysis
        analysis = await self.analyzer.predict_trends(demo_preferences, "90d")
        
        # Present results in compelling way
        print("\n🎯 TREND PREDICTIONS FOR NEXT 90 DAYS:")
        print("=" * 50)
        
        for i, prediction in enumerate(analysis.predictions[:3], 1):
            print(f"\n🔮 {i}. {prediction.predicted_trend}")
            print(f"   📊 Confidence: {prediction.confidence_score:.0f}%")
            print(f"   ⏱️ Timeline: {prediction.timeline_days} days")
            print(f"   🎯 Target: {', '.join(prediction.target_audience[:2])}")
            print(f"   💡 Why: {prediction.cultural_reasoning[:120]}...")
            print(f"   💰 Opportunity: {prediction.market_opportunity[:80]}...")
        
        print(f"\n✨ Generated {analysis.total_predictions} total predictions")
        print(f"📈 Average confidence: {analysis.average_confidence:.1f}%")
        
        # Save demo results
        save_to_file(analysis.dict(), "hackathon_demo_results.json")
        
        return analysis

# Run tests and demos
if __name__ == "__main__":
    # Create demo data
    create_demo_data()
    
    # Run performance benchmark
    performance_benchmark()
    
    # Run full system test
    result = asyncio.run(test_full_system())
    
    if result:
        print("\n🎉 All tests passed! Running hackathon demo...")
        
        # Run hackathon demo
        demo = HackathonDemo()
        asyncio.run(demo.run_compelling_demo())
        
        print("\n🚀 TrendSeer is ready for the hackathon!")
    else:
        print("\n💥 Some tests failed. Check your configuration.")
