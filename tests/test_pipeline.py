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

def test_prediction_within_dataset_range(predictor):
    res = predictor.predict("Arsenal", "Chelsea", "2024-04-15")
    assert res["is_historical_simulation"] is False
    assert res["warning"] is None

def test_prediction_exactly_after_latest_match(predictor):
    res = predictor.predict("Arsenal", "Chelsea", "2025-05-06")
    assert res["is_historical_simulation"] is True
    assert "beyond the latest available match" in res["warning"]

def test_prediction_far_future_date(predictor):
    res = predictor.predict("Arsenal", "Chelsea", "2026-10-15")
    assert res["is_historical_simulation"] is True
    assert "beyond the latest available match" in res["warning"]

def test_rest_days_capping_on_future_date(predictor):
    from src.feature_engineering import generate_match_features
    feats = generate_match_features("Arsenal", "Chelsea", "2026-10-15", predictor.df)
    assert feats.iloc[0]["HomeRestDays"] == 30.0
    assert feats.iloc[0]["AwayRestDays"] == 30.0

def test_regression_multi_class_attribute_missing(predictor):
    classifier = predictor.model.named_steps["classifier"]
    if hasattr(classifier, "multi_class"):
        delattr(classifier, "multi_class")
    if not hasattr(classifier, "multi_class"):
        classifier.multi_class = "auto"
    res = predictor.predict("Arsenal", "Chelsea", "2025-04-15")
    assert res is not None
    assert "prediction" in res
