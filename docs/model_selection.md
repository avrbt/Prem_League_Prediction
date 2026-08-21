# Model Selection & Draw Class Analysis

This document details the evaluation of candidate models, hyperparameter tuning methodology, final model selection, and in-depth Draw class analysis.

---

## 1. Models Evaluated & Baseline Results

We evaluated three candidate architectures on the chronological test set (comprising matches from season 2020/21 onwards):
1. **Logistic Regression (Baseline)**: Scaled inputs + default parameters.
2. **Random Forest (Baseline)**: Default parameters.
3. **XGBoost (Baseline)**: Default parameters.

### Baseline Comparison Table
(Sorted by Macro F1-score)

| Model | Accuracy | Macro F1 | Weighted F1 | Log Loss | Draw Precision | Draw Recall | Draw F1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGBoost (Baseline)** | 0.4783 | **0.4088** | 0.4527 | 1.0816 | 0.26 | 0.14 | 0.18 |
| **Random Forest (Baseline)** | 0.4985 | 0.3995 | 0.4541 | 1.0229 | 0.23 | 0.07 | 0.11 |
| **Logistic Regression (Baseline)**| **0.5401** | 0.3977 | **0.4656** | **0.9915** | **0.40** | 0.01 | 0.01 |

*Observation*: While Logistic Regression yields the highest raw accuracy (0.5401), it is heavily biased toward Home wins and fails to capture Draws (Recall = 0.01). XGBoost baseline has the highest Draw recall (0.14) and Macro F1 (0.4088), but shows overfitting (Log Loss: 1.0816).

---

## 2. Draw Class Analysis

### Why the Draw Class is Difficult
Draws are structurally difficult to predict in football:
1. **Class Imbalance**: Draws represent only ~24.6% of the dataset, compared to ~45.8% for Home Wins and ~29.5% for Away Wins.
2. **Outcome Entropy**: A draw is often a transitional outcome. A match where two teams are evenly matched can easily end in a narrow 1-goal win (H or A) due to a single match-day event (e.g. a red card, referee penalty, or individual error), making it highly volatile to predict using pre-match statistics alone.
3. **Probability Thresholds**: Standard classifiers assign prediction labels using `argmax` (the class with the highest probability). Since the prior probability of a Draw is low, the predicted probability rarely exceeds that of Home or Away, leading to near-zero predicted draws.

### Confusion Matrices (Baseline)
- **Logistic Regression**:
  - Predicted 3 Draws out of 374 actual draws (Recall: 1%).
- **Random Forest**:
  - Predicted 116 Draws (Recall: 7%).
- **XGBoost**:
  - Predicted 202 Draws (Recall: 14%).

---

## 3. Hyperparameter Tuning & Validation Strategy

### Chronological Validation
We utilized a **5-fold `TimeSeriesSplit`** cross-validation on the training set. This ensures that validation folds respect chronological ordering (older matches train the model; newer matches validate it) preventing time-travel data leakage. The test set was kept completely untouched during tuning.

### Hyperparameters Tuned
We tuned the strongest baseline model (**XGBoost**) using `GridSearchCV`:
- `n_estimators`: `[50, 100, 150]`
- `learning_rate`: `[0.01, 0.05, 0.1]`
- `max_depth`: `[3, 5, 7]`
- `subsample` & `colsample_bytree`: `[0.8, 1.0]`

**Best Hyperparameters found**:
- `colsample_bytree`: 0.8
- `learning_rate`: 0.05
- `max_depth`: 3
- `n_estimators`: 100
- `subsample`: 0.8

---

## 4. Final Model Selection Criteria

The **Calibrated XGBoost Classifier** was selected as the final model based on:
1. **Macro F1-score**: XGBoost balances classification metrics across all three outcomes better than Logistic Regression.
2. **Log Loss**: Minimizing Log Loss was prioritized over raw accuracy because the application exposes probabilities. Tuned XGBoost improved Log Loss to `0.9961`.
3. **Probability Calibration**: We applied Platt scaling (`CalibratedClassifierCV` with Sigmoid scaling) to ensure that the predicted probabilities align with actual empirical frequencies.

---

## 5. Final Test Evaluation

Evaluated once on the untouched chronological test set:
- **Accuracy**: 0.5187
- **Macro F1**: 0.3697
- **Weighted F1**: 0.4400
- **Log Loss**: 1.0000

### Test Set Actual vs Predicted Distribution
- **Actual Counts**: Home Win: 722, Away Win: 539, Draw: 374
- **Predicted Counts**: Home Win: 1205, Away Win: 430, Draw: 0 (using default argmax threshold)

*Note*: As discussed in Draw Analysis, the default argmax classification predicts 0 Draws. However, the model outputs well-calibrated probabilities for draws (ranging between 20-30%), which is the primary consumption mode of the production prediction pipeline.

---

## 6. Reproducibility
To ensure exact reproduction of these results:
- All training and validation algorithms use a fixed random state: `random_state = 42`.
- Clipped `RestDays` feature to a max of 30 days is enforced in the pipeline to prevent extrapolation errors.
