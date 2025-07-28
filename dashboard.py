import streamlit as st
from datetime import datetime
import random
import asyncio
from models.trend_models import BrandIdentityKit, CulturalProfile  # Updated import

# Import your content data (make sure content_data.py is in the same directory)
from content.content_data import popular_anime, travel_areas, football_clubs

from services.trend_analyzer import TrendAnalyzer  # your actual analyzer
from models.trend_models import UserPreferences    # adjust import as needed

st.set_page_config(page_title="Cultrend AI", layout="wide")

# --- UI Styles ---
st.markdown("""
<style>
.main-header { background: linear-gradient(90deg, #5a4e9e 0%, #7f5fc5 100%);
    padding: 1rem; border-radius: 12px; color: #f0f0f5; text-align: center;
    margin-bottom: 2.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    box-shadow: 0 4px 12px rgba(95, 78, 178, 0.6); }
.chat-message { padding: 1rem; border-radius: 14px; margin: 0.5rem 0; animation: fadeIn 0.4s;
    font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.45;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);}
.user-message { background-color: #d9e7ff; border-left: 6px solid #1a73e8; color: #003366;}
.assistant-message { background-color: #ede7f6; border-left: 6px solid #6a52c7; color: #3e2f75;}
@keyframes fadeIn { from { opacity: 0; transform: translateY(12px);} to{ opacity:1; transform: translateY(0);}}
.mini-product-card {
    background: #fff; border-radius: 12px; box-shadow: 0 6px 15px rgba(121,94,194, 0.15);
    display: flex; align-items: center; padding: 10px 12px; margin-bottom: 10px;
    width: 360px; max-width: 100%; border: 1px solid #ccc4f6; transition: box-shadow 0.25s, transform 0.25s; cursor: pointer;}
.mini-product-card:hover { box-shadow: 0 12px 28px rgba(101,78,190,0.3); transform: translateY(-4px);}
.mini-product-img { border-radius: 8px; width: 60px; height: 60px; object-fit: cover; box-shadow: 0 2px 6px rgba(74,55,157,0.3);}
.mini-product-txt {margin-left: 16px; flex: 1; color: #4b3f85; font-weight: 600;}
.mini-product-btn { background: linear-gradient(90deg, #5c4dbc, #7f5fc5); color: #fff; font-weight: 700;
    border-radius: 20px; padding: 6px 18px; text-decoration: none; font-size: 1em; margin-top: 3px; margin-left: 12px; display: inline-block;
    box-shadow: 0 3px 8px rgba(133,109,209,0.4); transition: background 0.3s;}
.mini-product-btn:hover { background: linear-gradient(90deg, #7f5fc5, #5c4dbc); box-shadow: 0 5px 15px rgba(133,109,209,0.7);}
.recommend-card-row { display: flex; flex-wrap: wrap; gap: 18px; margin-bottom: 14px; justify-content: flex-start;}
.brand-kit-container { background-color: #ffffff; padding: 1.5rem; border-radius: 15px; border: 1px solid #ddd; margin-top: 1rem;}
@media (max-width: 700px){
    .recommend-card-row { flex-direction: column; gap: 12px;}
    .mini-product-card { width: 100% !important; min-width:unset !important; margin-left:0 !important;}
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1> Cultrend AI</h1>
    <p>Your cultural friend: discover trends, brands, and experiences tailored just for you.</p>
</div>
""", unsafe_allow_html=True)

# ----- Friendly opening, small talk logic -----
friendly_openers = [
    "Hey there! 👋 How's your day going so far?",
    "Hi! It's nice to meet you. Have you done anything fun or interesting recently?",
    "Hello! 😃 If you could spend your afternoon any way you liked, what would you do?",
    "Hey! I always like starting with a friendly chat—what's something that's made you smile lately?"
]
smalltalk_questions = [
    "That sounds fun! By the way, do you gravitate more towards music, movies, books, or maybe something totally different?",
    "Love it. If you were to pick a favorite way to relax—music, games, travel, or anything—what would it be?",
    "Nice! Just out of curiosity, do you have a favorite artist, hobby, or trend lately?",
    "Beautiful! I always love hearing about what inspires people. Is there a genre, scene, or community you're drawn to these days?"
]
interest_prompt = "I'd love to learn about your cultural interests! What are some things you care about—like music, fashion, travel, gaming, or something else?"

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_stage" not in st.session_state:
    st.session_state.conversation_stage = "friend_talk"
