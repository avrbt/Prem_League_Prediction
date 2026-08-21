# Project Status

## Current Phase
Model Tuning and Explainability Setup

## Completed
- Data Collection and Cleaning Notebooks (`01_data_collection.ipynb`, `02_data_cleaning.ipynb`)
- Exploratory Data Analysis Notebook (`03_exploratory_data_analysis.ipynb`)
- Feature Engineering Notebook (`04_feature_engineering.ipynb`)
- Train/Test Split (Chronological, no leakage)
- Logistic Regression Baseline Model Training in `05_model_training.ipynb`
- Random Forest and XGBoost Baseline Model Training in `05_model_training.ipynb`
- Baseline Models Comparison and Confusion Matrices in `06_model_evaluation.ipynb`
- Draw Class Analysis and Experiments in `06_model_evaluation.ipynb`

## Currently Working On
- Model Tuning and Validation Strategy Setup in `07_model_tuning.ipynb`

## Next Steps
1. Tune Random Forest and XGBoost hyperparameters using `TimeSeriesSplit` cross-validation in `07_model_tuning.ipynb`.
2. Evaluate tuned models against the test set and perform probability calibration.
3. Select the best final model and save it to `models/` with metadata.
4. Perform Model Explainability analysis in `08_model_explainability.ipynb`.

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
- b435cda: Train baseline classifiers and perform model evaluation and draw analysis

## Last Updated
2026-08-22
