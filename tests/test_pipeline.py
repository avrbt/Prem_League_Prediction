import pytest
import numpy as np
from src.prediction import MatchPredictor

@pytest.fixture
def predictor():
    return MatchPredictor()

def test_predictor_initialization(predictor):
    assert predictor.model is not None
    assert len(predictor.teams) > 0
    assert "Arsenal" in predictor.teams

def test_prediction_sum_to_one(predictor):
    res = predictor.predict("Arsenal", "Chelsea", "2025-04-15")
    total_prob = res["home_win_probability"] + res["draw_probability"] + res["away_win_probability"]
    assert np.isclose(total_prob, 1.0, atol=1e-5)

def test_prediction_invalid_teams(predictor):
    with pytest.raises(ValueError, match="Unknown home team"):
        predictor.predict("NonExistentTeam", "Chelsea", "2025-04-15")

def test_prediction_same_team(predictor):
    with pytest.raises(ValueError, match="Home team and Away team cannot be the same"):
        predictor.predict("Arsenal", "Arsenal", "2025-04-15")

def test_prediction_invalid_date(predictor):
    with pytest.raises(ValueError, match="Invalid match date"):
        predictor.predict("Arsenal", "Chelsea", "invalid-date-string")
