# Backend (Flask) - Minimal setup

This folder contains a minimal Flask app for local development and manual testing.

Files:
- `app.py` - Minimal Flask application with a root endpoint, health check, and a sample POST `/checkin` endpoint.
- `requirements.txt` - Python deps for the backend.

Quick start (macOS / zsh):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000/ or http://127.0.0.1:8000/docs to see details run:

```bash
curl http://127.0.0.1:8000/
```
