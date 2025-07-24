# chatbot_dashboard.py
import streamlit as st
import asyncio
from datetime import datetime
from services.trend_analyzer import TrendAnalyzer
from models.trend_models import UserPreferences
import json

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="TrendSeer Chatbot",
    page_icon="🔮",
    layout="wide"
)

# Initialize session state OUTSIDE of class
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm TrendSeer 🔮. I can predict emerging trends based on your cultural preferences. Let's start by learning about your tastes!"}
    ]

if "step" not in st.session_state:
    st.session_state.step = "greeting"

if "preferences" not in st.session_state:
    st.session_state.preferences = {
        "music_genres": [],
        "dining_preferences": [],
        "fashion_styles": [],
        "entertainment_types": [],
        "lifestyle_choices": []
    }

# Main app function
def main():
    """Main chatbot application"""
    
    st.title("🔮 TrendSeer Chatbot")
    st.caption("*Powered by Qloo Cultural Intelligence + Google Gemini LLM*")
    
    # Initialize analyzer
    if "analyzer" not in st.session_state:
        st.session_state.analyzer = TrendAnalyzer()
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Tell me about your preferences..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate and display bot response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your preferences..."):
                response = process_user_input(prompt)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

def process_user_input(user_input: str) -> str:
    """Process user input and return appropriate response"""
    
    current_step = st.session_state.step
    
    if current_step == "greeting":
        return ask_music_preferences()
    elif current_step == "music":
        return process_music_input(user_input)
    elif current_step == "dining":
        return process_dining_input(user_input)
    elif current_step == "fashion":
        return process_fashion_input(user_input)
    elif current_step == "entertainment":
        return process_entertainment_input(user_input)
    elif current_step == "lifestyle":
        return process_lifestyle_input(user_input)
    elif current_step == "analysis":
        return run_trend_analysis()
    else:
        return "I'm ready to help you discover new trends! What would you like to explore?"

def ask_music_preferences() -> str:
    """Ask about music preferences"""
    st.session_state.step = "music"
    return """🎵 **Let's start with music!** 

What genres do you enjoy? You can mention multiple genres like:
- Indie rock, folk, electronic
- Hip-hop, jazz, R&B  
- Classical, pop, country
- Or describe your taste in your own words!"""

def process_music_input(user_input: str) -> str:
    """Process music preferences"""
    genres = extract_preferences(user_input, "music")
    st.session_state.preferences["music_genres"] = genres
    st.session_state.step = "dining"
    
    return f"""Great! I see you enjoy: **{', '.join(genres)}** 🎶

🍽️ **Now, let's talk about food and dining!**

What are your dining preferences? Tell me about:
- Types of cuisine you love
- Dining styles (fine dining, street food, etc.)
- Drinks (coffee, cocktails, etc.)
- Any specific food values (organic, local, etc.)"""

def process_dining_input(user_input: str) -> str:
    """Process dining preferences"""
    dining_prefs = extract_preferences(user_input, "dining")
    st.session_state.preferences["dining_preferences"] = dining_prefs
    st.session_state.step = "fashion"
    
    return f"""Perfect! Your dining style: **{', '.join(dining_prefs)}** 🍽️

👔 **Let's explore your fashion sense!**

How would you describe your style? Consider:
- Aesthetic preferences (minimalist, vintage, modern)
- Values (sustainable, luxury, budget-friendly)
- Specific styles (streetwear, classic, bohemian)"""

def process_fashion_input(user_input: str) -> str:
    """Process fashion preferences"""
    fashion_styles = extract_preferences(user_input, "fashion")
    st.session_state.preferences["fashion_styles"] = fashion_styles
    st.session_state.step = "entertainment"
    
    return f"""Stylish! Your fashion vibe: **{', '.join(fashion_styles)}** 👔

🎬 **What about entertainment?**

How do you like to spend your free time? Think about:
- Movies/TV preferences
- Activities you enjoy
- Social preferences
- Hobbies and interests"""

def process_entertainment_input(user_input: str) -> str:
    """Process entertainment preferences"""
    entertainment = extract_preferences(user_input, "entertainment")
    st.session_state.preferences["entertainment_types"] = entertainment
    st.session_state.step = "lifestyle"
    
    return f"""Interesting! Your entertainment choices: **{', '.join(entertainment)}** 🎬

🏡 **Finally, tell me about your lifestyle!**

What values and lifestyle choices are important to you?
- Work style (remote, office, freelance)
- Life values (sustainability, wellness, productivity)
- Living preferences (urban, suburban, minimalist)"""

