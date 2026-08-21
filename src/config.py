import os

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models")

CLEANED_DATA_PATH = os.path.join(DATA_DIR, "epl_clean.csv")
MODEL_PATH = os.path.join(MODELS_DIR, "final_model.pkl")
FEATURES_PATH = os.path.join(MODELS_DIR, "feature_columns.pkl")
METADATA_PATH = os.path.join(MODELS_DIR, "model_metadata.json")

# Model configuration
FEATURE_COLS = [
    "HomeForm",
    "AwayForm",
    "HomeGoalsAvg5",
    "AwayGoalsAvg5",
    "HomeGoalsConcededAvg5",
    "AwayGoalsConcededAvg5",
    "HomeWinRate5",
    "AwayWinRate5",
    "HomeH2HForm5",
    "HomePosition",
    "AwayPosition",
    "HomeGoalDiff5",
    "AwayGoalDiff5",
    "HomeRestDays",
    "AwayRestDays"
]
