# ⚽ Premier League Match Outcome Prediction

A serious, end-to-end machine learning project that predicts the outcome of English Premier League matches:
* `H` = Home Win
* `D` = Draw
* `A` = Away Win

The project focuses on **leakage-safe historical feature engineering**, **chronological validation**, and **probability calibration** to ensure that model outputs represent actual frequencies.

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Raw EPL Match Data] --> B[Data Cleaning & Mapping]
    B --> C[EDA & Target Verification]
    C --> D[Leakage-Safe Feature Engineering]
    D --> E[Chronological Train/Test Split]
    E --> F[TimeSeriesSplit CV & Tuning]
    F --> G[Probability Calibration]
    G --> H[Final Serialized Model]
    H --> I[Prediction Pipeline Module]
    I --> J[FastAPI Backend API]
    I --> K[Streamlit Prediction UI]
```

See [architecture.md](file:///home/avrbt/Documents/Projects/Prem_League/docs/architecture.md) for details.

---

## 📊 Model Comparison & Results

All models were evaluated on the exact same chronological test set (comprising seasons 2020/21 to 2024/25).

| Model | Accuracy | Macro Precision | Macro Recall | Macro F1 | Log Loss |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression (Baseline)** | **0.5401** | **0.4951** | **0.4513** | **0.3977** | **0.9915** |
| **Random Forest (Baseline)** | 0.4985 | 0.4194 | 0.4239 | 0.3995 | 1.0229 |
| **XGBoost (Baseline)** | 0.4783 | 0.4215 | 0.4188 | 0.4088 | 1.0816 |
| **Tuned XGBoost** | 0.5205 | 0.3540 | 0.4273 | 0.3705 | 0.9961 |
| **Calibrated XGBoost (Final)** | 0.5187 | 0.3475 | 0.4259 | 0.3697 | 1.0000 |

### Draw Prediction Insight
Due to severe class imbalance (Draws represent only ~24.6% of matches) and high outcome volatility, models tend to output low draw probabilities. By performing **probability threshold tuning** (predicting Draw if Draw probability exceeds `0.28`), we can boost Draw Recall from `0.01` to `0.1872`, improving overall macro F1-score to `0.4277`.

---

## ⚙️ How to Run

### 1. Set Up Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Tests
```bash
PYTHONPATH=. ./venv/bin/pytest
```

### 3. Run FastAPI Backend
```bash
PYTHONPATH=. ./venv/bin/uvicorn app.main:app --reload
```
API Documentation will be available at `http://127.0.0.1:8000/docs`.

### 4. Run Streamlit UI
```bash
./venv/bin/streamlit run app/ui.py
```
Open your browser at the local address printed by Streamlit.

---

## 📁 Repository Structure
See [PROJECT_STATUS.md](file:///home/avrbt/Documents/Projects/Prem_League/PROJECT_STATUS.md) for active tracking.
- `app/`: Streamlit interface (`ui.py`) and FastAPI backend (`main.py`).
- `src/`: Decoupled pipeline code (`config.py`, `data_loader.py`, `feature_engineering.py`, `prediction.py`).
- `models/`: Calibrated model, feature list, and metadata.
- `docs/`: In-depth project documentation (architecture, data dictionary, experiments log, model card).
- `tests/`: Automated test suite.