def process_lifestyle_input(user_input: str) -> str:
    """Process lifestyle preferences and trigger analysis"""
    lifestyle = extract_preferences(user_input, "lifestyle")
    st.session_state.preferences["lifestyle_choices"] = lifestyle
    st.session_state.step = "analysis"
    
    return f"""Perfect! Your lifestyle values: **{', '.join(lifestyle)}** 🏡"

## 📊 Your Complete Cultural Profile:
- 🎵 Music: {', '.join(st.session_state.preferences['music_genres'])}
- 🍽️ Dining: {', '.join(st.session_state.preferences['dining_preferences'])}
- 👔 Fashion: {', '.join(st.session_state.preferences['fashion_styles'])}
- 🎬 Entertainment: {', '.join(st.session_state.preferences['entertainment_types'])}
- 🏡 Lifestyle: {', '.join(st.session_state.preferences['lifestyle_choices'])}

🔮 **Now let me analyze your cultural DNA and predict emerging trends just for you!**

*Processing through Qloo's cultural intelligence and Gemini's AI...*"""

def extract_preferences(user_input: str, category: str) -> list:
    """Extract preferences from user input using keyword matching"""
    
    preference_maps = {
        "music": {
            "indie": "indie rock", "rock": "rock", "folk": "folk", "electronic": "electronic",
            "hip hop": "hip-hop", "hip-hop": "hip-hop", "rap": "hip-hop", "jazz": "jazz",
            "classical": "classical", "pop": "pop", "country": "country"
        },
        "dining": {
            "coffee": "artisanal coffee", "plant": "plant-based", "vegan": "plant-based",
            "local": "local sourcing", "organic": "organic", "street": "street food",
            "fine": "fine dining", "fusion": "fusion cuisine"
        },
        "fashion": {
            "vintage": "vintage", "minimal": "minimalist", "sustainable": "sustainable",
            "street": "streetwear", "luxury": "luxury brands", "classic": "classic"
        },
        "entertainment": {
            "indie": "indie films", "film": "indie films", "music": "live music",
            "podcast": "podcasts", "sport": "sports", "game": "gaming"
        },
        "lifestyle": {
            "sustain": "sustainable living", "wellness": "wellness", "remote": "remote work",
            "fitness": "fitness", "urban": "urban living", "travel": "travel"
        }
    }
    
    user_lower = user_input.lower()
    extracted = []
    
    for keyword, preference in preference_maps.get(category, {}).items():
        if keyword in user_lower:
            extracted.append(preference)
    
    # If no matches found, create from user words
    if not extracted:
        words = user_input.replace(",", "").split()
        extracted = [word.strip() for word in words if len(word.strip()) > 2][:3]
    
    return list(set(extracted))

def run_trend_analysis() -> str:
    """Run real trend analysis with user's preferences"""
    
    try:
        # Create UserPreferences object
        preferences = UserPreferences(
            music_genres=st.session_state.preferences["music_genres"],
            dining_preferences=st.session_state.preferences["dining_preferences"],
            fashion_styles=st.session_state.preferences["fashion_styles"],
            entertainment_types=st.session_state.preferences["entertainment_types"],
            lifestyle_choices=st.session_state.preferences["lifestyle_choices"]
        )
        
        # Run analysis
        analysis = asyncio.run(st.session_state.analyzer.predict_trends(preferences, "90d"))
        
        # Format results
        response = f"""🎯 **Your Personalized Trend Predictions** (Next 90 Days)

*Based on your unique cultural profile, here are {analysis.total_predictions} emerging trends I predict you'll be interested in:*

"""
        
        for i, prediction in enumerate(analysis.predictions[:3], 1):
            response += f"""
**{i}. {prediction.predicted_trend}**
📊 Confidence: {prediction.confidence_score:.0f}%
⏰ Timeline: {prediction.timeline_days} days
🎯 Perfect for: {', '.join(prediction.target_audience[:2])}
💡 Why this trend: {prediction.cultural_reasoning[:150]}...

---
"""
        
        response += f"""
📈 **Analysis Summary:**
- Average prediction confidence: {analysis.average_confidence:.1f}%
- Analysis powered by: Qloo Cultural Intelligence + Google Gemini

🔄 Want to explore more trends? Just ask!"""
        
        st.session_state.step = "complete"
        return response
        
    except Exception as e:
        return f"🚨 Sorry, I encountered an issue: {str(e)}. Let me try again!"

# Run the app
if __name__ == "__main__":
    main()
else:
    # This ensures main() runs when imported by Streamlit
    main()
