# Project Status

## Current Phase
Project Complete

## Completed
- Data Collection and Cleaning Notebooks (`01_data_collection.ipynb`, `02_data_cleaning.ipynb`)
- Exploratory Data Analysis Notebook (`03_exploratory_data_analysis.ipynb`)
- Feature Engineering Notebook (`04_feature_engineering.ipynb`)
- Train/Test Split (Chronological, no leakage)
- Logistic Regression Baseline Model Training in `05_model_training.ipynb`
- Random Forest and XGBoost Baseline Model Training in `05_model_training.ipynb`
- Baseline Models Comparison and Confusion Matrices in `06_model_evaluation.ipynb`
- Draw Class Analysis and Experiments in `06_model_evaluation.ipynb`
- GridSearch CV Tuning using `TimeSeriesSplit` in `07_model_tuning.ipynb`
- Probability calibration with Platt scaling / Sigmoid Calibrated Classifier
- Serialization of the final calibrated model, features list, and metadata config JSON
- Feature importance visualization and season-by-season performance evaluations in `08_model_explainability.ipynb`
- Decoupled production pipeline modules in `src/`
- FastAPI backend server in `app/main.py`
- Streamlit outcome predictor UI in `app/ui.py`
- Automated test suites (FastAPI client, input validators, prediction pipeline) in `tests/`
- Documentation suite (architecture flow, data dictionary, model card, decisions log, changelog, README)

## Currently Working On
- Production Prediction Audit Review

## Production Prediction Audit
- **Audit Status**: Completed, Verified, and Future Data Handling Review finalized.
- **Tests Performed**:
  - Expanded and executed automated pytest suite (14/14 tests passed successfully).
  - Verified probability bounds [0, 1] and sum constraint (~1.0).
  - Verified symmetry (Home vs Away swapping swaps probabilities logically).
  - Verified future-date prediction timing (no time-series leakage, rest days compute correctly, league positions fallback to last completed season).
  - Verified invalid input handling (ValueError raised for duplicate/unknown teams, invalid dates).
- **Issues Found**:
  - Future dates (e.g. 2026) generated out-of-distribution values for `RestDays` (e.g. 530 days) and stale form/standing features.
- **Fixes Made**:
  - Capped `RestDays` features to a maximum of 30 days.
  - Implemented `is_historical_simulation` warning flag/message in the prediction pipeline and API.
  - Integrated warnings banner in the Streamlit UI for matches scheduled after `2025-05-05`.
- **Remaining Issues**: None.

## Next Steps
- Deploy FastAPI backend to a hosting environment (e.g. Render, AWS).
- Integrate active database tracking (e.g. SQLite) to ingest future EPL matches as they are played.

## Dataset
- **English Premier League Match Data (2000–2025)**
- Train set: 7,745 matches
- Test set: 1,635 matches

## Features
- 15 pre-match strength/form features including rolling form, goals avg, win rates, goal difference, H2H, positions, and rest days.

## Current Best Model
- **Calibrated XGBoost Classifier**

## Current Metrics
- **Accuracy**: 0.5187
- **Macro F1**: 0.3697
- **Log Loss**: 1.0000

## Known Problems
- **Draw Recall**: The default decision threshold classifies very few draws. Probability calibration outputs realistic draw probability distributions (~20–30%) rather than binary classifications. Adjusting the prediction threshold for draws to `0.28` boosts Draw Recall to `18.7%` at a small accuracy cost.

## Important Decisions
- Chronological train/test split has been implemented to avoid future data leakage.
- Calibration was applied to XGBoost to ensure output probabilities represent actual frequencies.

## Last Completed Git Commit
- `67c3098` (or subsequent): Complete project development (API, UI, tests, documentation)

## Last Updated
2026-08-22
