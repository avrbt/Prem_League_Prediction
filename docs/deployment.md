# Deployment Documentation

This document describes the production deployment configuration, Docker setup, and hosting platform recommendations.

---

## 1. Architecture

We recommend **Option A: Two Separate Services** for the production deployment:
1. **FastAPI Service**: Serves prediction endpoints and health checks via a JSON API.
2. **Streamlit Frontend**: Interacts with the user, collects input, communicates with the API (or runs in-process using model weights), and visualizes predictions.

### Rationale
Separating the frontend and backend services ensures that:
- **Independent Scaling**: The frontend UI can scale independently of prediction workloads.
- **Microservice Isolation**: Heavy traffic on the prediction API does not degrade frontend load performance.
- **Standard Tooling**: Exposes API endpoints for external integrations (e.g. mobile apps, automated bots).

---

## 2. Production Docker Configurations

We created separate Docker configurations for each service to allow independent deployments.

### FastAPI Service (`Dockerfile.api`)
Builds a minimal Python container that exposes port `8000` and starts the Uvicorn server:
```bash
docker build -t epl-api -f Dockerfile.api .
docker run -p 8000:8000 epl-api
```

### Streamlit Frontend (`Dockerfile.streamlit`)
Builds a frontend container exposing port `8501`:
```bash
docker build -t epl-streamlit -f Dockerfile.streamlit .
docker run -p 8501:8501 epl-streamlit
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

## 3. Deployment Platform Recommendations (Render)

For a student-friendly, low-cost deployment, we recommend **Render**:
- **FastAPI**: Deploy as a **Web Service** using the Docker runtime pointing to `Dockerfile.api`.
- **Streamlit**: Deploy as a **Web Service** using the Docker runtime pointing to `Dockerfile.streamlit`.
- **GitHub Integration**: Render automatically triggers a new deployment when updates are pushed to the main branch.

---

## 4. Local Startup & Commands

### Running Locally without Docker
1. **Activate Environment**:
   ```bash
   source venv/bin/activate
   ```
2. **FastAPI Startup**:
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```
3. **Streamlit Startup**:
   ```bash
   streamlit run app/ui.py --server.port 8501
   ```
