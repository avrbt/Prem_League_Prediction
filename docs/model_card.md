# Model Card — Calibrated XGBoost Classifier

## Model Details
- **Developer**: Antigravity & Pair Programming Partner
- **Model Type**: Calibrated XGBoost Classifier (using `CalibratedClassifierCV` with Sigmoid Platt Scaling)
- **Base Estimator**: `XGBClassifier`
- **Release Date**: 2026-08-22
- **Version**: 1.0.0

## Intended Use
- **Primary Use**: Predict outcome probabilities (Home Win, Draw, Away Win) for English Premier League matches.
- **Target Audience**: Recruiter reviewers and football sports analysts.
- **Not Intended For**: Gambling, commercial betting recommendation systems, or financial risk modeling.

## Training & Evaluation Data
- **Dataset**: Kaggle EPL Match Data 2000–2025.
- **Chronological Train Split**: 7,745 matches (older matches).
- **Chronological Test Split**: 1,635 matches (newer matches starting from season 2020/21).

## Performance Metrics (Test Set)
- **Accuracy**: 0.520
- **Log Loss**: 1.000
- **Macro F1**: 0.37
- **Weighted F1**: 0.44

## Known Limitations & Weaknesses
- **Draw Class Under-prediction**: Due to high class imbalance and high variance in draw outcomes, the default decision boundary predicts very few draws. Probability calibration outputs realistic draw probability distributions (~20–30%) rather than binary classifications.
- **COVID Season Anomaly**: Model accuracy decreases to 46.8% during the 2020/21 season due to stadium closures reducing home advantage.
