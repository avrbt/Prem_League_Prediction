# Premier League Match Prediction — Interview Preparation Guide

This guide compiles answers to the essential data science and machine learning questions regarding this repository. Use it to prepare for technical interviews and placement rounds.

---

## 📊 1. Data Questions

### Q1: Why did you choose this dataset?
* **Answer**: The **EPL Match Data (2000–2025)** dataset provides a long, rich history (9,000+ matches) of Premier League fixtures. It contains not only outcomes but also granular match-day events (shots, corners, fouls, cards) which allows for detailed historical feature engineering.

### Q2: What is the target?
* **Answer**: The target is `FullTimeResult` (stored as `H` = Home Win, `D` = Draw, `A` = Away Win). It represents a multi-class classification problem.

### Q3: What problems existed in the raw data?
* **Answer**:
  - **Spelling Inconsistencies**: Team names were spelled differently across seasons (e.g. "Man City" vs "Manchester City"). These were mapped to a unified dictionary.
  - **Class Imbalance**: Home wins are significantly more frequent (~45.8%) than away wins (~29.5%) and draws (~24.6%).
  - **Missing Values**: Some match-day event columns had missing values for older seasons (where data collection was less mature). These were verified and handled during cleaning.

---

## ⚙️ 2. Feature Engineering Questions

### Q4: How did you calculate team form?
* **Answer**: Team form is calculated as the sum of points earned (W=3, D=1, L=0) in a team's previous 5 matches.

### Q5: Why did you use rolling averages?
* **Answer**: In sports modeling, recent performance is a much stronger indicator of current strength than season-long stats. Rolling averages capture short-term shifts in form, momentum, and team strength.

### Q6: How did you prevent data leakage?
* **Answer**: We applied a strict `shift(1)` before any rolling calculations (e.g., `x.shift(1).rolling(5)`). This ensures that for a match played on Date T, the rolling average features only contain match statistics from matches played *prior* to Date T, and never include any information from the match being predicted.

### Q7: Why use the previous five matches?
* **Answer**: A window of 5 matches represents a standard timeline in football (roughly 3–4 weeks). It is long enough to smooth out single-match outliers (such as an unexpected red card or referee error) but short enough to remain sensitive to recent form changes.

### Q8: How did you calculate H2H?
* **Answer**: Head-to-Head (H2H) form is calculated as the sum of points earned by the target Home team against the Away team in their last 5 head-to-head meetings.

### Q9: Why is chronological splitting necessary?
* **Answer**: Random splitting (like `train_test_split`) causes time-travel data leakage, where the model trains on future matches to predict past matches. Chronological splitting ensures the test set contains only matches played strictly after all training matches.

---

## 🤖 3. Machine Learning Questions

### Q10: Why Logistic Regression?
* **Answer**: It serves as a linear baseline. It is fast to train, highly interpretable, and establishes a performance floor (accuracy ~0.54).

### Q11: Why Random Forest?
* **Answer**: It is a non-linear bagging ensemble of decision trees. It reduces variance, captures complex non-linear feature interactions, and handles feature scales natively.

### Q12: Why XGBoost?
* **Answer**: It is a gradient boosting framework that builds trees sequentially to minimize errors. It is highly robust, handles regularisation natively, and is generally state-of-the-art for tabular data.

### Q13: Which model performed best?
* **Answer**: Tuned and calibrated **XGBoost** performed best. While its raw accuracy (0.52) was slightly lower than Logistic Regression's home-biased accuracy, its **Log Loss (0.996)** was superior, and it demonstrated much better probability calibration.

### Q14: Why is accuracy insufficient?
* **Answer**: Because of class imbalance. A simple baseline that always predicts "Home Win" would achieve ~46% accuracy. Accuracy does not capture how well the model predicts Draws or how reliable its probability distributions are.

### Q15: Why is Draw prediction difficult?
* **Answer**: Draws are a high-entropy outcome. In football, draws often result from tactical stalemates, defensive playstyles, or late equalizers, which are hard to distinguish from narrow home or away wins using pre-match statistics.

### Q16: What is Log Loss?
* **Answer**: Log Loss measures the performance of a classification model whose output is a probability value between 0 and 1. It heavily penalizes confident but incorrect predictions.

### Q17: What does `predict_proba()` provide?
* **Answer**: It outputs the probability vector for each class (e.g., `[0.18, 0.26, 0.56]`), allowing the system to communicate the uncertainty of the prediction to the user.

---

## 🚀 4. Production & Deployment Questions

### Q18: How is the model saved?
* **Answer**: The final Platt-scaled calibrated model is serialized using `joblib.dump` into `models/final_model.pkl`.

### Q19: How does the API work?
* **Answer**: The FastAPI server exposes a `POST /predict` endpoint. It parses inputs, checks team validity and same-team constraints, generates features dynamically, and calls the model to return the probability dictionary.

### Q20: How does a future match get its features?
* **Answer**: The pipeline pulls the historical records from `data/processed/epl_clean.csv`, filters for matches played by those teams prior to the target match date, and computes form, rolling averages, head-to-head, and rest days on the fly.

### Q21: How does the UI communicate predictions?
* **Answer**: The Streamlit interface displays the predicted outcome and renders a bar chart showing the probability split for each outcome, along with an educational betting disclaimer.

---

## ⚠️ 5. Limitations & Future Improvements

### Q22: What can cause prediction errors?
* **Answer**: Match-day events (early red cards, referee decisions, sudden weather shifts, tactical changes, or key player injuries) are not captured by pre-match historical team form.

### Q23: What information is missing from the dataset?
* **Answer**: Player line-ups, injury reports, manager changes, player fatigue indexes, market odds, and transfer market team values.

### Q24: How could the project be improved?
* **Answer**:
  - Incorporating player-level stats (e.g., from FIFA/FC ratings or actual player match histories).
  - Adding advanced metrics (like Expected Goals (xG), shot conversion rates).
  - Implementing live web scraping to fetch real-time upcoming fixture dates.
