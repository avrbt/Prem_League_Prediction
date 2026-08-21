# Project Status

## Current Phase
Project Audit and Baseline Model Comparison Setup

## Completed
- Data Collection and Cleaning Notebooks (`01_data_collection.ipynb`, `02_data_cleaning.ipynb`)
- Exploratory Data Analysis Notebook (`03_exploratory_data_analysis.ipynb`)
- Feature Engineering Notebook (`04_feature_engineering.ipynb`)
- Train/Test Split (Chronological, no leakage)
- Logistic Regression Baseline Model Training in `05_model_training.ipynb`

## Currently Working On
- Project Audit
- Setup of Random Forest and XGBoost baseline models in `05_model_training.ipynb`

## Next Steps
1. Implement Random Forest baseline model (no tuning).
2. Implement XGBoost/Gradient Boosting baseline model (no tuning).
3. Create model comparison table and confusion matrices for baseline models.
4. Perform Draw class analysis.

## Dataset
- **English Premier League Match Data (2000–2025)**
- Shape: 9,380 rows, 44 columns
- Train set: 7,745 rows (older matches)
- Test set: 1,635 rows (newer matches)

## Features
- `HomeForm`, `AwayForm`
- `HomeGoalsAvg5`, `AwayGoalsAvg5`
- `HomeGoalsConcededAvg5`, `AwayGoalsConcededAvg5`
- `HomeWinRate5`, `AwayWinRate5`
- `HomeH2HForm5` (Head-to-Head form)
- `HomePosition`, `AwayPosition`
- `HomeGoalDiff5`, `AwayGoalDiff5`
- `HomeRestDays`, `AwayRestDays`

## Current Best Model
- **Logistic Regression** (Baseline)

## Current Metrics
- **Accuracy**: 0.540
- **Macro F1**: 0.40
- **Log Loss**: 0.9915
- **Draw Recall**: 0.01 (extremely low)

## Known Problems
- Logistic Regression model is heavily biased toward predicting Home/Away results and fails to capture Draws (Recall: 0.01).
- Lack of model persistence, backend API, prediction pipeline, frontend UI, testing, and full documentation.

## Important Decisions
- Chronological train/test split has been implemented to avoid future data leakage.

## Last Completed Git Commit
- Initial commit / project setup from previous stage.

## Last Updated
2026-08-22
