# Experiments Log

This document tracks all machine learning model experiments, features used, model parameters, and test set performance.

## Experiment 001 — Logistic Regression (Baseline)
* **Date**: 2026-08-22
* **Features**: 15 pre-match strength/form features.
* **Model**: `LogisticRegression` + `StandardScaler` (Default parameters).
* **Test Metrics**:
  - Accuracy: 0.5401
  - Macro F1: 0.3977
  - Weighted F1: 0.4656
  - Log Loss: 0.9915
* **Observations**: Heavy home-bias; performs very poorly on Draw predictions (Recall: 0.01).

## Experiment 002 — Random Forest (Baseline)
* **Date**: 2026-08-22
* **Features**: 15 pre-match strength/form features.
* **Model**: `RandomForestClassifier` (Default parameters).
* **Test Metrics**:
  - Accuracy: 0.4985
  - Macro F1: 0.3995
  - Weighted F1: 0.4541
  - Log Loss: 1.0229
* **Observations**: Overfits train set (Log Loss on test is higher than Logistic Regression). Slightly higher Draw Recall (0.07).

## Experiment 003 — XGBoost (Baseline)
* **Date**: 2026-08-22
* **Features**: 15 pre-match strength/form features.
* **Model**: `XGBClassifier` (Default parameters).
* **Test Metrics**:
  - Accuracy: 0.4783
  - Macro F1: 0.4088
  - Weighted F1: 0.4527
  - Log Loss: 1.0816
* **Observations**: High overfitting with default parameters (test Log Loss is 1.0816). However, achieves the best baseline Draw Recall (0.14). Needs tuning and regularization.
