# Architectural Decisions Log

This log documents major decisions made during the design and development of the Premier League Match Prediction project.

## Decision 001: Chronological Train/Test Split
* **Status**: Approved
* **Context**: Traditional random train/test splits lead to severe data leakage in time-series sports datasets since information from future matches (e.g. form, goal differences) propagates back to predict historical matches.
* **Decision**: We enforced a strict chronological split where all training matches occur before any test matches.

## Decision 002: Model Calibration
* **Status**: Approved
* **Context**: XGBoost predictions are often uncalibrated out-of-the-box, meaning output probabilities do not align with actual class frequencies.
* **Decision**: We wrapped the best tuned model with `CalibratedClassifierCV` (Sigmoid scaling) using chronological cross-validation to provide trustworthy, calibrated probabilities.

## Decision 003: Draw Class Mitigation
* **Status**: Approved
* **Context**: Baseline classifiers had near-zero recall for draws.
* **Decision**: While balanced class weights and threshold tuning (setting Draw threshold to 0.28) improve Draw recall, they lower overall accuracy. We decided to output calibrated probabilities and add a threshold option or explain this limitation transparently in the model card rather than artificially manipulating labels.
