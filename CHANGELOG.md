# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-08-22
### Added
- Completed baseline model training for Random Forest and XGBoost in `05_model_training.ipynb`.
- Baseline comparison tables and confusion matrices in `06_model_evaluation.ipynb`.
- Draw class recall analysis and threshold tuning experiments.
- Hyperparameter tuning utilizing `TimeSeriesSplit` chronological cross-validation.
- Platt-scaling probability calibration with `CalibratedClassifierCV`.
- Saved final model pickle, feature list pickle, and JSON metadata configuration.
- Model explainability and season-by-season performance evaluations in `08_model_explainability.ipynb`.
- Decoupled production modules in `src/` (`config.py`, `data_loader.py`, `feature_engineering.py`, `prediction.py`).
- FastAPI backend endpoints in `app/main.py`.
- Interactive Streamlit predictor UI in `app/ui.py`.
- Automated test suites in `tests/`.
- Full project documentation (`docs/` folder: data dictionary, model card, decisions, architecture).