if "smalltalk_turns" not in st.session_state:
    st.session_state.smalltalk_turns = 0
if "analyzer" not in st.session_state:
    st.session_state.analyzer = TrendAnalyzer()
if "recommendations_unlocked" not in st.session_state:
    st.session_state.recommendations_unlocked = False
# ADDED: Brand kit session state variables
if "last_cultural_profile" not in st.session_state:
    st.session_state.last_cultural_profile = None
if "show_brand_kit_prompt" not in st.session_state:
    st.session_state.show_brand_kit_prompt = False

if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": random.choice(friendly_openers),
        "timestamp": datetime.now(),
        "type": "standard"
    })

def render_product_cards(items, content, timestamp):
    st.markdown(f"""
        <div class="chat-message assistant-message" style="margin-bottom:0.5rem;">
            <strong>🤖 Cultrend</strong>
            <small>({timestamp.strftime('%H:%M') if timestamp else ''})</small><br>
            {content}
            <div class="recommend-card-row">
    """, unsafe_allow_html=True)

    for item in items:
        st.markdown(f"""
            <div class="mini-product-card" tabindex="0" role="button" aria-label="{item['name']}">
                <img src="{item['image']}" class="mini-product-img" alt="{item['name']} image" />
                <div class="mini-product-txt">{item['name']}</div>
                <a class="mini-product-btn" href="{item['link']}" target="_blank" rel="noopener noreferrer" aria-label="Shop {item['name']}">🛒 Shop</a>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

# --- ADDED: Function to render brand identity kit ---
def render_brand_kit(brand_kit: BrandIdentityKit):
    """Renders the BrandIdentityKit in a structured, visually appealing card"""
    st.markdown("### 🎨 Your Personal Brand Identity Kit")
    st.markdown(f"#### {brand_kit.brand_name}")
    st.markdown(f"> *{brand_kit.tagline}*")
    
    st.markdown("**Mission Statement**")
    st.write(brand_kit.mission_statement)
    
    st.markdown("**Core Keywords**")
    st.write(" | ".join([f"`{kw}`" for kw in brand_kit.core_keywords]))

    st.markdown("**Social Media Bio**")
    st.info(brand_kit.social_media_bio)
    
    st.markdown("**Color Palette**")
    cols = st.columns(len(brand_kit.color_palette))
    for i, (name, color) in enumerate(brand_kit.color_palette.items()):
        with cols[i]:
            st.color_picker(f"{name.replace('_', ' ').title()}", value=color, key=f"color_{name}", disabled=True)

# --- Content Detection Logic ---
def detect_specific_content(user_message: str):
    msg = user_message.lower()

    # Anime title
    for key in popular_anime:
        if key in msg:
            return ("anime", key)
    # Travel destination (search by first word in "title")
    for area in travel_areas:
        first_word = area["title"].split(",")[0].lower()
        if first_word in msg:
            return ("travel", area["title"])
    # Football club
    for key in football_clubs:
        if key in msg:
            return ("football", key)
    return (None, None)

# --- Chat History Renderer ---
for message in st.session_state.messages:
    # Handle recommendation messages
    if message.get("type") == "recommendation":
        render_product_cards(message["items"], message["content"], message.get("timestamp"))
        continue
        
    # ADDED: Handle brand kit messages
    if message.get("type") == "brand_kit":
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 Cultrend</strong>
            <small>({message.get('timestamp').strftime('%H:%M') if message.get('timestamp') else ''})</small><br>
            {message['content']}
        </div>
        """, unsafe_allow_html=True)
        render_brand_kit(message["brand_kit"])
        continue
        
    # Handle standard messages
    role = message["role"]
    content = message["content"]
    timestamp = message.get("timestamp", datetime.now())
    msg_class = "user-message" if role == "user" else "assistant-message"
    avatar = "🧑" if role == "user" else "🤖"
    st.markdown(f"""
    <div class="chat-message {msg_class}">
        <strong>{avatar} {'You' if role == 'user' else 'Cultrend'}</strong> <small>({timestamp.strftime('%H:%M')})</small><br>
        {content}
    </div>
    """, unsafe_allow_html=True)

