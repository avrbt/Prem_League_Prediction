from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.prediction import MatchPredictor

app = FastAPI(
    title="Premier League Match Predictor API",
    description="API for predicting outcome probabilities of Premier League matches.",
    version="1.0.0"
)

try:
    predictor = MatchPredictor()
except Exception as e:
    print(f"Error loading MatchPredictor: {e}")
    predictor = None

class PredictionRequest(BaseModel):
    home_team: str = Field(..., example="Liverpool")
    away_team: str = Field(..., example="Chelsea")
    match_date: str = Field(..., example="2025-04-15")

class PredictionResponse(BaseModel):
    home_team: str
    away_team: str
    match_date: str
    prediction: str
    home_win_probability: float
    draw_probability: float
    away_win_probability: float
    is_historical_simulation: bool
    warning: str | None = None

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/teams")
def get_teams():
    if predictor is None:
        raise HTTPException(status_code=500, detail="Model predictor is not initialized.")
    return {"teams": predictor.teams}

@app.post("/predict", response_model=PredictionResponse)
def predict_match(request: PredictionRequest):
    if predictor is None:
        raise HTTPException(status_code=500, detail="Model predictor is not initialized.")
    
    try:
        result = predictor.predict(
            home_team=request.home_team,
            away_team=request.away_team,
            match_date=request.match_date
        )
        return result
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
