import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_get_teams():
    res = client.get("/teams")
    assert res.status_code == 200
    assert "teams" in res.json()
    assert "Arsenal" in res.json()["teams"]

def test_predict_success():
    req_body = {
        "home_team": "Arsenal",
        "away_team": "Chelsea",
        "match_date": "2025-04-15"
    }
    res = client.post("/predict", json=req_body)
    assert res.status_code == 200
    res_data = res.json()
    assert res_data["home_team"] == "Arsenal"
    assert res_data["away_team"] == "Chelsea"
    assert "prediction" in res_data
    assert "home_win_probability" in res_data

def test_predict_same_team():
    req_body = {
        "home_team": "Arsenal",
        "away_team": "Arsenal",
        "match_date": "2025-04-15"
    }
    res = client.post("/predict", json=req_body)
    assert res.status_code == 400
    assert "Home team and Away team cannot be the same" in res.json()["detail"]

def test_predict_invalid_team():
    req_body = {
        "home_team": "FakeTeamName",
        "away_team": "Chelsea",
        "match_date": "2025-04-15"
    }
    res = client.post("/predict", json=req_body)
    assert res.status_code == 400
    assert "Unknown home team" in res.json()["detail"]
