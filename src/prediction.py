import joblib
import pandas as pd
import numpy as np
from src.config import MODEL_PATH, FEATURE_COLS
from src.data_loader import load_historical_data
from src.feature_engineering import generate_match_features

class MatchPredictor:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
        self.df = load_historical_data()
        self.teams = sorted(list(set(self.df["HomeTeam"]) | set(self.df["AwayTeam"])))

    def validate_inputs(self, home_team, away_team, match_date):
        if home_team not in self.teams:
            raise ValueError(f"Unknown home team: {home_team}")
        if away_team not in self.teams:
            raise ValueError(f"Unknown away team: {away_team}")
        if home_team == away_team:
            raise ValueError("Home team and Away team cannot be the same.")
        try:
            pd.to_datetime(match_date)
        except Exception:
            raise ValueError(f"Invalid match date: {match_date}")

    def predict(self, home_team, away_team, match_date):
        self.validate_inputs(home_team, away_team, match_date)
        
        # Generate dynamic features from historical data before match_date
        features = generate_match_features(home_team, away_team, match_date, self.df)
        
        # Select features in the exact order required by the model
        X = features[FEATURE_COLS]
        
        # Predict probabilities
        # classes_ are mapped as 0: 'A', 1: 'D', 2: 'H'
        probs = self.model.predict_proba(X)[0]
        
        # Predict outcome
        pred_val = self.model.predict(X)[0]
        if isinstance(pred_val, (int, np.integer)):
            outcome_map = {0: "A", 1: "D", 2: "H"}
            predicted_outcome = outcome_map[pred_val]
        else:
            predicted_outcome = str(pred_val)
        
        max_date = self.df["MatchDate"].max()
        is_simulated = pd.to_datetime(match_date) > max_date
        
        return {
            "home_team": home_team,
            "away_team": away_team,
            "match_date": str(pd.to_datetime(match_date).date()),
            "prediction": predicted_outcome,
            "home_win_probability": float(probs[2]),
            "draw_probability": float(probs[1]),
            "away_win_probability": float(probs[0]),
            "is_historical_simulation": is_simulated,
            "warning": f"The match date is beyond the latest available match in the dataset ({max_date.date()}). Predictions are simulated using the final historical state." if is_simulated else None
        }
