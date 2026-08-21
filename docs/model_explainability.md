# Model Explainability & Sanity Check Report

This document analyzes the final **Calibrated XGBoost Classifier** predictions using feature importance and output verification.

---

## 1. Feature Importance Ranking (Top 10)

Because the final model is wrapped in Platt calibration (`CalibratedClassifierCV`), we extracted the average feature importances from the underlying XGBoost base estimators:

| Rank | Feature | Importance | Football Interpretation |
| :--- | :--- | :---: | :--- |
| 1 | **AwayPosition** | 0.1404 | League standing (reflects historical/season-long away team strength) |
| 2 | **HomePosition** | 0.1125 | League standing (reflects historical/season-long home team strength) |
| 3 | **AwayWinRate5** | 0.0789 | Recent away team win conversion rate (5 matches) |
| 4 | **HomeGoalDiff5** | 0.0768 | Recent home attacking/defensive goal superiority (5 matches) |
| 5 | **AwayGoalDiff5** | 0.0707 | Recent away attacking/defensive goal superiority (5 matches) |
| 6 | **HomeH2HForm5** | 0.0653 | Historical head-to-head performance match-up points |
| 7 | **HomeWinRate5** | 0.0603 | Recent home team win conversion rate (5 matches) |
| 8 | **HomeGoalsConcededAvg5**| 0.0552 | Recent home defensive stability (goals conceded in last 5 matches) |
| 9 | **AwayForm** | 0.0534 | Recent away points form sum (last 5 matches) |
| 10 | **AwayGoalsAvg5** | 0.0513 | Recent away attacking strength (goals scored in last 5 matches) |

### Important Disclaimer: Correlation vs. Causation
Feature importance measures the **dependence** of the decision trees on specific features during classification splits. It does **NOT** represent causation. For example, a high importance for `AwayPosition` shows the model relies on standings to partition match outcomes; it does not mean a team's position physically causes them to win or lose.

---

## 2. Probability Sanity Checks

We ran 10 predictions representing different tactical matchup scenarios. All predictions conform to:
- $0 \le P(\text{Outcome}) \le 1$
- $P(\text{Home}) + P(\text{Draw}) + P(\text{Away}) \approx 1.0$

| Fixture | Category | Date | P(Home Win) | P(Draw) | P(Away Win) | Prediction |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Man City vs Norwich** | Strong Home vs Weak Away | 2021-10-15 | 68.65% | 18.94% | 12.40% | H |
| **Norwich vs Man City** | Weak Home vs Strong Away | 2021-10-15 | 17.45% | 20.30% | 62.26% | A |
| **Liverpool vs Chelsea** | Strong vs Strong | 2022-01-15 | 47.37% | 26.83% | 25.80% | H |
| **Chelsea vs Liverpool** | Strong vs Strong | 2022-01-15 | 47.63% | 24.95% | 27.42% | H |
| **Norwich vs Watford** | Weak vs Weak | 2021-09-18 | 32.05% | 26.51% | 41.44% | A |
| **Watford vs Norwich** | Weak vs Weak | 2021-09-18 | 38.49% | 30.46% | 31.06% | H |
| **Tottenham vs Everton** | Historically Balanced | 2022-03-07 | 53.59% | 24.67% | 21.74% | H |
| **Everton vs Tottenham** | Historically Balanced | 2022-03-07 | 34.60% | 29.29% | 36.12% | A |
| **Arsenal vs Chelsea** | Future Simulation | 2026-10-15 | 49.27% | 26.96% | 23.76% | H |
| **Man United vs Liverpool**| Future Simulation | 2026-12-15 | 18.71% | 23.03% | 58.26% | A |

---

## 3. Home/Away Symmetry Tests

By swapping home/away teams, we verified that the model responds logically to venue advantage:
- **Arsenal vs Chelsea (2025-04-15)**: Home Win: `58.15%`, Draw: `25.81%`, Away Win: `16.04%` (Pred: H)
- **Chelsea vs Arsenal (2025-04-15)**: Home Win: `37.58%`, Draw: `25.00%`, Away Win: `37.42%` (Pred: H)
- **Liverpool vs Man United (2024-12-15)**: Home Win: `65.73%`, Draw: `19.90%`, Away Win: `14.37%` (Pred: H)
- **Man United vs Liverpool (2024-12-15)**: Home Win: `25.15%`, Draw: `25.69%`, Away Win: `49.16%` (Pred: A)
