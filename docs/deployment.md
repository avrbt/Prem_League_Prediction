# Deployment Documentation

This document describes the production deployment configuration, Docker setup, and dependency management strategy.

---

## 1. Architecture

We recommend **Option A: Two Separate Services** for the production deployment:
1. **FastAPI Service**: Serves prediction endpoints and health checks via a JSON API.
2. **Streamlit Frontend**: Interacts with the user, collects input, communicates with the API, and visualizes predictions.

---

## 2. Production Dependency Strategy

To prevent build failures on Render and minimize container size, we separate the dependencies:
- **`requirements-dev.txt`**: Contains all packages, including Jupyter Notebook, matplotlib, and test runner libraries, used for local exploratory data analysis and development.
- **`requirements-api.txt`**: Contains only the core libraries required to run FastAPI, Uvicorn, and scikit-learn predictions.
- **`requirements-streamlit.txt`**: Contains only the libraries required to run Streamlit.

### Why Jupyter/Matplotlib is Excluded
Jupyter Notebook kernels, extensions, and web assets pull in over 60+ heavy development packages (such as `tornado`, `traitlets`, `nbconvert`, `jupyterlab`). These are only useful during exploration and add over 300MB of overhead, slow down pip installations, and increase security vulnerability surfaces in production containers.

### Version Compatibility Matrix
- **Python Version**: We use the official `python:3.11-slim` base image.
- **NumPy Version**: Pinned to `numpy>=1.26.4,<2.0.0`. This ensures compatibility with Python 3.11 and the scientific computing stack, avoiding installation errors seen with uncompiled pre-release versions.
- **scikit-learn Version**: Pinned to `scikit-learn==1.9.0` (matching the training environment) to prevent unpickling version warnings/inconsistencies when loading `models/final_model.pkl`.

---

## 3. Production Docker Configurations

We created separate Docker configurations for each service.

### FastAPI Service (`Dockerfile.api`)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt
COPY src/ ./src/
COPY app/ ./app/
COPY models/ ./models/
COPY data/processed/epl_clean.csv ./data/processed/epl_clean.csv
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Streamlit Frontend (`Dockerfile.streamlit`)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements-streamlit.txt .
RUN pip install --no-cache-dir -r requirements-streamlit.txt
COPY src/ ./src/
COPY app/ ./app/
COPY models/ ./models/
COPY data/processed/epl_clean.csv ./data/processed/epl_clean.csv
EXPOSE 8501
CMD ["streamlit", "run", "app/ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Exclusions (`.dockerignore`)
Excluded all development-specific dependencies to minimize image sizes:
- `.git`
- `.venv` & `venv`
- `__pycache__`
- `tests/`
- `.pytest_cache`
- `data/raw/` & `data/processed/train.csv` (keeping only `epl_clean.csv`)

---

## 4. Deployment Platform Recommendations (Render)

For a student-friendly, low-cost deployment, we recommend **Render**:
- **FastAPI**: Deploy as a **Web Service** using the Docker runtime pointing to `Dockerfile.api`.
- **Streamlit**: Deploy as a **Web Service** using the Docker runtime pointing to `Dockerfile.streamlit`.
- **GitHub Integration**: Render automatically triggers a new deployment when updates are pushed to the main branch.
