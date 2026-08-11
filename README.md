# ⚽ Premier League Match Prediction

A machine learning project that predicts the outcome of English Premier League matches using historical match data and pre-match team performance features.

The goal is to build an end-to-end ML system that can predict:

- 🏠 Home Win
- 🤝 Draw
- ✈️ Away Win

The project focuses heavily on **time-aware feature engineering** to ensure that only information available before a match is used for prediction.

---

## 🎯 Project Objective

Build a machine learning model capable of predicting Premier League match outcomes based on historical team performance.

Instead of directly using match statistics from the game being predicted, the project creates historical features such as:

- Recent team form
- Rolling goals scored
- Rolling goals conceded
- Home/away strength
- Head-to-head performance
- League position
- Goal difference
- Rest days

This helps prevent **data leakage** and makes the prediction setup closer to a real-world prediction system.

---

## 📊 Dataset

The project uses the following Kaggle dataset:

**English Premier League (EPL) Match Data 2000–2025**

Dataset:
https://www.kaggle.com/datasets/marcohuiii/english-premier-league-epl-match-data-2000-2025

The dataset contains Premier League matches from 2000 to 2025.

### Main Match Information

- Match date
- Home team
- Away team
- Full-time home goals
- Full-time away goals
- Full-time result
- Half-time result
- Shots
- Shots on target
- Corners
- Fouls
- Yellow cards
- Red cards

---

# 🏗️ Project Structure

```text
Premier-League-Prediction/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   └── 04_feature_engineering.ipynb
│
├── models/
│
├── src/
│
├── api/
│
├── frontend/
│
├── requirements.txt
├── README.md
└── .gitignore
