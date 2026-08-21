import pandas as pd
import numpy as np

def get_team_stats(team, match_date, df):
    """
    Get rolling stats for a team in the 5 matches played before match_date.
    """
    # Filter for matches where the team played, before the match date
    team_df = df[((df["HomeTeam"] == team) | (df["AwayTeam"] == team)) & (df["MatchDate"] < match_date)]
    team_df = team_df.sort_values("MatchDate", ascending=False).head(5)
    
    if len(team_df) == 0:
        return {
            "Form": 0.0,
            "GoalsAvg5": 0.0,
            "GoalsConcededAvg5": 0.0,
            "WinRate5": 0.0,
            "GoalDiff5": 0.0,
            "RestDays": 7.0  # default rest days
        }
    
    goals_scored = []
    goals_conceded = []
    points = []
    wins = 0
    
    for _, row in team_df.iterrows():
        is_home = row["HomeTeam"] == team
        scored = row["FullTimeHomeGoals"] if is_home else row["FullTimeAwayGoals"]
        conceded = row["FullTimeAwayGoals"] if is_home else row["FullTimeHomeGoals"]
        res = row["FullTimeResult"]
        
        goals_scored.append(scored)
        goals_conceded.append(conceded)
        
        if (res == "H" and is_home) or (res == "A" and not is_home):
            points.append(3)
            wins += 1
        elif res == "D":
            points.append(1)
        else:
            points.append(0)
            
    last_match_date = team_df.iloc[0]["MatchDate"]
    rest_days = (pd.to_datetime(match_date) - last_match_date).days
    # Cap rest days to a maximum of 30 days to prevent extreme out-of-distribution values
    rest_days = min(rest_days, 30)
    
    # Pad if fewer than 5 matches are available (e.g. at the start of historical records)
    n = len(team_df)
    
    return {
        "Form": float(sum(points)),
        "GoalsAvg5": float(np.mean(goals_scored)),
        "GoalsConcededAvg5": float(np.mean(goals_conceded)),
        "WinRate5": float(wins / 5.0), # Win rate is wins / 5.0 (as per rolling 5 count)
        "GoalDiff5": float(sum(goals_scored) - sum(goals_conceded)),
        "RestDays": float(rest_days)
    }

def get_h2h_form(home_team, away_team, match_date, df):
    """
    Get sum of points earned by home_team against away_team in their last 5 H2H meetings.
    """
    h2h_df = df[
        (((df["HomeTeam"] == home_team) & (df["AwayTeam"] == away_team)) |
         ((df["HomeTeam"] == away_team) & (df["AwayTeam"] == home_team))) &
        (df["MatchDate"] < match_date)
    ]
    h2h_df = h2h_df.sort_values("MatchDate", ascending=False).head(5)
    
    points = 0
    for _, row in h2h_df.iterrows():
        # Home team in the target match is home_team.
        # If home_team was home in the H2H match:
        if row["HomeTeam"] == home_team:
            if row["FullTimeResult"] == "H":
                points += 3
            elif row["FullTimeResult"] == "D":
                points += 1
        # If home_team was away in the H2H match:
        else:
            if row["FullTimeResult"] == "A":
                points += 3
            elif row["FullTimeResult"] == "D":
                points += 1
                
    return float(points)

def get_league_positions(home_team, away_team, match_date, df):
    """
    Build the league table for the current season up to match_date, and return positions.
    """
    # 1. Determine current season based on match_date
    # Since match_date is in datetime format, find the season
    target_match = df[df["MatchDate"] < match_date].sort_values("MatchDate", ascending=False)
    if len(target_match) == 0:
        return 10.0, 10.0  # Defaults if no prior matches
        
    current_season = target_match.iloc[0]["Season"]
    
    # 2. Filter matches of the same season before match_date
    season_df = df[(df["Season"] == current_season) & (df["MatchDate"] < match_date)]
    
    # All teams in this season
    teams = set(df[df["Season"] == current_season]["HomeTeam"]) | set(df[df["Season"] == current_season]["AwayTeam"])
    if not teams:
        return 10.0, 10.0
        
    table = {team: {"Points": 0, "GF": 0, "GA": 0} for team in teams}
    
    for _, match in season_df.iterrows():
        home = match["HomeTeam"]
        away = match["AwayTeam"]
        home_goals = match["FullTimeHomeGoals"]
        away_goals = match["FullTimeAwayGoals"]
        
        table[home]["GF"] += home_goals
        table[home]["GA"] += away_goals
        table[away]["GF"] += away_goals
        table[away]["GA"] += home_goals
        
        if home_goals > away_goals:
            table[home]["Points"] += 3
        elif home_goals < away_goals:
            table[away]["Points"] += 3
        else:
            table[home]["Points"] += 1
            table[away]["Points"] += 1
            
    # Sort teams by Points, Goal Difference, Goals For
    ranking = sorted(
        teams,
        key=lambda t: (
            table[t]["Points"],
            table[t]["GF"] - table[t]["GA"],
            table[t]["GF"]
        ),
        reverse=True
    )
    
    positions = {team: i + 1 for i, team in enumerate(ranking)}
    
    home_pos = positions.get(home_team, 10.0)
    away_pos = positions.get(away_team, 10.0)
    
    return float(home_pos), float(away_pos)

def generate_match_features(home_team, away_team, match_date, df):
    """
    Generate the complete pre-match feature row for Team A vs Team B.
    """
    match_date = pd.to_datetime(match_date)
    
    home_stats = get_team_stats(home_team, match_date, df)
    away_stats = get_team_stats(away_team, match_date, df)
    
    h2h_form = get_h2h_form(home_team, away_team, match_date, df)
    home_pos, away_pos = get_league_positions(home_team, away_team, match_date, df)
    
    feature_dict = {
        "HomeForm": home_stats["Form"],
        "AwayForm": away_stats["Form"],
        "HomeGoalsAvg5": home_stats["GoalsAvg5"],
        "AwayGoalsAvg5": away_stats["GoalsAvg5"],
        "HomeGoalsConcededAvg5": home_stats["GoalsConcededAvg5"],
        "AwayGoalsConcededAvg5": away_stats["GoalsConcededAvg5"],
        "HomeWinRate5": home_stats["WinRate5"],
        "AwayWinRate5": away_stats["WinRate5"],
        "HomeH2HForm5": h2h_form,
        "HomePosition": home_pos,
        "AwayPosition": away_pos,
        "HomeGoalDiff5": home_stats["GoalDiff5"],
        "AwayGoalDiff5": away_stats["GoalDiff5"],
        "HomeRestDays": home_stats["RestDays"],
        "AwayRestDays": away_stats["RestDays"]
    }
    
    return pd.DataFrame([feature_dict])
