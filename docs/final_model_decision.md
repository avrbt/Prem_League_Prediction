# Final Model Selection Decision

This document details the final model selection analysis and why **Logistic Regression** was chosen over tree-based ensembles (Random Forest, XGBoost) and calibrated pipelines for the production prediction engine.

---

## 1. Problem Objective
The objective of this application is to predict English Premier League match outcome probabilities:
- Home Win ($P(H)$)
- Draw ($P(D)$)
- Away Win ($P(A)$)

Because these probabilities are exposed directly in the UI and API, **probability quality** (measured by **Log Loss**) is the primary performance metric, alongside **Macro F1-score** (to measure balanced performance across all classes, particularly draws).

---

## 2. Models Compared (Final Test Set)
We evaluated all candidates on the exact same chronological test set (comprising seasons 2020/21 to 2024/25):

| Model | Accuracy | Macro F1 | Weighted F1 | Log Loss | Draw Precision | Draw Recall | Draw F1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | **0.5401** | **0.3977** | **0.4656** | **0.9915** | **0.4000** | 0.0053 | 0.0106 |
| **Random Forest** | 0.4985 | 0.3995 | 0.4541 | 1.0229 | 0.2250 | **0.0722** | **0.1093** |
| **XGBoost (Uncalibrated)** | 0.5235 | 0.3741 | 0.4427 | 0.9961 | 0.0000 | 0.0000 | 0.0000 |
| **Calibrated XGBoost** | 0.5174 | 0.3688 | 0.4371 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |

---

## 3. Key Findings

### Probability Quality Comparison (Log Loss)
- **Logistic Regression** achieved the lowest Log Loss (`0.9915`) on the test set.
- Uncalibrated XGBoost followed close behind (`0.9961`).
- Calibrated XGBoost actually saw a slight degradation in Log Loss (`1.0000`) on the test set.

### Accuracy & Macro F1 Comparison
- **Logistic Regression** achieved the highest test accuracy (`0.5401`) and a strong Macro F1 (`0.3977`).
- Random Forest has a slightly higher Macro F1 (`0.3995`) but suffers from low overall accuracy (`0.4985`) and high Log Loss (`1.0229`) due to overfitting.

### Draw Performance
- Draws remain highly volatile and difficult to predict for all models. Under default argmax classification, both XGBoost and Calibrated XGBoost predicted **0 Draws** on the test set.
- Logistic Regression predicted 5 Draws (with a high precision of 40% but low recall).
- Random Forest predicted 120 Draws, but with low precision (22.5%).

---

## 4. Final Decision: Switch back to Logistic Regression

Based on the empirical evidence, we have switched the final production model to **StandardScaler + Logistic Regression**.

### Reasons for Selection:
1. **Best Generalization**: Linear models with L2 regularization prevent overfitting on sports datasets where the signal-to-noise ratio is low.
2. **Superior Log Loss**: Logistic Regression outputs the most mathematically sensible probability estimates, minimizing test set Log Loss (`0.9915`).
3. **Accuracy Floor**: Logistic Regression maintains the highest overall test accuracy (`54.01%`).

---

## 5. Limitations
- **Argmax Draw Limitation**: Like all candidate models, the default prediction classification will rarely output a "Draw" class because the probability of home/away wins is naturally higher. The application communicates these outcomes as probabilities (e.g. 26% Draw, 54% Home, 20% Away) which is the most realistic way to represent football match uncertainties.
