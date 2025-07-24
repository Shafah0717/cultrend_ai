# dashboard.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import asyncio
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="TrendSeer Dashboard",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

class TrendSeerDashboard:
    """Main dashboard application"""
    
    def __init__(self):
        self.api_base_url = "http://localhost:8000"
    
    def run(self):
        """Main dashboard application"""
        
        # Custom CSS for better styling
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1rem;
        }
        .gemini-badge {
            background: linear-gradient(45deg, #4285f4, #34a853, #fbbc05, #ea4335);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            text-align: center;
            margin: 1rem 0;
        }
        .trend-card {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
            margin: 0.5rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Main header
        st.markdown('<h1 class="main-header">🔮 TrendSeer</h1>', unsafe_allow_html=True)
        st.markdown('<div class="gemini-badge">Powered by Google Gemini LLM 🤖</div>', unsafe_allow_html=True)
        st.markdown("*Predict the next big trends with cultural intelligence and advanced AI*")
        
        # Sidebar configuration
        self._setup_sidebar()
        
        # Main content area
        if st.session_state.get('analysis_results'):
            self._display_results()
        else:
            self._display_input_form()
    
    def _setup_sidebar(self):
        """Setup sidebar with controls and information"""
        
        st.sidebar.title("🎯 Analysis Settings")
        st.sidebar.caption("Powered by Google Gemini 🤖")
        
        # Timeframe selection
        st.session_state['timeframe'] = st.sidebar.selectbox(
            "Prediction Timeframe",
            ["30d", "90d", "180d"],
            index=1,  # Default to 90d
            help="How far into the future to predict trends"
        )
        
        # Sample data options
        st.sidebar.markdown("### 📁 Quick Start")
        
        sample_types = {
            "Indie Culture Enthusiast": {
                "music_genres": ["indie rock", "folk", "electronic"],
                "dining_prefs": ["artisanal coffee", "plant-based", "local sourcing"],
                "fashion_styles": ["minimalist", "sustainable", "vintage"],
                "entertainment": ["indie films", "live music", "podcasts"],
                "lifestyle": ["sustainable living", "wellness", "remote work"]
            },
            "Urban Trendsetter": {
                "music_genres": ["hip-hop", "jazz", "R&B"],
                "dining_prefs": ["street food", "fusion cuisine", "craft cocktails"],
                "fashion_styles": ["streetwear", "luxury brands", "sneakers"],
                "entertainment": ["sports", "gaming", "social media"],
                "lifestyle": ["fitness", "urban living", "nightlife"]
            },
            "Luxury Connoisseur": {
                "music_genres": ["classical", "ambient", "new age"],
                "dining_prefs": ["fine dining", "wine pairing", "molecular gastronomy"],
                "fashion_styles": ["luxury", "classic", "designer"],
                "entertainment": ["opera", "art galleries", "theater"],
                "lifestyle": ["luxury travel", "collecting", "cultural events"]
            }
        }
        
        selected_sample = st.sidebar.selectbox(
            "Load Sample Profile:",
            ["Select a sample..."] + list(sample_types.keys())
        )
        
        if st.sidebar.button("Load Sample") and selected_sample != "Select a sample...":
            self._load_sample_preferences(sample_types[selected_sample])
        
        # Clear results
        if st.sidebar.button("Clear Results"):
            st.session_state['analysis_results'] = None
            st.rerun()
        
        # API status
        st.sidebar.markdown("---")
        st.sidebar.markdown("**System Status**")
        try:
            response = requests.get(f"{self.api_base_url}/health", timeout=5)
            if response.status_code == 200:
                st.sidebar.success("🟢 All Systems Online")
                health_data = response.json()
                if health_data.get('services'):
                    for service, status in health_data['services'].items():
                        emoji = "🟢" if status == "healthy" else "🔴"
                        st.sidebar.text(f"{emoji} {service.replace('_', ' ').title()}")
            else:
                st.sidebar.error("🔴 API Issues")
        except:
            st.sidebar.error("🔴 API Offline")
        
        # Info section
        st.sidebar.markdown("---")
        st.sidebar.markdown("**About TrendSeer**")
        st.sidebar.info(
            "TrendSeer uses Qloo's cultural intelligence API combined with Google Gemini LLM to predict emerging trends 3-6 months before they hit mainstream."
        )
    
    def _display_input_form(self):
        """Display user preference input form"""
        
        st.subheader("📝 Enter Your Cultural Preferences")
        st.markdown("Tell us about your tastes across different domains to discover emerging trends:")
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            # Music preferences
            st.markdown("**🎵 Music Preferences**")
            music_genres = st.multiselect(
                "Select your favorite music genres:",
                ["indie rock", "electronic", "folk", "hip-hop", "jazz", "classical", "pop", "R&B", "country", "reggae", "ambient", "punk", "blues", "metal"],
                key="music_genres",
                help="Choose genres that best represent your music taste"
            )
            
            # Dining preferences
            st.markdown("**🍽️ Dining Preferences**")
            dining_prefs = st.multiselect(
                "Select your dining preferences:",
                ["artisanal coffee", "plant-based", "local sourcing", "street food", "fusion cuisine", "fine dining", "organic", "craft cocktails", "molecular gastronomy", "wine pairing"],
                key="dining_prefs",
                help="What kind of food experiences do you enjoy?"
            )
            
            # Fashion preferences
            st.markdown("**👔 Fashion Style**")
            fashion_styles = st.multiselect(
                "Select your fashion preferences:",
                ["minimalist", "sustainable", "vintage", "streetwear", "luxury brands", "bohemian", "classic", "avant-garde", "designer", "sneakers"],
                key="fashion_styles",
                help="Styles that match your aesthetic preferences"
            )
        
        with col2:
            # Entertainment preferences
            st.markdown("**🎬 Entertainment Preferences**")
            entertainment = st.multiselect(
                "Select your entertainment preferences:",
                ["indie films", "live music", "podcasts", "sports", "gaming", "theater", "documentaries", "reality TV", "opera", "art galleries", "social media"],
                key="entertainment",
                help="How do you like to spend your leisure time?"
            )
            
            # Lifestyle choices
            st.markdown("**🏡 Lifestyle Choices**")
            lifestyle = st.multiselect(
                "Select your lifestyle preferences:",
                ["sustainable living", "wellness", "remote work", "fitness", "urban living", "travel", "meditation", "DIY", "luxury living", "nightlife", "collecting", "cultural events"],
                key="lifestyle",
                help="Values and lifestyle choices that are important to you"
            )
        
        # Analysis button
        st.markdown("---")
        if st.button("🔍 Analyze Trends with Gemini AI", type="primary", use_container_width=True):
            if self._validate_preferences():
                with st.spinner("🤖 Gemini AI is analyzing cultural patterns and predicting trends..."):
                    self._run_trend_analysis()
            else:
                st.error("Please select at least 2 preferences in each category to get accurate predictions.")
    
    def _validate_preferences(self) -> bool:
        """Validate that user has selected enough preferences"""
        
        required_categories = ['music_genres', 'dining_prefs', 'fashion_styles', 'entertainment', 'lifestyle']
        
        for category in required_categories:
            if len(st.session_state.get(category, [])) < 1:
                return False
        
        return True
    
    def _run_trend_analysis(self):
        """Run trend analysis via API"""
        
        try:
            # Prepare request data
            request_data = {
                "preferences": {
                    "music_genres": st.session_state.get('music_genres', []),
                    "dining_preferences": st.session_state.get('dining_prefs', []),
                    "fashion_styles": st.session_state.get('fashion_styles', []),
                    "entertainment_types": st.session_state.get('entertainment', []),
                    "lifestyle_choices": st.session_state.get('lifestyle', [])
                },
                "timeframe": st.session_state.get('timeframe', '90d')
            }
            
            # Make API request
            response = requests.post(
                f"{self.api_base_url}/predict-trends",
                json=request_data,
                timeout=60  # Increased timeout for Gemini processing
            )
            
            if response.status_code == 200:
                st.session_state['analysis_results'] = response.json()
                st.success("✅ Gemini AI analysis complete! Scroll down to see your predictions.")
                st.rerun()
            else:
                st.error(f"Analysis failed: {response.text}")
                
        except Exception as e:
            st.error(f"Error running analysis: {e}")
    
    def _display_results(self):
        """Display trend analysis results"""
        
        results = st.session_state['analysis_results']
        
        # Results header
        st.subheader("🎯 Your Gemini-Powered Trend Predictions")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Predictions", results['total_predictions'])
        with col2:
            st.metric("Average Confidence", f"{results['average_confidence']:.1f}%")
        with col3:
            st.metric("Timeframe", results['timeframe'])
        with col4:
            st.metric("Analysis Date", results['analysis_date'][:10])
        
        # Confidence distribution chart
        if results['predictions']:
            st.subheader("📊 Analysis Overview")
            
            # Confidence distribution
            confidence_scores = [p['confidence_score'] for p in results['predictions']]
            categories = [p['product_category'] for p in results['predictions']]
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_hist = px.histogram(
                    x=confidence_scores,
                    nbins=10,
                    title="Confidence Score Distribution",
                    labels={'x': 'Confidence Score', 'y': 'Number of Predictions'},
                    color_discrete_sequence=['#1f77b4']
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Category breakdown
                category_counts = pd.Series(categories).value_counts()
                fig_pie = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    title="Predictions by Category"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        # Individual predictions
        st.subheader("📈 Detailed Trend Predictions")
        
        for i, prediction in enumerate(results['predictions'], 1):
            with st.expander(f"🔮 {i}. {prediction['predicted_trend']} - {prediction['confidence_score']:.0f}% confidence"):
                
                # Prediction details in columns
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Category:** {prediction['product_category']}")
                    st.markdown(f"**Timeline:** {prediction['timeline_days']} days")
                
                with col2:
                    st.markdown(f"**Confidence:** {prediction['confidence_score']:.0f}%")
                    st.markdown(f"**Created:** {prediction.get('created_at', 'Recently')[:10]}")
                
                with col3:
                    # Confidence gauge
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = prediction['confidence_score'],
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Confidence"},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "#4285f4"},
                            'steps': [
                                {'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 80], 'color': "#fbbc05"},
                                {'range': [80, 100], 'color': "#34a853"}
                            ]
                        }
                    ))
                    fig.update_layout(height=200)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Target audience
                st.markdown("**🎯 Target Audience:**")
                for audience in prediction['target_audience']:
                    st.badge(audience, type="secondary")
                
                # Cultural reasoning from Gemini
                st.markdown("**🧠 Gemini AI Cultural Analysis:**")
                st.markdown(f"*{prediction['cultural_reasoning']}*")
                
                # Market opportunity
                st.markdown("**💡 Market Opportunity:**")
                st.markdown(prediction['market_opportunity'])
        
        # Export options
        st.subheader("📥 Export Your Predictions")
        
        # Convert to CSV format
        df = pd.DataFrame(results['predictions'])
        csv = df.to_csv(index=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📄 Download as CSV",
                data=csv,
                file_name=f"trendseer_gemini_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # JSON export
            json_data = json.dumps(results, indent=2, default=str)
            st.download_button(
                label="🔧 Download as JSON",
                data=json_data,
                file_name=f"trendseer_gemini_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    def _load_sample_preferences(self, sample_data: dict):
        """Load sample preferences for testing"""
        
        for key, value in sample_data.items():
            st.session_state[key] = value
        
        st.success("✅ Sample preferences loaded! Click 'Analyze Trends' to see predictions.")
        st.rerun()

# Initialize and run dashboard
if __name__ == "__main__":
    dashboard = TrendSeerDashboard()
    dashboard.run()
