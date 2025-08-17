# Cultrend AI Dashboard

An interactive Streamlit application for cultural trend discovery, personalized recommendations, and user brand identity generation.

---

##  Features

- Friendly conversational chat interface
- Cultural DNA analysis based on user preferences
- Personalized trend predictions (details: category, confidence, timeline, audience, reasons)
- Brand Identity kit generation
- Recommendations: products, experiences
- Anime, travel, and sports integration
- Responsive UI (mobile-friendly)

---

## Installation

git clone https://github.com/yourusername/cultrend-ai.git
cd cultrend-ai
pip install -r requirements.txt

text

---

## ⚙️ Usage

1. **Set API Keys**  
   Save credentials in `.streamlit/secrets.toml`:
[qloo]
api_key = "YOUR_QLOO_API_KEY"

[gemini]
api_key = "YOUR_GEMINI_API_KEY"

text

2. **Run the Dashboard**
streamlit run dashboard.py

text

3. **Interacting**
- First AI message is a friendly opener
- Submit your cultural interests/preferences
- Click _"Generate My Brand DNA"_ for your personal kit
- Ask for recommendations or mention anime, football, or travel

---

##  Folder Structure

cultrend-ai/
├── dashboard.py
├── models/
├── services/
├── content/
├── static/
├── requirements.txt
└── .streamlit/

text

---

## Customization

- Modify `content_data.py` to add more anime, travel, sports, etc.
- Tweak trend prediction logic in `services/trend_analyzer.py`

---

## Technologies

- Python 3.8+
- Streamlit
- Qloo API
- Gemini API



##  Contributing

- Fork the repo and submit a pull request!
- Follow [Streamlit best practices](https://docs.streamlit.io)
- Code is clean, readable, and heavily commented

---

**[Repository Link](https://github.com/yourusername/cultrend-ai)**
