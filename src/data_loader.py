import pandas as pd
from src.config import CLEANED_DATA_PATH

def load_historical_data(path=CLEANED_DATA_PATH):
    """
    Load cleaned EPL match data and parse MatchDate as datetime.
    """
    df = pd.read_csv(path)
    df["MatchDate"] = pd.to_datetime(df["MatchDate"])
    df = df.sort_values("MatchDate").reset_index(drop=True)
    return df
