import streamlit as st
import os
import random
import asyncio
import base64
from datetime import datetime

# CRITICAL: Page config MUST be first
st.set_page_config(
    page_title="Cultrend AI - Cultural Intelligence",
    page_icon="https://i.ibb.co/qYZWLGqH/Plugin-icon-1-1.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import after page config
from models.trend_models import BrandIdentityKit, CulturalProfile, UserPreferences
from services.explanation_service import ExplanationService
from services.recommendation_service import RecommendationService
from content.content_data import popular_anime, travel_areas, football_clubs
from services.trend_analyzer import TrendAnalyzer

def get_api_keys():
    """Get API keys from Streamlit secrets"""
    qloo_key = st.secrets.get("qloo", {}).get("api_key")
    gemini_key = st.secrets.get("gemini", {}).get("api_key")
    
    if qloo_key and gemini_key:
        return qloo_key, gemini_key
    else:
        st.error("❌ API keys missing!")
        st.stop()

# Get API keys
qloo_key, gemini_key = get_api_keys()

# CSS Styles
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
.assistant-message { background-color: #f0ecf5; border-left: 6px solid #6a52c7; color: #3e2f75;}
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
.brand-kit-container { background-color: #ffffff; padding: 1.5rem; border-radius: 15px; border: 1px solid #ddd; margin-top: 1rem;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin-bottom: 0; color: #fff; font-size: 2.5rem;">Cultrend AI</h1>
    <p style="color: #fff; font-size: 1.1rem; margin: 0;">Your cultural friend: discover trends, brands, and experiences tailored just for you.</p>
</div>
""", unsafe_allow_html=True)

# Conversation data
friendly_openers = [
    "Hey there! How's your day going so far?",
    "Hi! It's nice to meet you. Have you done anything fun or interesting recently?",
    "Hello! If you could spend your afternoon any way you liked, what would you do?",
    "Hey! I always like starting with a friendly chat—what's something that's made you smile lately?"
]

smalltalk_questions = [
    "That sounds fun! By the way, do you gravitate more towards music, movies, books, or maybe something totally different?",
    "Love it. If you were to pick a favorite way to relax—music, games, travel, or anything—what would it be?",
    "Nice! Just out of curiosity, do you have a favorite artist, hobby, or trend lately?",
    "Beautiful! I always love hearing about what inspires people. Is there a genre, scene, or community you're drawn to these days?"
]

interest_prompt = "I'd love to learn about your cultural interests! What are some things you care about like music, fashion, travel, gaming, or something else?"

# BULLETPROOF SESSION STATE INITIALIZATION
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_stage" not in st.session_state:
    st.session_state.conversation_stage = "friend_talk"
if "smalltalk_turns" not in st.session_state:
    st.session_state.smalltalk_turns = 0
if "analyzer" not in st.session_state:
    st.session_state.analyzer = TrendAnalyzer()
if "last_cultural_profile" not in st.session_state:
    st.session_state.last_cultural_profile = None
if "show_brand_kit_prompt" not in st.session_state:
    st.session_state.show_brand_kit_prompt = False
if "recommendation_service" not in st.session_state:
    st.session_state.recommendation_service = RecommendationService()
if "explanation_service" not in st.session_state:
    st.session_state.explanation_service = ExplanationService()
if "input_key_counter" not in st.session_state:
    st.session_state.input_key_counter = 0

# CRITICAL: Loop prevention variables
if "processing_input" not in st.session_state:
    st.session_state.processing_input = False
if "last_processed_input" not in st.session_state:
    st.session_state.last_processed_input = ""
if "execution_count" not in st.session_state:
    st.session_state.execution_count = 0

# Initialize with friendly opener only once
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": random.choice(friendly_openers),
        "timestamp": datetime.now(),
        "type": "standard"
    })

# Helper functions
def get_cultrend_avatar_img():
    try:
        with open("cultrend_avatar.png", "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        return f'<img src="data:image/png;base64,{encoded}" width="32" style="vertical-align:middle;margin-right:4px;">'
    except FileNotFoundError:
        return "(•‿•) Cultrend"

def render_product_cards(items, content, timestamp):
    st.markdown(f'<div class="chat-message assistant-message"><strong>{get_cultrend_avatar_img()}</strong> <small>({timestamp.strftime("%H:%M")})</small><br>{content}</div>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, item in enumerate(items):
        with cols[idx % 3]:
            st.markdown(
                f"<img src='{item['image']}' style='height:350px;width:100%;object-fit:cover;border-radius:12px;margin-bottom:0.6rem;'>",
                unsafe_allow_html=True
            )
            st.markdown(f"<h4>{item['name']}</h4>", unsafe_allow_html=True)
            if item.get('price'):
                st.markdown(f"<p><b>{item['price']}</b></p>", unsafe_allow_html=True)
            if item.get("explanation"):
                with st.expander("✨ Why it's for you"):
                    for reason in item["explanation"].values():
                        st.markdown(f"- {reason}")
            st.link_button("🛒 Shop Now", item["link"], use_container_width=True)

def render_brand_kit(brand_kit: BrandIdentityKit):
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

def detect_specific_content(user_message: str):
    msg = user_message.lower()
    for key in popular_anime:
        if key in msg:
            return ("anime", key)
    for area in travel_areas:
        first_word = area["title"].split(",")[0].lower()
        if first_word in msg:
            return ("travel", area["title"])
    for key in football_clubs:
        if key in msg:
            return ("football", key)
    return (None, None)

def is_smalltalk(content: str) -> bool:
    smalltalk_keywords = ["day", "hello", "hi", "fine", "thanks", "good", "fun", "busy", "cool", "morning", "evening", "night", "weather", "smile", "chill"]
    return any(kw in content.lower() for kw in smalltalk_keywords)

def extract_user_preferences(messages):
    prefs_text = " ".join([msg["content"].lower() for msg in messages if msg["role"] == "user"])
    
    music_keywords = ["pop", "indie", "rock", "jazz", "classical", "electronic", "hip hop", "r&b", "folk", "country", "blues", "metal", "punk", "reggae", "soul", "funk", "disco", "house", "techno", "ambient"]
    fashion_keywords = ["minimalist", "vintage", "streetwear", "sustainable", "luxury", "casual", "formal", "bohemian", "preppy", "gothic", "punk", "athletic", "trendy", "classic", "avant-garde"]
    dining_keywords = ["local", "organic", "vegan", "vegetarian", "italian", "japanese", "chinese", "mexican", "indian", "thai", "french", "mediterranean", "artisanal", "craft", "farm-to-table", "street food", "fine dining"]
    entertainment_keywords = ["gaming", "movies", "music", "books", "art", "theater", "comedy", "podcasts", "streaming", "concerts", "festivals", "museums", "galleries", "sports", "outdoor", "travel"]
    lifestyle_keywords = ["gym","wellness", "fitness", "yoga", "meditation", "sustainability", "minimalism", "technology", "innovation", "entrepreneurship", "creativity", "community", "volunteering", "travel", "adventure", "learning"]
    
    music = {w for w in music_keywords if w in prefs_text}
    fashion = {w for w in fashion_keywords if w in prefs_text}
    dining = {w for w in dining_keywords if w in prefs_text}
    entertainment = {w for w in entertainment_keywords if w in prefs_text}
    lifestyle = {w for w in lifestyle_keywords if w in prefs_text}
    
    return UserPreferences(
        music_genres=list(music),
        fashion_styles=list(fashion),
        dining_preferences=list(dining),
        entertainment_types=list(entertainment),
        lifestyle_choices=list(lifestyle)
    )

# Chat History Renderer
for message in st.session_state.messages:
    if message.get("type") == "recommendation":
        render_product_cards(message["items"], message["content"], message.get("timestamp"))
        continue
        
    if message.get("type") == "brand_kit":
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>{get_cultrend_avatar_img()}</strong>
            <small>({message.get('timestamp').strftime('%H:%M') if message.get('timestamp') else ''})</small><br>
            {message['content']}
        </div>
        """, unsafe_allow_html=True)
        render_brand_kit(message["brand_kit"])
        continue
        
    role = message["role"]
    content = message["content"]
    timestamp = message.get("timestamp", datetime.now())
    msg_class = "user-message" if role == "user" else "assistant-message"
    avatar = "👤" if role == "user" else get_cultrend_avatar_img()
    st.markdown(f"""
    <div class="chat-message {msg_class}">
        <strong>{avatar} {'You' if role == 'user' else 'Cultrend'}</strong> <small>({timestamp.strftime('%H:%M')})</small><br>
        {content}
    </div>
    """, unsafe_allow_html=True)

# Brand kit generation button
if st.session_state.show_brand_kit_prompt:
    st.markdown("---")
    if st.button("✨ Generate My Brand DNA", use_container_width=True):
        if st.session_state.last_cultural_profile:
            with st.spinner("Crafting your personal brand identity..."):
                analyzer = st.session_state.analyzer
                brand_kit = asyncio.run(analyzer.generate_brand_identity(st.session_state.last_cultural_profile))
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Here's your personalized Brand Identity Kit based on your cultural DNA:",
                    "type": "brand_kit",
                    "brand_kit": brand_kit,
                    "timestamp": datetime.now()
                })
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "🎉 Your brand identity is ready! Type 'recommendations' to see personalized products that match your vibe!",
                    "timestamp": datetime.now(),
                    "type": "standard"
                })
                
            st.session_state.show_brand_kit_prompt = False
            st.session_state.conversation_stage = "post-brand-generation"
            st.rerun()

