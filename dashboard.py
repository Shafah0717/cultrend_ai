import streamlit as st
from datetime import datetime
import random
import asyncio

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
    if message.get("type") == "recommendation":
        render_product_cards(message["items"], message["content"], message.get("timestamp"))
        continue
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
    music_keywords = ["pop", "indie", "k-pop", "j-pop", "rock", "alternative", "electronic", "edm", "techno", "trance",
    "house", "hip hop", "rap", "classical", "jazz", "blues", "r&b", "soul", "metal", "punk", "folk", 
    "acoustic", "country", "reggaeton", "disco", "lo-fi", "soundtrack", "instrumental", "band",
    "artist", "singer", "concert", "playlist", "dance", "trap"]
    fashion_keywords = ["minimalist", "vintage", "streetwear", "thrift", "luxury", "sustainable", "boho", "casual", "formal", 
    "chic", "retro", "hipster", "athleisure", "preppy", "avant-garde", "couture", "designer", "branded",
    "sportswear", "blazer", "jeans", "sneakers", "denim", "dress", "hoodie", "jacket", "t-shirt", 
    "accessories", "jewelry", "watches", "purse", "bag", "fashionista", "runway", "lookbook", "capsule", "outfit"]
    dining_keywords = ["local", "italian", "japanese", "fusion", "vegan", "artisanal", "coffee", "food", "sushi", "global", "street food", "baking", "fine dining", "brunch"]
    entertainment_keywords = ["gaming", "movies", "art", "anime", "theater", "music", "books", "esports", "film", "documentaries", "standup", "tv series", "podcasts"]
    lifestyle_keywords = ["travel", "tourism", "adventure", "remote work", "digital nomad", "staycation", "road trip", 
    "vacation", "working from home", "expat", "backpacking", "trip", "journey", "flight", "wanderlust",
    "bucket list", "hiking", "camping", "outdoors", "eco-friendly", "sustainability", "zero waste", 
    "wellness", "yoga", "mindfulness", "meditation", "self care", "gym", "workout", "fitness", "sports",
    "running", "cycling", "walking", "volunteering", "charity", "social impact", "productivity", 
    "startup", "entrepreneurship", "innovation", "tech", "gadgets", "creative", "art", "photography", 
    "journaling", "reading", "pet", "family", "gardening"]
    music, fashion, dining, entertainment, lifestyle = set(), set(), set(), set(), set()
    for msg in messages:
        if msg["role"] == "user":
            text = msg["content"].lower()
            for kw in music_keywords:
                if kw in text: music.add(kw)
            for kw in fashion_keywords:
                if kw in text: fashion.add(kw)
            for kw in dining_keywords:
                if kw in text: dining.add(kw)
            for kw in entertainment_keywords:
                if kw in text: entertainment.add(kw)
            for kw in lifestyle_keywords:
                if kw in text: lifestyle.add(kw)
    return UserPreferences(
        music_genres=list(music),
        dining_preferences=list(dining),
        fashion_styles=list(fashion),
        entertainment_types=list(entertainment),
        lifestyle_choices=list(lifestyle)
    )

# --- Main Chat Logic with new content integration ---
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
        # ---- Friend talk and profile logic as before ----
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
            if history_len >= 3:
                prefs = extract_user_preferences(st.session_state.messages)
                with st.spinner("Thinking about your unique trend profile..."):
                    analyzer = st.session_state.analyzer
                    analysis = asyncio.run(analyzer.predict_trends(prefs, "90d"))
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
                resp_lines.append("Would you like some recommendations for products or experiences that match your vibe? Just tell me a passion, place, or club!")
                resp = "\n".join(resp_lines)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": resp,
                    "timestamp": datetime.now(),
                    "type": "standard"
                })
                st.session_state.conversation_stage = "post-analysis"
                st.session_state.recommendations_unlocked = True
                st.rerun()
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": random.choice([
                        "That's awesome! Tell me another thing you enjoy. The more I learn, the more personal my trend predictions get!",
                        "Cool, anything else you love? Feel free to talk about music, style, travel, or whatever inspires you.",
                        "I love your energy! Shall we keep exploring your interests? Share more or type 'ready' if you want my analysis."
                    ]),
                    "timestamp": datetime.now(),
                    "type": "standard"
                })
                st.rerun()
        elif st.session_state.conversation_stage == "post-analysis":
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Love the conversation! Type any anime, destination, or club for custom picks, or share more about your tastes.",
                "timestamp": datetime.now(),
                "type": "standard"
            })
            st.rerun()
