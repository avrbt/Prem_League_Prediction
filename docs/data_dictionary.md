# Data Dictionary

This document describes all engineered features used by the machine learning model.

| Feature Name | Meaning | Calculation | Timing & Availability | Leakage Risk & Prevention |
|:---|:---|:---|:---|:---|
| **HomeForm** / **AwayForm** | Recent team form over the last 5 matches | Sum of points (W=3, D=1, L=0) earned in the previous 5 matches of the team. | Pre-match. Calculated dynamically from historical records before the match date. | Safe. Uses `shift(1)` to ensure the current match's outcome is not included. |
| **HomeGoalsAvg5** / **AwayGoalsAvg5** | Average goals scored over the last 5 matches | Mean of goals scored in the team's last 5 matches. | Pre-match. | Safe. Prevents leakage by rolling only over past matches. |
| **HomeGoalsConcededAvg5** / **AwayGoalsConcededAvg5** | Average goals conceded over the last 5 matches | Mean of goals conceded in the team's last 5 matches. | Pre-match. | Safe. |
| **HomeWinRate5** / **AwayWinRate5** | Win rate over the last 5 matches | Count of wins divided by 5 in the team's last 5 matches. | Pre-match. | Safe. |
| **HomeGoalDiff5** / **AwayGoalDiff5** | Cumulative goal difference over the last 5 matches | Sum of (Goals Scored - Goals Conceded) over the team's last 5 matches. | Pre-match. | Safe. |
| **HomeH2HForm5** | Head-to-Head form | Sum of points earned by the Home team against the Away team in their last 5 head-to-head meetings. | Pre-match. | Safe. |
| **HomePosition** / **AwayPosition** | Current league standings position | Position in the current season's league table ranked by Points, Goal Difference, and Goals For. | Pre-match. Table calculated from matches played strictly before the match date. | Safe. |
| **HomeRestDays** / **AwayRestDays** | Days of rest since the last match | Days elapsed between the match date and the date of the team's previous match. | Pre-match. | Safe. |