# ADDED: Brand kit generation button after message rendering
if st.session_state.show_brand_kit_prompt:
    st.markdown("---")
    if st.button("✨ Generate My Brand DNA", use_container_width=True):
        if st.session_state.last_cultural_profile:
            with st.spinner("Crafting your personal brand identity..."):
                analyzer = st.session_state.analyzer
                brand_kit = asyncio.run(analyzer.generate_brand_identity(
                    st.session_state.last_cultural_profile
                ))
                
                # Add brand kit to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Here's your personalized Brand Identity Kit based on your cultural DNA:",
                    "type": "brand_kit",
                    "brand_kit": brand_kit,
                    "timestamp": datetime.now()
                })
                
            st.session_state.show_brand_kit_prompt = False
            st.rerun()
        else:
            st.error("Couldn't find your cultural profile. Please try analyzing again.")
            st.session_state.show_brand_kit_prompt = False

col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_input("Your message:", "",
        key=f"chat_input_{len(st.session_state.messages)}",
        placeholder="Say something friendly, mention an anime, travel place, or football club!",
        label_visibility="collapsed"
    )
with col2:
    send_btn = st.button("📤 Send", type="primary")

def is_smalltalk(content: str) -> bool:
    smalltalk_keywords = ["day", "hello", "hi", "fine", "thanks", "good", "fun", "busy", "cool", "morning", "evening", "night", "weather", "smile", "chill"]
    return any(kw in content.lower() for kw in smalltalk_keywords)

def extract_user_preferences(messages):
    """Enhanced preference extraction with broader keyword coverage"""
    prefs_text = " ".join([msg["content"].lower() for msg in messages if msg["role"] == "user"])
    
    # Expanded keyword sets
    music_keywords = ["pop", "indie", "rock", "jazz", "classical", "electronic", "hip hop", "r&b", "folk", "country", "blues", "metal", "punk", "reggae", "soul", "funk", "disco", "house", "techno", "ambient"]
    fashion_keywords = ["minimalist", "vintage", "streetwear", "sustainable", "luxury", "casual", "formal", "bohemian", "preppy", "gothic", "punk", "athletic", "trendy", "classic", "avant-garde"]
    dining_keywords = ["local", "organic", "vegan", "vegetarian", "italian", "japanese", "chinese", "mexican", "indian", "thai", "french", "mediterranean", "artisanal", "craft", "farm-to-table", "street food", "fine dining"]
    entertainment_keywords = ["gaming", "movies", "music", "books", "art", "theater", "comedy", "podcasts", "streaming", "concerts", "festivals", "museums", "galleries", "sports", "outdoor", "travel"]
    lifestyle_keywords = ["wellness", "fitness", "yoga", "meditation", "sustainability", "minimalism", "technology", "innovation", "entrepreneurship", "creativity", "community", "volunteering", "travel", "adventure", "learning"]
    
    # Extract matches
    music = {w for w in music_keywords if w in prefs_text}
    fashion = {w for w in fashion_keywords if w in prefs_text}
    dining = {w for w in dining_keywords if w in prefs_text}
    entertainment = {w for w in entertainment_keywords if w in prefs_text}
    lifestyle = {w for w in lifestyle_keywords if w in prefs_text}
    # 🔍 ADD INPUT CHECK HERE
    print(f"🔍 INPUT CHECK - Extracted preferences:")
    print(f"   🎵 Music: {list(music)}")
    print(f"   👔 Fashion: {list(fashion)}")
    print(f"   🍽️ Dining: {list(dining)}")
    print(f"   🎬 Entertainment: {list(entertainment)}")
    print(f"   🏡 Lifestyle: {list(lifestyle)}")
    
    
    return UserPreferences(
        music_genres=list(music),
        fashion_styles=list(fashion),
        dining_preferences=list(dining),
        entertainment_types=list(entertainment),
        lifestyle_choices=list(lifestyle)
    )