# BULLETPROOF CHAT INPUT - ZERO LOOP GUARANTEE
col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_input("Your message:", "",
        key="main_chat_input",
        label_visibility="collapsed"
    )
with col2:
    send_btn = st.button("✔️ Send")

# REVOLUTIONARY LOOP-PROOF INPUT PROCESSING
if (user_input and send_btn and 
    user_input.strip() != st.session_state.last_processed_input and 
    not st.session_state.processing_input):
    
    # Lock processing immediately
    st.session_state.processing_input = True
    st.session_state.last_processed_input = user_input.strip()
    st.session_state.execution_count += 1
    
    print(f"🚀 Processing execution #{st.session_state.execution_count}: '{user_input}'")
    
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now(),
        "type": "standard"
    })
    
    try:
        # Handle recommendations (highest priority)
        if any(keyword in user_input.lower() for keyword in ["recommend", "recommendations", "suggestion", "products"]):
            if st.session_state.last_cultural_profile:
                brand_kit = None
                for message in reversed(st.session_state.messages):
                    if message.get("type") == "brand_kit":
                        brand_kit = message.get("brand_kit")
                        break
                
                if brand_kit:
                    with st.spinner("Finding personalized recommendations..."):
                        recommendations = st.session_state.recommendation_service.get_personalized_recommendations(
                            st.session_state.last_cultural_profile, brand_kit, "products", 6
                        )
                        
                        if recommendations:
                            product_cards = []
                            for rec in recommendations:
                                explanation = st.session_state.explanation_service.get_recommendation_explanation(
                                    rec, st.session_state.last_cultural_profile, brand_kit
                                )
                                product_cards.append({
                                    "name": rec["name"], "image": rec["image"], "link": rec["link"],
                                    "price": rec.get("price", ""), "description": rec.get("description", ""),
                                    "explanation": explanation
                                })
                            
                            summary = st.session_state.recommendation_service.get_recommendation_summary(recommendations)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": f"<b>🛍️ Personalized Recommendations</b><br>{summary}",
                                "type": "recommendation", "items": product_cards, "timestamp": datetime.now()
                            })
                        else:
                            st.session_state.messages.append({
                                "role": "assistant", "content": "I couldn't find recommendations right now.",
                                "timestamp": datetime.now(), "type": "standard"
                            })
                else:
                    st.session_state.messages.append({
                        "role": "assistant", "content": "Please generate your brand identity first!",
                        "timestamp": datetime.now(), "type": "standard"
                    })
            else:
                st.session_state.messages.append({
                    "role": "assistant", "content": "I need to analyze your cultural DNA first.",
                    "timestamp": datetime.now(), "type": "standard"
                })
        
        # Handle brand kit requests
        elif any(keyword in user_input.lower() for keyword in ["brand", "kit", "identity"]):
            if st.session_state.last_cultural_profile:
                with st.spinner("Creating your brand identity..."):
                    analyzer = st.session_state.analyzer
                    brand_kit = asyncio.run(analyzer.generate_brand_identity(st.session_state.last_cultural_profile))
                    
                    st.session_state.messages.append({
                        "role": "assistant", "content": "Here's your personalized Brand Identity Kit:",
                        "type": "brand_kit", "brand_kit": brand_kit, "timestamp": datetime.now()
                    })
                    st.session_state.conversation_stage = "post-brand-generation"
                    st.session_state.show_brand_kit_prompt = False
            else:
                st.session_state.messages.append({
                    "role": "assistant", "content": "Please complete your cultural analysis first.",
                    "timestamp": datetime.now(), "type": "standard"
                })
        
        # Handle specific content
        else:
            category, key = detect_specific_content(user_input)
            if category:
                if category == "anime":
                    d = popular_anime[key]
                    st.session_state.messages.append({
                        "role": "assistant", "content": f"<b>{d['title']}</b><br>{d['desc']}",
                        "type": "recommendation", "items": d["products"], "timestamp": datetime.now()
                    })
                elif category == "travel":
                    d = next(area for area in travel_areas if area["title"] == key)
                    st.session_state.messages.append({
                        "role": "assistant", "content": f"<b>{d['title']}</b><br>{d['desc']}<br><a href='{d['flight_link']}' target='_blank'>Find Flights</a>",
                        "type": "standard", "timestamp": datetime.now()
                    })
                elif category == "football":
                    d = football_clubs[key]
                    st.session_state.messages.append({
                        "role": "assistant", "content": f"<b>{d['title']}</b><br>{d['desc']}",
                        "type": "recommendation", "items": d["products"], "timestamp": datetime.now()
                    })
            
            # Handle conversation stages
            else:
                if st.session_state.conversation_stage == "friend_talk":
                    st.session_state.smalltalk_turns += 1
                    if is_smalltalk(user_input) and st.session_state.smalltalk_turns < 2:
                        st.session_state.messages.append({
                            "role": "assistant", "content": random.choice(smalltalk_questions),
                            "timestamp": datetime.now(), "type": "standard"
                        })
                    else:
                        st.session_state.messages.append({
                            "role": "assistant", "content": interest_prompt,
                            "timestamp": datetime.now(), "type": "standard"
                        })
                        st.session_state.conversation_stage = "collecting"

                elif st.session_state.conversation_stage == "collecting":
                    history_len = len([m for m in st.session_state.messages if m["role"] == "user"])
                    
                    if "analyze" in user_input.lower() or history_len >= 3:
                        prefs = extract_user_preferences(st.session_state.messages)
                        
                        with st.spinner("Analyzing your cultural DNA..."):
                            analyzer = st.session_state.analyzer
                            analysis = asyncio.run(analyzer.predict_trends(prefs, "90d"))
                            profile = getattr(analysis, 'cultural_profile', None)
                        
                        if profile and getattr(profile, 'cultural_segments', None):
                            st.session_state.last_cultural_profile = profile
                            
                            resp_lines = ["Here's what I've learned about your trend vibe!\n"]
                            resp_lines.append(f"**Your Cultural Segments:** {', '.join(profile.cultural_segments)}")
                            for i, pred in enumerate(analysis.predictions[:3], 1):
                                resp_lines.append(f"{i}. {pred.predicted_trend} (Confidence: {pred.confidence_score:.0f}%)")
                            resp_lines.append("\nReady to create your Brand DNA? Click the button below!")
                            
                            st.session_state.messages.append({
                                "role": "assistant", "content": "\n".join(resp_lines),
                                "timestamp": datetime.now(), "type": "standard"
                            })
                            
                            st.session_state.show_brand_kit_prompt = True
                            st.session_state.conversation_stage = "post-analysis"
                        else:
                            st.session_state.messages.append({
                                "role": "assistant", "content": "Could you tell me more about your interests?",
                                "timestamp": datetime.now(), "type": "standard"
                            })
                    else:
                        st.session_state.messages.append({
                            "role": "assistant", "content": "Tell me more about your interests, or type 'analyze' when ready!",
                            "timestamp": datetime.now(), "type": "standard"
                        })
                
                # GENIUS: Only respond to specific inputs
                elif st.session_state.conversation_stage in ["post-analysis", "post-brand-generation"]:
                    if user_input.lower().strip() in ["hey", "hi", "hello", "help"]:
                        response = ("Hey! Your analysis is ready. Generate your Brand DNA below!" 
                                 if st.session_state.conversation_stage == "post-analysis" 
                                 else "Hey! Ready for recommendations? Just type 'recommendations'!")
                        st.session_state.messages.append({
                            "role": "assistant", "content": response,
                            "timestamp": datetime.now(), "type": "standard"
                        })
                    # Ignore all other inputs to prevent loops
        
        print(f"✅ Execution #{st.session_state.execution_count} completed successfully")
        
    except Exception as e:
        print(f"❌ Error in execution #{st.session_state.execution_count}: {e}")
        st.session_state.messages.append({
            "role": "assistant", "content": "Sorry, I encountered an error. Please try again!",
            "timestamp": datetime.now(), "type": "standard"
        })
    
    finally:
        # Always unlock processing
        st.session_state.processing_input = False
        print(f"🔄 Triggering rerun after execution #{st.session_state.execution_count}")
        st.rerun()
