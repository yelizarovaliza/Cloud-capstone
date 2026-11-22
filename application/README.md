# Cloud Capstone Application

Python application scaffold for the Cloud Capstone project. It currently provides only a health-check endpoint; key-value, Coordinator, and Shard behavior has not been implemented.

## Setup

From this directory, create and activate a virtual environment, then install the application and test dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
```

Copy `.env.example` to `.env` and adjust local settings as needed.

## Run

```powershell
uvicorn app.main:app --reload
```

The health endpoint is available at `http://127.0.0.1:8000/health`.

## Test

```powershell
pytest
```