# --- Main Chat Logic with brand kit integration ---
if user_input and send_btn:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now(),
        "type": "standard"
    })

    # Detect and respond to anime/travel/football queries first
    category, key = detect_specific_content(user_input)
    if category == "anime":
        d = popular_anime[key]
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"<b>{d['title']}</b><br>{d['desc']}",
            "type": "recommendation",
            "items": d["products"],
            "timestamp": datetime.now()
        })
        st.rerun()
    elif category == "travel":
        d = next(area for area in travel_areas if area["title"] == key)
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"<b>{d['title']}</b><br>{d['desc']}<br><a href='{d['flight_link']}' target='_blank'>Find Flights</a>",
            "type": "standard",
            "timestamp": datetime.now()
        })
        st.rerun()
    elif category == "football":
        d = football_clubs[key]
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"<b>{d['title']}</b><br>{d['desc']}",
            "type": "recommendation",
            "items": d["products"],
            "timestamp": datetime.now()
        })
        st.rerun()
    else:
        # ---- Friend talk and profile logic ----
        if st.session_state.conversation_stage == "friend_talk":
            st.session_state.smalltalk_turns += 1
            # Continue small talk
            if is_smalltalk(user_input) and st.session_state.smalltalk_turns < 2:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": random.choice(smalltalk_questions),
                    "timestamp": datetime.now(),
                    "type": "standard"
                })
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": interest_prompt,
                    "timestamp": datetime.now(),
                    "type": "standard"
                })
                st.session_state.conversation_stage = "collecting"
            st.rerun()

        elif st.session_state.conversation_stage == "collecting":
            # Natural interest collection for 2+ interactions, then analyze
            history_len = len([m for m in st.session_state.messages if m["role"] == "user"])
            
            # Trigger analysis with "analyze" keyword or after 3 interactions
            if "analyze" in user_input.lower() or history_len >= 3:
                prefs = extract_user_preferences(st.session_state.messages)
                
                # Initialize profile as None
                profile = None
                
                with st.spinner("Analyzing your cultural DNA..."):
                    analyzer = st.session_state.analyzer
                    try:
                        # Call your Qloo+Gemini pipeline
                        analysis = asyncio.run(analyzer.predict_trends(prefs, "90d"))
                        
                        # Safely get the profile from the result
                        if hasattr(analysis, 'cultural_profile') and analysis.cultural_profile:
                            profile = analysis.cultural_profile
                        else:
                            # Handle case where analysis object IS the profile
                            profile = analysis
                            
                    except Exception as e:
                        print(f"Error during analysis: {e}")
                        # If the analysis service fails, profile remains None

                # --- Enhanced profile validation ---
                valid_profile = False
                segments = []
                
                if profile:
                    # Check for cultural segments with different naming conventions
                    if hasattr(profile, 'cultural_segments') and profile.cultural_segments:
                        segments = profile.cultural_segments
                        valid_profile = True
                    elif hasattr(profile, 'enhanced_cultural_segments') and profile.enhanced_cultural_segments:
                        segments = profile.enhanced_cultural_segments
                        valid_profile = True
                    elif hasattr(profile, 'segments') and profile.segments:
                        segments = profile.segments
                        valid_profile = True
                
                if valid_profile:
                    st.session_state.last_cultural_profile = profile
                   
                    
                    # Check 1: Verify API connection
                    qloo_service = st.session_state.analyzer.qloo_service
                    api_status = asyncio.run(qloo_service._test_api_connection())
                    st.write(f"**API Connection:** {'✅ Working' if api_status else '❌ Failed'}")
                    
                    # Check 2: Verify data sources
                    connections = profile.cross_domain_connections
                    data_sources = connections.get('data_sources', [])
                    st.write(f"**Data Sources Used:** {data_sources}")
                    
                    # Check 3: Show raw entity counts
                    st.write(f"**Brand Entities:** {len(connections.get('brands', []))}")
                    st.write(f"**Artist Entities:** {len(connections.get('artists', []))}")
                    st.write(f"**Cultural Segments:** {profile.cultural_segments}")
                    
                    # Check 4: Performance metrics
                    metrics = qloo_service.get_performance_metrics()
                    st.write(f"**Service Metrics:** {metrics}")
                    # Build success message with trend predictions
                    resp_lines = []
                    resp_lines.append("Here's what I've learned about your trend vibe!\n")
                    resp_lines.append(f"Average Confidence: {getattr(analysis, 'average_confidence', 0):.1f}%")
                    resp_lines.append(f"Timeframe: {getattr(analysis, 'timeframe', '90d')}")
                    resp_lines.append("")
                    resp_lines.append("Top Trends")
                    resp_lines.append("")
                    
                    for i, pred in enumerate(analysis.predictions, 1):
                        resp_lines.append(f"{i}. {pred.predicted_trend}")
                        resp_lines.append(f"   - Category: {pred.product_category}")
                        resp_lines.append(f"   - Confidence: {pred.confidence_score:.0f}%")
                        resp_lines.append(f"   - Timeline: {pred.timeline_days:.0f} days")
                        resp_lines.append(f"   - Target Audience: {', '.join(pred.target_audience)}")
                        reason = getattr(pred, 'cultural_reasoning', '')
                        if reason:
                            resp_lines.append(f"   - Reason: {reason[:200].rstrip()}")
                        resp_lines.append("")
                    
                    # Add cultural segments info
                    resp_lines.append(f"**Your Cultural Segments:** {', '.join(segments)}")
                    
                    # Add BRAND KIT PROMPT
                    resp_lines.append("Would you like some recommendations for products or experiences that match your vibe?")
                    
                    
                    resp = "\n".join(resp_lines)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": resp,
                        "timestamp": datetime.now(),
                        "type": "standard"
                    })
                    
                    # SHOW BRAND KIT BUTTON PROMPT
                    st.session_state.show_brand_kit_prompt = True
                    st.session_state.conversation_stage = "post-analysis"
                    st.rerun()
                    
                else:
                    # If profile creation failed, ask for more info
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "I had a little trouble building a full cultural profile from those preferences. Could you tell me more about your favorite music, fashion styles, or hobbies? The more details, the better!",
                        "timestamp": datetime.now(),
                        "type": "standard"
                    })
                    # DEBUG: Print error details to console
                    print("⚠️ Cultural profile creation failed despite trend prediction")
                    print(f"Profile object exists: {profile is not None}")
                    if profile:
                        print(f"Profile attributes: {dir(profile)}")
                    # Keep stage as "collecting" to allow more input
                    st.rerun()
                    
            else:
                # Continue collecting preferences
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": random.choice([
                        "That's awesome! Tell me another thing you enjoy. The more I learn, the more personal my trend predictions get!",
                        "I love your energy! Shall we keep exploring your interests? Share more or type 'analyze' if you want me to analyze your profile."
                    ]),
                    "timestamp": datetime.now(),
                    "type": "standard"
                })
                st.rerun()

        elif st.session_state.conversation_stage == "post-analysis":
            # Handle brand kit request
            if "brand" in user_input.lower() or "kit" in user_input.lower() or "identity" in user_input.lower():
                if st.session_state.last_cultural_profile:
                    with st.spinner("Crafting your personal brand identity..."):
                        analyzer = st.session_state.analyzer
                        brand_kit = asyncio.run(analyzer.generate_brand_identity(
                            st.session_state.last_cultural_profile
                        ))
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "Here's your personalized Brand Identity Kit based on your cultural DNA:",
                            "type": "brand_kit",
                            "brand_kit": brand_kit,
                            "timestamp": datetime.now()
                        })
                    st.session_state.show_brand_kit_prompt = False
                    st.rerun()
                else:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Sorry, I couldn't find your cultural profile. Please try analyzing again.",
                        "timestamp": datetime.now(),
                        "type": "standard"
                    })
                    st.rerun()
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Love the conversation! Type any anime, travel, or football club for custom picks.",
                    "timestamp": datetime.now(),
                    "type": "standard"
                })
                st.rerun()