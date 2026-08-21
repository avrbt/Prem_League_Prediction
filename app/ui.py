import streamlit as st
import pandas as pd
from datetime import datetime
import os
import sys

# Ensure project root is in path for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.prediction import MatchPredictor

st.set_page_config(
    page_title="EPL Match Outcome Predictor",
    page_icon="⚽",
    layout="centered"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #3F51B5;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #757575;
        font-family: 'Outfit', sans-serif;
        font-weight: 400;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-label {
        font-size: 14px;
        color: #616161;
        font-weight: 500;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #2E7D32;
    }
    .disclaimer {
        font-size: 12px;
        color: #9e9e9e;
        margin-top: 50px;
        text-align: center;
        border-top: 1px solid #e0e0e0;
        padding-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>⚽ Premier League Match Outcome Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Serious pre-match statistical prediction engine</p>", unsafe_allow_html=True)

import requests

API_URL = os.environ.get("API_URL", "https://prem-league-prediction.onrender.com")

use_api = False
teams = []
try:
    response = requests.get(f"{API_URL}/teams", timeout=3)
    if response.status_code == 200:
        teams = response.json()["teams"]
        use_api = True
except Exception:
    pass

if not use_api:
    @st.cache_resource
    def load_predictor():
        return MatchPredictor()

    try:
        predictor = load_predictor()
        teams = predictor.teams
    except Exception as e:
        st.error(f"Error loading prediction engine: {e}")
        st.stop()

# Layout
col1, col2 = st.columns(2)

with col1:
    home_team = st.selectbox("🏠 Select Home Team", teams, index=teams.index("Arsenal") if "Arsenal" in teams else 0)

with col2:
    # Filter out home team from away selection
    away_teams = [t for t in teams if t != home_team]
    away_team = st.selectbox("✈️ Select Away Team", away_teams, index=away_teams.index("Chelsea") if "Chelsea" in away_teams else 0)

match_date = st.date_input("📅 Select Match Date", datetime.now().date())

if st.button("Predict Match Outcome", use_container_width=True):
    try:
        # Run Prediction
        if use_api:
            payload = {
                "home_team": home_team,
                "away_team": away_team,
                "match_date": str(match_date)
            }
            res = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
            if res.status_code == 200:
                pred_res = res.json()
            else:
                detail = res.json().get("detail", "API prediction failed.")
                raise ValueError(detail)
        else:
            pred_res = predictor.predict(home_team, away_team, str(match_date))
        
        if pred_res.get("is_historical_simulation"):
            st.warning(pred_res["warning"])
        else:
            st.success("Prediction complete!")
        
        # Display Prediction result
        prediction_map = {"H": "Home Win", "D": "Draw", "A": "Away Win"}
        st.subheader(f"Predicted Outcome: **{prediction_map[pred_res['prediction']]}**")
        
        # Display Probabilities
        prob_df = pd.DataFrame({
            "Outcome": ["Home Win", "Draw", "Away Win"],
            "Probability (%)": [
                pred_res["home_win_probability"] * 100,
                pred_res["draw_probability"] * 100,
                pred_res["away_win_probability"] * 100
            ]
        })
        
        st.bar_chart(prob_df.set_index("Outcome"))
        
        # Metrics Display
        col_h, col_d, col_a = st.columns(3)
        with col_h:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>🏠 Home Win</div>
                <div class='metric-value'>{pred_res['home_win_probability']*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col_d:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>🤝 Draw</div>
                <div class='metric-value' style='color:#EF6C00;'>{pred_res['draw_probability']*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col_a:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>✈️ Away Win</div>
                <div class='metric-value' style='color:#1565C0;'>{pred_res['away_win_probability']*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
    except ValueError as val_err:
        st.error(str(val_err))
    except Exception as e:
        st.error(f"Prediction failed: {e}")

st.markdown("""
<div class='disclaimer'>
    ⚠️ <strong>Educational Disclaimer:</strong> This tool is an educational football outcome prediction system built for placement preparation. 
    It is not a gambling or betting system, nor does it recommend any betting choices. Predictions are purely probabilistic 
    based on historical team form and are not guarantees of match results.
</div>
""", unsafe_allow_html=True)
